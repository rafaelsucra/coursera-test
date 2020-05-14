import sqlite3

#Conectando ao sqlite
conn = sqlite3.connect('liga_toscannanbol.db')
#definindo cursor
cursor = conn.cursor()

#Acessando com usuarios:
#Recebendo os valores do usuario:
bd_usuario = input("Usuario :")
bd_pass = input("Password :")

def acesso(usuario,password):
    """
    Esse é o documentation string (docstring) da função acesso.
    Essa função simplesmente recebe o valor do argumento passado por parâmetro.
    Verifica se é valido e se é administrador ou não.
    """
    query = "select tipo_acesso from main.ACESSO_USUARIO where usuario='"+usuario+"' and password='"+password+"';"

    print(query)

    cursor.execute(query)
    #cursor.execute("""select tipo_acesso from ACESSO_USUARIO where usuario='"""+usuario+"""' and password='"""+password+"""';""")
    
    #cursor.execute("""Select usuario from main.ACESSO_USUARIO;""")
   
    linha = []

    for reg in cursor.fetchone():
        linha=reg
        print(linha)
        print(reg)
        if linha == "ADM":
            print("Usuário Administrador:"+str(linha))
            return linha
        elif linha == "USU":
            print("Usuário não é Administrador:"+str(linha))
            return linha
        else:
            print("Usuário não está cadastrado:"+str(linha))
            return linha

acesso(usuario=bd_usuario,password=bd_pass)

conn.commit()

conn.close()
