from website import recommendation
from insert import SQL


def getPopularProducts(expiration_date,limiet):
    return recommendation.get_popularProducts(expiration_date,limiet)

def getPersonalProducts(session,limiet):
    print("Recommendations for session: {}".format(session['_id']))
    visitor_id=session['_id']
    return recommendation.get_personalProducts(limiet,visitor_id)
