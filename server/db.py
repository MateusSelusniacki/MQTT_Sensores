import sqlite3
try:
    import mysql.connector
except:
    import mariadb
#conn = create_connection("localhost","root","dell","tblcontroles")
def create_table():
    con = sqlite3.connect("System.db")

    cur = con.cursor()

    try:
        cur.execute("CREATE TABLE tblControles(cod)")
        cur.close()
    except:
        pass

def create_connection(c_port,c_host,c_user,c_password):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        mydb = mysql.connector.connect(
            host=c_host,
            user=c_user,
            password=c_password,
            database="tblcontroles"
        )

        return mydb
    except:
        print('não conectado ao banco de dados mysql')
    
    try:
        conn = mariadb.connect(
            host=c_host,
            user=c_user,
            password=c_password,
            database="tblcontroles"

        )
    except:
        print("não conectado mariadb")

def insertCode(port,host,user,password,codigo): 
    print(port,host,user,password)
    conn = create_connection(port,host,user,password)
    print(f'inserindo {codigo} no banco')
    try:
        sql = ''' INSERT INTO tblControles(IdentfControle,CodItem,NomeControle,DescricaoControle,CodControle)
                VALUES(%s,%s,%s,%s,%s) '''
        cur = conn.cursor()
        cur.execute(sql, codigo)
        conn.commit()

        return cur.lastrowid
    except:
        return -1

def getCode(port,host,user,password,codigo):
    conn = create_connection(port,host,user,password)
    try:
        sql = ''' SELECT * FROM tblControles
                WHERE CodControle = %s
                '''
        cur = conn.cursor()
        cur.execute(sql, (codigo,))
        
        tuples = cur.fetchall()[0][3]
        return tuples
    except:
        return -1

def get_row_byCode(port,host,user,password,codigo):
    try:
        conn = create_connection(port,host,user,password)

        sql = ''' SELECT * FROM tblControles Where CodControle = %s
                '''
        cur = conn.cursor()
        cur.execute(sql, (codigo,))
        
        tuples = cur.fetchall()[0]
        return tuples
    except:
        print('não encontrado')
        return -1
def get_all(port,host,user,password):
    try:
        conn = create_connection(port,host,user,password)
        sql = ''' SELECT * FROM tblControles
                '''
        cur = conn.cursor()
        cur.execute(sql)
        
        tuples = cur.fetchall()
        return tuples
    except:
        print('except get all')
        return -1

def updateCode(port,host,user,password,codigo):
    try:
        conn = create_connection(port,host,user,password)
        sql = '''UPDATE tblControles
            SET IdentfControle = %s,
                CodItem = %s,
                NomeControle = %s,
                DescricaoControle = %s
            WHERE CodControle = %s'''
        cur = conn.cursor()
        cur.execute(sql, codigo)
        conn.commit()

        return cur.lastrowid
    except:
        return -1


def deleteCode(port,host,user,password,codigo):
    conn = create_connection(port,host,user,password)
    print('deletando')
    try:
        print('1d')
        sql = '''DELETE FROM tblControles
            WHERE NomeControle = %s'''
        print('2d')
        cur = conn.cursor()
        sdfadf()
        print('3d',codigo)
        cur.execute(sql, (codigo,))
        print('4d')
        conn.commit()
        print('deletado')
        return cur.lastrowid
    except:
        print('except')
        return -1

