import os          # Para interactuar con el SO y generar entropía criptográfica real.
import hashlib     # Para las funciones matemáticas de hash SHA-1 y SHA-256.
import hmac        # Para crear el código de autenticación y prevenir Timing Attacks.
import time        # Para obtener el Unix Timestamp necesario en Google Authenticator.
import base64      # Para codificar y decodificar en Base32.
import struct      # Para empaquetar bytes en estructuras de red (Big-Endian).
import binascii    # Para conversiones hexadecimales seguras.

def hashear_password(password_plano):
    # Genera 16 bytes de datos aleatorios criptográficamente seguros (Sal).
    sal = os.urandom(16) 
    # Ejecuta PBKDF2 con SHA-256, iterando 100,000 veces para frustrar fuerza bruta.
    hash_resultado = hashlib.pbkdf2_hmac('sha256', password_plano.encode('utf-8'), sal, 100000)
    # Convierte la sal a formato texto hexadecimal para poder guardarla.
    sal_hex = binascii.hexlify(sal).decode('ascii')
    # Convierte el hash resultante a formato texto hexadecimal.
    hash_hex = binascii.hexlify(hash_resultado).decode('ascii')
    # Retorna la sal y el hash unidos por dos puntos (formato estándar de almacenamiento).
    return f"{sal_hex}:{hash_hex}"

def verificar_password(password_intento, hash_guardado):
    # Separa la cadena guardada en la base de datos para obtener la sal y el hash.
    sal_hex, hash_original_hex = hash_guardado.split(':')
    # Revierte la sal de texto hexadecimal a sus bytes originales.
    sal = binascii.unhexlify(sal_hex)
    # Vuelve a calcular el hash usando la contraseña ingresada y la sal original.
    hash_intento = hashlib.pbkdf2_hmac('sha256', password_intento.encode('utf-8'), sal, 100000)
    # Convierte el hash original guardado de hexadecimal a bytes.
    hash_original_bytes = binascii.unhexlify(hash_original_hex)
    # Utiliza compare_digest para evitar ataques de canal lateral (Timing Attacks).
    return hmac.compare_digest(hash_intento, hash_original_bytes)

def generar_secreto_totp():
    # Genera 10 bytes completamente aleatorios.
    bytes_aleatorios = os.urandom(10)
    # Codifica en Base32 y quita los signos de igual, formato requerido por Google Authenticator.
    return base64.b32encode(bytes_aleatorios).decode('utf-8').replace('=', '')

def verificar_totp(secreto_b32, codigo_ingresado):
    # Calcula los intervalos de 30 segundos que han pasado desde el inicio del tiempo Unix.
    intervalo_tiempo = int(time.time() // 30)
    # Agrega relleno (padding) al secreto Base32 para evitar errores de decodificación.
    secreto_b32 += '=' * (-len(secreto_b32) % 8)
    # Decodifica el secreto ignorando si el usuario lo guardó con minúsculas.
    llave_bytes = base64.b32decode(secreto_b32, casefold=True)
    # Empaqueta el intervalo de tiempo en 8 bytes (formato Big-Endian).
    mensaje_tiempo = struct.pack(">Q", intervalo_tiempo)
    # Crea un HMAC usando el secreto, el tiempo y el algoritmo SHA-1.
    hmac_calculado = hmac.new(llave_bytes, mensaje_tiempo, hashlib.sha1).digest()
    # Toma los últimos 4 bits para determinar el "offset" dinámico.
    offset = hmac_calculado[19] & 15
    # Extrae 4 bytes del HMAC desde el offset omitiendo el bit de signo.
    token_entero = (struct.unpack(">I", hmac_calculado[offset:offset+4])[0] & 0x7fffffff)
    # Reduce el número resultante a 6 dígitos exactos.
    codigo_esperado = str(token_entero % 1000000).zfill(6)
    # Compara el código calculado con el ingresado usando compare_digest por seguridad.
    return hmac.compare_digest(codigo_esperado.encode('utf-8'), str(codigo_ingresado).encode('utf-8'))