Web API :

Please change mysql configuration in index.php

Get all wines:
curl -i -X GET http://localhost/cellar/api/wines

Get all wines with ‘chateau’ in their name:
curl -i -X GET http://localhost/cellar/api/wines/search/chateau

Get wine #5:
curl -i -X GET http://localhost/cellar/api/wines/5

Delete wine #5:
curl -i -X DELETE http://localhost/cellar/api/wines/5

Add a new wine:
curl -i -X POST -H 'Content-Type: application/json' -d '{"name": "New Wine", "year": "2009"}' http://localhost/cellar/api/wines

Modify wine #27:
curl -i -X PUT -H 'Content-Type: application/json' -d '{"id": "27", "name": "New Wine", "year": "2010"}' http://localhost/cellar/api/wines/27

Python API:

require python-webpy

usage: python2.7 ApiCellar.py start|stop|restart|console

check CONFIG part in ApiCellar.py (mysql, Web url...)

Listen on *:2020 by default (check end of file to change tcp port)

POST picture : http://localhost:2020 (sent filename in cookie: filename=0000.png)
POST new EAN, add new bottle for known EAN : http://localhost:2020/addean
POST remove bottle for known EAN: http://localhost:2020/removeean

