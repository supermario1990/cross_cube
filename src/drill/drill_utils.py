from pydrill.client import PyDrill

drill = PyDrill(host='localhost', port=8047)

def drill_get(sql):

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    yelp_reviews = drill.query(sql)
    return yelp_reviews.rows