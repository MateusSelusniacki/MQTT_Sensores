import sqlite3
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
    print('port',c_port,type(c_port),'user',c_user,type(c_user),'host',c_host,type(c_host),'password',c_password,type(c_password))
    try:
        conn = mariadb.connect(
            host=c_host,
            port=c_port,
            user=c_user,
            password=c_password,
            database="tblcontroles"

        )
        return conn
    except mariadb.Error as e:
        print(f"Error: {e}")

def insertCode(port,host,user,password,codigo): 
    print(port,host,user,password)
    conn = create_connection(port,host,user,password)
    print(f'inserindo {codigo} no banco {conn}')
    try:
        sql = ''' INSERT INTO tblControles(IdentfControle,CodItem,NomeControle,DescricaoControle,CodControle)
                VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, codigo)
        conn.commit()

        return cur.lastrowid
    except mariadb.Error as e:
        print(f"Error: {e}")

def getCode(port,host,user,password,codigo):
    conn = create_connection(port,host,user,password)
    try:
        sql = ''' SELECT * FROM tblControles
                WHERE CodControle = ?
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

        sql = ''' SELECT * FROM tblControles Where CodControle = ?
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
            SET IdentfControle = ?,
                CodItem = ?,
                NomeControle = ?,
                DescricaoControle = ?
            WHERE CodControle = ?'''
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
            WHERE NomeControle = ?'''
        print('2d')
        cur = conn.cursor()
        print('3d',codigo)
        cur.execute(sql, (codigo,))
        print('4d')
        conn.commit()
        print('deletado')
        return cur.lastrowid
    except mariadb.Error as e:
        print(f"Error: {e}")
        return -1