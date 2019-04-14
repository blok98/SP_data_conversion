
def change_query(query,value):
    if type(value)==list:
        value = value[0]
    attribute = str(value).replace("'", "")
    query += "'" + attribute + "'" + ","
    return query