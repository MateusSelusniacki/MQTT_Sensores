import sqlite3

def create_table():
    con = sqlite3.connect("System.db")

    cur = con.cursor()

    try:
        cur.execute("CREATE TABLE codigo(cod)")
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
    sql = ''' INSERT INTO codigo(nome,numero,comando)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, codigo)
    conn.commit()

    return cur.lastrowid

def getCode(codigo):
    print(codigo + "|")
    try:
        sql = ''' SELECT * FROM codigo
                WHERE comando = ?
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
    sql = '''UPDATE codigo
        SET nome = ?,
            numero = ?
        WHERE comando = ?'''
    cur = conn.cursor()
    cur.execute(sql, codigo)
    conn.commit()

    return cur.lastrowid

def deleteCode(codigo):
    sql = '''DELETE FROM codigo
        WHERE cod = ?'''
    cur = conn.cursor()
    cur.execute(sql, (codigo,))
    conn.commit()

    return cur.lastrowid

conn = create_connection('System.db')