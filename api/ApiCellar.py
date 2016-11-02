#!/usr/bin/python
# -*- coding: utf-8 -*-
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
#
# Api Cellar

import sys,re
import json, web
import urllib, urllib2
import base64
from Daemon import Daemon

##########
# CONFIG #
##########

# url winecellar php
url = 'http://localhost/cellar/api/wines'

# wine pics local path
winepics = '/var/www/cellar/pics/'

# MySQL
mysqlhost="localhost" # your host, usually localhost
mysqluser="cellar",   # your username
mysqlpasswd="cellar"  # your password
mysqldb="cellar"      # name of the data base


#############
# HTTP REST #
#############
web.config.debug = False

urls = (
  '/addean(.*)', 'addean',
  '/removeean(.*)', 'removeean',
  '/(.*)', 'index'
)


render = web.template.render('templates/', globals={'re':re})
app = web.application(urls, globals())

class index:
    def POST(self,uri):
        try:
          web.cookies().filename
          filenamereceived = web.cookies().filename
        except:
          filenamereceived == "generic"
        try :
          data = web.data()
        except:
          return web.badrequest()
        if data == "":
          return web.badrequest()
        print filenamereceived
        b64response = base64.b64encode(data)
        fh = open(winepics+filenamereceived+".png", "wb")
        fh.write(b64response.decode('base64'))
        fh.close()
        return "200 STORED"

class addean:
    def POST(self,uri):
        try :
          ID = web.data()
        except:
          return web.badrequest()
        con = MySQLdb.connect(host=mysqlhost, user=mysqluser, passwd=mysqlpasswd, db=mysqldb);
        cur = con.cursor()
        print ID
        cur.execute("""SELECT * from wine where EAN=%s""", (ID,))
        result = cur.fetchone()
        if result is None:
          print "no bottle"
          print ID
          data = {'EAN': ID, 'picture': ID+'.png'}
          data = json.dumps(data)
          req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
          f = urllib2.urlopen(req)
          response = f.read()
          f.close()
        else:
          cur.execute("""UPDATE wine SET nombre=(nombre+1) where EAN=%s""", (ID,))
          con.commit()
          print "Number of rows updated: %d" % cur.rowcount
          con.close()

class removeean:
    def POST(self,uri):
        try :
          ID = web.data()
        except:
          return web.badrequest()
        con = MySQLdb.connect(host=mysqlhost, user=mysqluser, passwd=mysqlpasswd, db=mysqldb);
        cur = con.cursor()
        print ID
        cur.execute("""SELECT * from wine where EAN=%s""", (ID,))
        result = cur.fetchone()
        if result is None:
          print "new bottle"
          print ID
          data = {'EAN': ID, 'picture': ID+'.png'}
          data = json.dumps(data)
          req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
          f = urllib2.urlopen(req)
          response = f.read()
          f.close()
        else:
          cur.execute("""UPDATE wine SET nombre=(nombre-1) where EAN=%s""", (ID,))
          con.commit()
          print "Number of rows updated: %d" % cur.rowcount
          con.close()


class MyDaemon(Daemon):
        def run(self):
          app.run()

if __name__ == "__main__":

        service = MyDaemon('/tmp/cellarapi.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        sys.argv[1] =  '2020'
                        service.start()
                elif 'stop' == sys.argv[1]:
                        service.stop()
                elif 'restart' == sys.argv[1]:
                        service.restart()
                elif 'console' == sys.argv[1]:
                        sys.argv[1] =  '2020'
                        service.console()

                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart|console" % sys.argv[0]
                sys.exit(2)

