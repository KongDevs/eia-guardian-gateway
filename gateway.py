import sys
import time
from eia_auth import validar_codigo_2fa

def mostrar_banner():
    banner = """
    ====================================================
               EBROMARES AJAW INTELLIGENCE             
                    CUSTOS SUB DEO                     
                                                       
              E.I.A. GUARDIAN GATEWAY v1.0             
    ====================================================
    """
    print(banner)

def iniciar_gateway():
    mostrar_banner()
    
    usuario = input("User ID: ").strip()
    
    if not usuario:
        print("Error: Identificación requerida.")
        sys.exit(1)

    print("\nIniciando protocolo de verificación...")
    time.sleep(1) # Simulación de latencia de red
    
    codigo = input("Ingrese el token de Google Authenticator (6 dígitos): ").strip()
    
    if validar_codigo_2fa(usuario, codigo):
        print("\n[+] AUTENTICACIÓN EXITOSA")
        print(f"[+] Bienvenido al sistema, {usuario}. Acceso concedido.")
        # Aquí iría la lógica para abrir el dashboard o la siguiente app
    else:
        print("\n[-] ACCESO DENEGADO")
        print("[-] Token inválido o usuario no encontrado. Se ha registrado el intento.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        iniciar_gateway()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario. Cerrando Gateway...")
        sys.exit(0)