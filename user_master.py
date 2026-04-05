import os
import pandas as pd
import pyotp

EXCEL_DB = "usuarios_master.xlsx"

def mostrar_banner():
    banner = """
    ====================================================
               EBROMARES AJAW INTELLIGENCE             
                    CUSTOS SUB DEO                     
                                                       
              E.I.A. GUARDIAN GATEWAY v1.0             
    ====================================================
    """
    print(banner)

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
        df = pd.DataFrame(columns=["Usuario", "Secreto_TOTP", "Telefono"])
        df.to_excel(EXCEL_DB, index=False)

def usuario_existe(usuario):
    if not os.path.exists(EXCEL_DB):
        return False
    df = pd.read_excel(EXCEL_DB)
    return not df[df['Usuario'] == usuario].empty

def guardar_usuario(usuario, secreto, telefono):
    df = pd.read_excel(EXCEL_DB)
    nuevo_registro = pd.DataFrame([{
        "Usuario": usuario, 
        "Secreto_TOTP": secreto,
        "Telefono": telefono
    }])
    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_excel(EXCEL_DB, index=False)

def provisionar_administrador():
    # 1. Mostrar identidad visual en el orden correcto
    mostrar_banner()
    mostrar_logo()
    
    print("\n[+] MÓDULO DE REGISTRO EIA GUARDIAN [+]")
    
    # 2. Validación de User ID (Alfanumérico)
    while True:
        username_input = input("Ingrese el nuevo User ID (solo letras y números): ").strip()
        if username_input.isalnum():
            break
        print("[-] Error: El User ID no puede estar vacío, no debe contener espacios ni caracteres especiales.")
    
    # 3. Validación de Lada Internacional
    while True:
        lada_input = input("Ingrese la lada internacional (ej. +52, +1): ").strip()
        if lada_input.startswith("+") and lada_input[1:].isdigit():
            break
        print("[-] Error: La lada debe comenzar con el signo '+' seguido de números.")
        
    # 4. Validación de Número de Teléfono (Solo números)
    while True:
        telefono_input = input("Ingrese el número de teléfono (solo números, sin espacios): ").strip()
        if telefono_input.isdigit():
            break
        print("[-] Error: El teléfono no puede estar vacío y debe contener únicamente números.")
    
    # Concatenamos la lada con el teléfono para guardarlo en la base de datos
    telefono_completo = f"{lada_input}{telefono_input}"
    
    print("\nIniciando secuencia de aprovisionamiento...")
    inicializar_bd()

    if usuario_existe(username_input):
        print(f"[-] Operación abortada: El usuario '{username_input}' ya se encuentra registrado.")
        return

    secreto_totp = pyotp.random_base32()
    
    guardar_usuario(username_input, secreto_totp, telefono_completo)
    
    print(f"\n[+] Administrador '{username_input}' aprovisionado exitosamente con el teléfono {telefono_completo}.")
    print("[!] Vincula el siguiente secreto en Google Authenticator para habilitar el 2FA.")
    print(f"[!] TU CÓDIGO SECRETO: {secreto_totp}\n")

if __name__ == "__main__":
    provisionar_administrador()


    