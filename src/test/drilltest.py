from pydrill.client import PyDrill

drill = PyDrill(host='localhost', port=8047)

if not drill.is_active():
    raise ImproperlyConfigured('Please run Drill first')

yelp_reviews = drill.query('''
  select id as ID,(sum(date_day)) as DAY from mysql_250.main.dates group by id
''')

for result in yelp_reviews.rows:
    print(result)