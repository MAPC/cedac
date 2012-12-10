# CEDAC Expiring Use Atlas

A map to explore expiring use properties in combination with a set of thematic overlays.

Features:

* Leaflet Map (Mapclusterer, Bing Aerial)
* Twitter Bootstrap framework

MAPC Project team: Barry Fradkin, Clay Martin, Christian Spanring 

Client: [CEDAC](http://cedac.org)

## Dependencies

A PostgreSQL/PostGIS database is required for data storage and GeoDjango functionality. To create one, execute:

    $ createdb cedac -T template_postgis

Python dependencies can be installed through the pip requirements file:

    $ pip install -r requirements.txt

---

Copyright 2012 MAPC