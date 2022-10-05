import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table():
    con = sqlite3.connect("Client.db")

    cur = con.cursor()

    try:
        cur.execute("CREATE TABLE if not exists ")
        cur.close()
    except:
        pass

def insert(codigo):
    conn = create_connection('Cliente.db')
    sql = ''' INSERT INTO servidor(porta,servidor,login,senha,boolean)
                VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, codigo)
    conn.commit()
    #close the connection
    conn.close()

def getServer():
    conn_client = create_connection('Cliente.db')
    sql = ''' SELECT * FROM servidor
        '''
    cur = conn_client.cursor()
    cur.execute(sql)

    tuples = cur.fetchall()

    conn_client.close()
    return list(tuples[0])


def setServerBoo(server_tup):
    conn_client = create_connection('Cliente.db')
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
    conn_client.close()
    
conn = create_connection('Cliente.db')

print('deveria criar essa tabela------------------------------------------------------------')
sql ='''CREATE TABLE IF NOT EXISTS servidor(
    porta INT,
    servidor TEXT,
    login TEXT,
    senha TEXT,
    boolean INT
)'''
c = conn.cursor()
c.execute(sql)
conn.commit()
conn.close()

try:
    server = getServer()
except:
    insert((55022,'179.105.72.237','admin','Ls001008**++',0))
    server = getServer()