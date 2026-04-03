import os
import pandas as pd
import pyotp
from dotenv import load_dotenv

load_dotenv()

EXCEL_DB = "usuarios_master.xlsx"
USERNAME = os.getenv("ADMIN_USER", "user.1")

def mostrar_logo():
    logo = r"""
                                               +++++++                                               
                                           +++++++++++++++                                           
                                          ++--+++++++++--++                                          
                                         ++++++-     -++++++                                         
                                        ++++++        -++-+++                                        
                                        -++++-         -++++-                                        
                                        -+--+-         -++++-                                        
                                      +++++++++++++++++++++++++                                      
                                      ---+++--+++++++++--++----                                      
                                       ++++-++++ +++ ++++-++++                                       
                                       ++ +++--++---++-++++ ++                                       
                                      -++---+  ++---+- -++-++++                                      
                                       +-+++-+++-+-+-+++++++-+                                       
                                      -+++-+++  ++-++  ++++ ++                                       
                                      +++++  +++++++++++--+++++                                      
                                 ++++++---+++++++++++++++++---++++++                                 
                              ++++++++++++------+++++-----++++++++++++++                             
                           +++--++---+----+-+++---+---+++-+---++---++--+++                           
                        +----++-++++---+++-------++++------+++---++++-++--+++                        
                     --------++++++--++-----+++++++++++++-----++--+++++++----+++                     
                   -------+++-+++---+----+++-+++++++++++++++----++-++++-+++----+++                   
                 ----+-----++-+++--+-----+++--+++++++++--+++-----++-+++-++-++--+++++                 
               ----------  ++-++--+-------+++++++++++++++++++-----++-++-+++ -+++++++++               
              --------- +++++-++-++----++++++  +++++++ +++++++----++-++++++++ -+++ ++++              
            ---- ---- ---+ ++ ++-+------+ ++++++ +-+ ++++++ +-----+++++ ++ ++-- -+++ -+++            
             ---+----+-+++++++++-++-----++++-+++++-++++++++++-----++-++++++++++ +--+++---            
              ---+- --+-++ ++ ++----------++++-+++-++++++ --+-----++-++ +++++ ++-  +---              
                ---++---++++-++++-++------+++ ++++-++++ +++ -----++-++++ +++++-+++---                
                  -------++++ -+-+--+----+++ +++---+++++ +++----+--++++ ++++-------                  
                    ---+-++-++++ ------+++  ++------+++++ -+++------ ++++-++-+----                   
                      ---+--+--++-------  +++--- ----++++++  +++++-+++--++++---                      
                        ----+---------  ------+++-----++++++   -+-++--++++---                        
                           ----++--    ------+++++++++--+----+    -+++----                           
                               ----+++-----           --------++++----                               
                                  ------+++++++++++++++++++++------                                  
                                       ---------+++++---------                                       
    """
    print(logo)

def inicializar_bd():
    if not os.path.exists(EXCEL_DB):
        df = pd.DataFrame(columns=["Usuario", "Contraseña_TOTP"])
        df.to_excel(EXCEL_DB, index=False)

def usuario_existe(usuario):
    if not os.path.exists(EXCEL_DB):
        return False
    df = pd.read_excel(EXCEL_DB)
    return not df[df['Usuario'] == usuario].empty

def guardar_usuario(usuario, secreto):
    df = pd.read_excel(EXCEL_DB)
    nuevo_registro = pd.DataFrame([{
        "Usuario": usuario, 
        "Contraseña_TOTP": secreto
    }])
    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_excel(EXCEL_DB, index=False)

def provisionar_administrador():
    mostrar_logo()
    print("Iniciando secuencia de generar codigo en Google Authenticator...")
    print("Generando código...")
    print("Copia y pega el código generado en Google Authenticator.")


    
    inicializar_bd()

    if usuario_existe(USERNAME):
        print("Operación abortada: El usuario ya se encuentra registrado.")
        return

    # Generar el secreto para Google Authenticator
    secreto_totp = pyotp.random_base32()
    
    # Guardar en Excel sin el teléfono
    guardar_usuario(USERNAME, secreto_totp)
    
    print(f"Administrador '{USERNAME}' Vincula en Google Authenticator.")
    print("Name: EIA Guardian")

    print(f"TU CONTRASEÑA (Guárdalo ahora): {secreto_totp}")

if __name__ == "__main__":
    provisionar_administrador()