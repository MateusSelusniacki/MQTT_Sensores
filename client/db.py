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
    sql = ''' INSERT INTO servidor(broker,id)
                VALUES(?,?) '''
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
        SET broker = ?,
            id = 1
        WHERE id = 0 OR id = 1'''

    cur = conn_client.cursor()
    cur.execute(sql, (server_tup,))
    conn_client.commit()
    conn_client.close()
    
conn = create_connection('Cliente.db')

print('deveria criar essa tabela------------------------------------------------------------')
sql ='''CREATE TABLE IF NOT EXISTS servidor(
    broker TEXT,
    id INT
)'''
c = conn.cursor()
c.execute(sql)
conn.commit()
conn.close()

try:
    server = getServer()
except:
    insert(('test.mosquitto.org','0'))
    server = getServer()