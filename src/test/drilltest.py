from pydrill.client import PyDrill

drill = PyDrill(host='localhost', port=8047)

if not drill.is_active():
    raise ImproperlyConfigured('Please run Drill first')

yelp_reviews = drill.query('''
  select * from mysql_250.main.sales t0 left join mysql_250.main.dates t1 on t0.date_id = t1.id left join mysql_250.main.products t2 on t0.product_id = t2.id
''')

for result in yelp_reviews.rows:
    print(result)