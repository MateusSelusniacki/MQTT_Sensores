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

def getServerAdmin():
    sql = ''' SELECT * FROM servidor
        '''
    cur = conn_admin.cursor()
    cur.execute(sql)
    
    tuples = cur.fetchall()[0]
    return list(tuples)

def setServerAdmin(server_tup):
    print('setserver',server_tup)
    sql = '''UPDATE servidor
        SET porta = ?,
            servidor = ?,
            login = ?,
            senha = ?
        WHERE id = 1'''

    cur = conn_admin.cursor()
    cur.execute(sql, server_tup)
    conn_admin.commit()

conn_admin = create_connection('Admin.db')

setServerAdmin((123,'servidor','login','senha'))