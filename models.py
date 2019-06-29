


def insert(con, imagename, predict, graph):
    """ INSERT処理 """
    cur = con.cursor()
    cur.execute('insert into results (imagename, predict, graph) values (?, ?, ?)', [imagename, predict, graph])
 
    pk = cur.lastrowid
    con.commit()
 
    return pk

def select(con, pk):
    """ 指定したキーのデータをSELECTする """
    cur = con.execute('select id, imagename, predict, graph, created from results where id=?', (pk,))
    return cur.fetchone()

def select_all(con):
    """ SELECTする """
    cur = con.execute('select id, imagename, predict, graph, created from results order by id desc')
    return cur.fetchall()

def delete(con, pk):
    """ 指定したキーのデータをDELETEする """
    cur = con.cursor()
    cur.execute('delete from results where id=?', (pk,))
    con.commit()