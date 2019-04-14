from insert import MongoDB
from insert import SQL
from statistics import mode



conn              = SQL.connect('postgres', 'toegang', 'Tom-1998', '127.0.0.1')

#POPULAR
def select_popularProducts(expiration_date,limiet):
    # qry0="SELECT _id from products WHERE price in (" \
    #     "SELECT max(price)" \
    #     "FROM products)" \
    #     "LIMIT {};".format(3)

    qry="""select order_products.product_id, session_id, session_start
            from order_products
            inner join products on products._id=order_products.product_id
            inner join sessions on order_products.session_id=sessions._id
            where sessions.session_start>'{}' limit{};""".format(expiration_date,limiet)
    cursor=conn.cursor()
    cursor.execute(qry)
    res=cursor.fetchall()
    return res

def get_popularProducts(limiet):
    list=[]
    recommendation_list=select_popularProducts(limiet)
    for i in recommendation_list:
        id = str(i[0])
        cursor= MongoDB.get_database('products', 9999999999, {"_id":id})
        product = next(cursor, None)
        list.append(product)
    return list



# PERSONAL
def select_ordered_products(visitor_id):
    qry="""select order_products.product_id from visitors 
            inner join visitors_buids on visitors_buids._id=visitors._id
            inner join sessions on sessions.buid=visitors_buids.buid
            inner join order_products on order_products.session_id=sessions._id
            inner join products on products._id=order_products.product_id
            where visitors._id='{}' """.format(visitor_id)
    cursor=conn.cursor()
    cursor.execute(qry)
    res=cursor.fetchall()
    ordered_products=[]
    for product in res:
        product=product[0]
        ordered_products.append(product)
    print('ordered products',ordered_products)
    return ordered_products

def make_idealProduct(visitor_id):
    products=select_ordered_products(visitor_id)
    # products=['23978','7225','29438','16121']

    product_specs=[]

    most_common_categories=[]
    for product in products:
        qry="""select sub_category,sub_sub_category,brand,price from products where _id='{}'""".format(product)
        cursor=conn.cursor()
        cursor.execute(qry)
        res=cursor.fetchall()
        for spec in res[0]:
            product_specs.append(spec)

    for i in range(0,4):
        cat_list = []
        for j in range(i,len(product_specs),4):
            cat_list.append(product_specs[j])
        try:
            most_common_categories.append(mode(cat_list))
        except Exception as e:
            most_common_categories.append(cat_list[0])

    return most_common_categories,products

def select_similar_products(limiet,visitor_id):
    idealProduct,ordered_products=make_idealProduct(visitor_id)
    qry="""select * from products
          where sub_category='{}' 
          and sub_sub_category='{}' 
          and brand='{}' and price='{}'""".format(idealProduct[0],idealProduct[1],idealProduct[2],idealProduct[3])
    cursor=conn.cursor()
    cursor.execute(qry)
    similars=cursor.fetchall()

    personal_product_id=[]
    for product in similars:
        product_id=product[0]
        if product_id not in ordered_products:   #check if similar product is not the same as orderd product
            personal_product_id.append(product_id)
            limiet-=1
        if limiet==0:
            break

    return personal_product_id

def get_personalProducts(limiet,visitor_id):
    personal_product_id=select_similar_products(limiet,visitor_id)
    personal_products=[]
    for product_id in personal_product_id:
        cursor=MongoDB.get_database('products',9999999999,{"_id":product_id})
        product = next(cursor, None)
        personal_products.append(product)
    return personal_products









