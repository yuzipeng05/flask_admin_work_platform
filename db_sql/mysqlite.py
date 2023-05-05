import sqlite3

# mydb = '..\\instance\\sample_db.sqlite'


def query_data_by_id(id, table, mydb):
    conn = sqlite3.connect(mydb)
    c = conn.cursor()
    sql = "select * from {} where id={}".format(table, id)
    cursor = c.execute(sql)
    res = cursor.fetchone()
    conn.close()
    return res

# query_data_by_id(1,'Price')