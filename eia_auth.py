import os
import pandas as pd
import pyotp

EXCEL_DB = "usuarios_master.xlsx"

def obtener_secreto_usuario(usuario):
    """Busca el secreto TOTP del usuario en la base de datos Excel."""
    if not os.path.exists(EXCEL_DB):
        return None
        
    df = pd.read_excel(EXCEL_DB)
    registro = df[df['Usuario'] == usuario]
    
    if not registro.empty:
        return registro.iloc[0]['Secreto_TOTP']
    return None

def validar_codigo_2fa(usuario, codigo_ingresado):
    """Valida el código de 6 dígitos usando el secreto del usuario."""
    secreto = obtener_secreto_usuario(usuario)
    
    if not secreto:
        return False
        
    totp = pyotp.TOTP(secreto)
    return totp.verify(codigo_ingresado)