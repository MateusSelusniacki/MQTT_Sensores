import sqlite3
import mysql.connector
#conn = create_connection("localhost","root","dell","tblcontroles")
def create_table():
    con = sqlite3.connect("System.db")

    cur = con.cursor()

    try:
        cur.execute("CREATE TABLE tblControles(cod)")
        cur.close()
    except:
        pass

def create_connection(c_host,c_user,c_password,c_database):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    mydb = mysql.connector.connect(
        host=c_host,
        user=c_user,
        password=c_password,
        database=c_database
    )

    return mydb

def insertCode(host,user,password,table,codigo): 
    conn = create_connection(host,user,password,table)
    print(f'inserindo {codigo} no banco')
    try:
        sql = ''' INSERT INTO tblControles(IdentfControle,CodItem,NomeControle,DescricaoControle,CodControle)
                VALUES(%s,%s,%s,%s,%s) '''
        cur = conn.cursor()
        cur.execute(sql, codigo)
        conn.commit()

        return cur.lastrowid
    except:
        pass

def getCode(host,user,password,table,codigo):
    conn = create_connection(host,user,password,table)
    try:
        sql = ''' SELECT * FROM tblControles
                WHERE CodControle = %s
                '''
        cur = conn.cursor()
        cur.execute(sql, (codigo,))
        
        tuples = cur.fetchall()[0][3]
        return tuples
    except:
        return ""

def get_row_byCode(host,user,password,table,codigo):
    conn = create_connection(host,user,password,table)
    try:
        sql = ''' SELECT * FROM tblControles Where CodControle = %s
                '''
        cur = conn.cursor()
        cur.execute(sql, (codigo,))
        
        tuples = cur.fetchall()[0]
        return tuples
    except:
        print('except')
        return ""

def get_all(host,user,password,table):
    conn = create_connection(host,user,password,table)
    sql = ''' SELECT * FROM tblControles
            '''
    cur = conn.cursor()
    cur.execute(sql)
    
    tuples = cur.fetchall()
    return tuples

def updateCode(host,user,password,table,codigo):
    conn = create_connection(host,user,password,table)
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


def deleteCode(host,user,password,table,codigo):
    conn = create_connection(host,user,password,table)
    print('deletando')
    try:
        sql = '''DELETE FROM tblControles
            WHERE NomeControle = %s'''
        cur = conn.cursor()
        cur.execute(sql, (codigo,))
        conn.commit()

        return cur.lastrowid
    except:
        pass