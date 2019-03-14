from insert import MongoDB
from insert import SQL

conn              = SQL.connect('postgres', 'toegang', 'Tom-1998', '127.0.0.1')

def select_popularProducts():
    qry="SELECT _id from products WHERE price in (" \
        "SELECT max(price)" \
        "FROM products)" \
        "LIMIT {};".format(3)

    cursor=conn.cursor()
    cursor.execute(qry)
    res=cursor.fetchall()
    return res

def get_info_popularProducts(limiet):
    list=[]
    recommendation_list=select_popularProducts()
    for i in recommendation_list:
        id = str(i[0])
        cursor= MongoDB.get_database('products', limiet, {"_id":id})
        product = next(cursor, None)
        list.append(product)
    return list