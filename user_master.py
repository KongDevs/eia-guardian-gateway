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
    # Se agrega de nuevo la columna 'Telefono'
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
    mostrar_logo()
    
    # === INTERFAZ DE CAPTURA DE DATOS ===
    print("\n[+] MÓDULO DE REGISTRO EIA GUARDIAN [+]")
    username_input = input("Ingrese el nuevo User ID: ").strip()
    
    if not username_input:
        print("[-] Error: El User ID no puede estar vacío.")
        return
        
    telefono_input = input("Ingrese el número de teléfono: ").strip()
    
    print("\nIniciando secuencia de aprovisionamiento...")
    inicializar_bd()

    if usuario_existe(username_input):
        print(f"[-] Operación abortada: El usuario '{username_input}' ya se encuentra registrado.")
        return

    # Generar el secreto para Google Authenticator
    secreto_totp = pyotp.random_base32()
    
    # Guardar en Excel
    guardar_usuario(username_input, secreto_totp, telefono_input)
    
    print(f"\n[+] Administrador '{username_input}' aprovisionado exitosamente.")
    print("[!] Vincula el siguiente secreto en Google Authenticator para habilitar el 2FA.")
    print(f"[!] TU CÓDIGO SECRETO: {secreto_totp}\n")

if __name__ == "__main__":
    provisionar_administrador()
