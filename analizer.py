from http.server import BaseHTTPRequestHandler, HTTPServer # Para montar el servidor web nativo.
import json                                              # Para parsear los payloads que envía el cliente.
import basedata                                          # Módulo local de persistencia actualizado.
import eia_guardian                                      # Módulo local de seguridad actualizado.

# Prepara la base de datos en cuanto arranca el servidor.
basedata.inicializar_tablas()

# Clase que procesa las peticiones HTTP entrantes.
class AnalizadorHandler(BaseHTTPRequestHandler):
    
    # Método nativo que intercepta todas las llamadas POST.
    def do_POST(self):
        # Valida que el cliente solo esté atacando el endpoint correcto.
        if self.path == '/login':
            # Extrae el tamaño del payload para saber cuántos bytes leer.
            longitud_contenido = int(self.headers['Content-Length'])
            # Lee el cuerpo de la petición HTTP.
            datos_raw = self.rfile.read(longitud_contenido)
            # Transforma los bytes crudos a un diccionario de Python.
            payload = json.loads(datos_raw.decode('utf-8'))
            
            # Obtiene las credenciales provistas por el cliente.
            username = payload.get('username')
            password = payload.get('password')
            codigo_mfa = payload.get('mfa')
            # Extrae la IP de origen para el análisis forense.
            ip_cliente = self.client_address[0]
            
            # Abre la conexión de solo lectura.
            conexion = basedata.conectar_bd()
            # Busca al usuario. Se usa (?) para evitar Inyección SQL.
            usuario = conexion.execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone()
            
            # Defensa contra enumeración: Mensaje ambiguo si el usuario no existe.
            if not usuario:
                basedata.registrar_auditoria(username, "USUARIO_DESCONOCIDO", ip_cliente)
                self.enviar_respuesta(401, {"error": "Credenciales inválidas."})
                return
            
            # Bloqueo estricto: Si la cuenta está comprometida, se detiene el flujo inmediatamente.
            if usuario['bloqueado']:
                basedata.registrar_auditoria(username, "INTENTO_CUENTA_BLOQUEADA", ip_cliente)
                self.enviar_respuesta(403, {"error": "Cuenta bloqueada por seguridad."})
                return
            
            # Valida la contraseña usando el algoritmo resistente a ataques de tiempo en eia_guardian.
            if not eia_guardian.verificar_password(password, usuario['hashed_password']):
                # Incrementa el contador de fallos.
                nuevos_intentos = usuario['intentos_fallidos'] + 1
                # Si llega a 5 fallos, activa el flag booleano de bloqueo.
                bloquear = 1 if nuevos_intentos >= 5 else 0
                
                # Actualiza el estado del usuario en la base de datos.
                conexion.execute("UPDATE usuarios SET intentos_fallidos = ?, bloqueado = ? WHERE username = ?", 
                                 (nuevos_intentos, bloquear, username))
                conexion.commit()
                
                # Registra el evento exacto en la bitácora interna.
                evento = "BLOQUEO_FUERZA_BRUTA" if bloquear else f"FALLO_PASSWORD_{nuevos_intentos}"
                basedata.registrar_auditoria(username, evento, ip_cliente)
                # Responde ambiguamente al atacante/usuario.
                self.enviar_respuesta(401, {"error": "Credenciales inválidas."})
                return
            
            # Valida el token TOTP dinámico de 6 dígitos.
            if not eia_guardian.verificar_totp(usuario['totp_secret'], codigo_mfa):
                basedata.registrar_auditoria(username, "FALLO_MFA", ip_cliente)
                self.enviar_respuesta(401, {"error": "Código de autenticador incorrecto."})
                return
            
            # Si el flujo llega aquí, el usuario es legítimo. Se resetean los fallos.
            conexion.execute("UPDATE usuarios SET intentos_fallidos = 0 WHERE username = ?", (username,))
            conexion.commit()
            
            # Log de éxito para las auditorías.
            basedata.registrar_auditoria(username, "LOGIN_EXITOSO", ip_cliente)
            # Se otorga el token de acceso o se procesa la lógica del analizador financiero.
            self.enviar_respuesta(200, {"status": "Acceso concedido al Analizador de Transacciones."})
            conexion.close()

    # Función auxiliar para despachar la respuesta HTTP con las cabeceras correctas.
    def enviar_respuesta(self, codigo_estado, diccionario_datos):
        # Escribe el código HTTP (200, 401, 403).
        self.send_response(codigo_estado)
        # Indica que el contenido devuelto es JSON seguro.
        self.send_header('Content-type', 'application/json')
        # Cierra la inyección de cabeceras.
        self.end_headers()
        # Envía el JSON empaquetado en bytes al cliente.
        self.wfile.write(json.dumps(diccionario_datos).encode('utf-8'))

# Verifica que este script sea el proceso principal.
if __name__ == '__main__':
    # Levanta el socket en todas las interfaces de red en el puerto 8080.
    servidor = HTTPServer(('0.0.0.0', 8080), AnalizadorHandler)
    print("Gatekeeper EIA iniciado en puerto 8080...")
    # Mantiene el proceso vivo escuchando de forma indefinida.
    servidor.serve_forever()