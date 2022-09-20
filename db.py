import sqlite3

def create_table():
    con = sqlite3.connect("System.db")

    cur = con.cursor()

    try:
        cur.execute("CREATE TABLE tblControles(cod)")
        cur.close()
    except:
        pass

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def insertCode(codigo): 
    sql = ''' INSERT INTO tblControles(IdentfControle,CodItem,NomeControle,DescricaoControle,CodControle)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, codigo)
    conn.commit()

    return cur.lastrowid

def insertCodeAdmin(codigo):
    sql = ''' INSERT INTO tblControles(IdentfControle,CodItem,NomeControle,DescricaoControle,CodControle)
              VALUES(?,?,?,?,?) '''
    cur = conn_admin.cursor()
    cur.execute(sql, codigo)
    conn_admin.commit()

    return cur.lastrowid

def getAll():
    sql = ''' SELECT * FROM tblControles'''
    cur = conn_admin.cursor()
    cur.execute(sql)
    
    tuples = cur.fetchall()
    return tuples


def getCode(codigo):
    try:
        sql = ''' SELECT * FROM tblControles
                WHERE CodControle = ?
                '''
        cur = conn.cursor()
        cur.execute(sql, (codigo,))
        
        tuples = cur.fetchall()[0][0]
        print('try')
        return tuples
    except:
        print('except')
        return ''

def updateCode(codigo):
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

def updateCodeAdmin(codigo):
    sql = '''UPDATE tblControles
        SET IdentfControle = ?,
            CodItem = ?,
            NomeControle = ?,
            DescricaoControle = ?
        WHERE CodControle = ?'''
    cur = conn_admin.cursor()
    cur.execute(sql, codigo)
    conn_admin.commit()

    return cur.lastrowid

def deleteCode(codigo):
    sql = '''DELETE FROM tblControles
        WHERE NomeControle = ?'''
    cur = conn.cursor()
    cur.execute(sql, (codigo,))
    conn.commit()

    return cur.lastrowid

def deleteCodeAdmin(codigo):
    sql = '''DELETE FROM tblControles
        WHERE NomeControle = ?'''
    cur = conn_admin.cursor()
    cur.execute(sql, (codigo,))
    conn_admin.commit()

    return cur.lastrowid

def getServer():
    sql = ''' SELECT * FROM servidor
        '''
    cur = conn_client.cursor()
    cur.execute(sql)
    
    tuples = cur.fetchall()[0]
    return list(tuples)


def getServerAdmin():
    sql = ''' SELECT * FROM servidor
        '''
    cur = conn_admin.cursor()
    cur.execute(sql)
    
    tuples = cur.fetchall()[0]
    return list(tuples)

def setServerAdmin(server_tup):
    sql = '''UPDATE servidor
        SET porta = ?,
            servidor = ?,
            login = ?,
            senha = ?
        WHERE porta = ?'''

    cur = conn_admin.cursor()
    cur.execute(sql, server_tup)
    conn_admin.commit()

def setServerBoo(server_tup):
    sql = '''UPDATE servidor
        SET porta = ?,
            servidor = ?,
            login = ?,
            senha = ?,
            boolean = ?
        WHERE porta = ?'''

    cur = conn_client.cursor()
    cur.execute(sql, server_tup)
    conn_client.commit()

conn = create_connection('System.db')
conn_client = create_connection('Cliente.db')
conn_admin = create_connection('Admin.db')
