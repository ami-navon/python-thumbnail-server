#!/usr/bin/env python
from twisted.internet import reactor #sudo pip install -U twisted
from twisted.web.server import Site
from twisted.web.resource import Resource
import re

# === Python Thumbnai Server
#
# ### To run:  
#
# sudo pip install -U twisted         
# python webserver_thumbnails.py
# 
# ### To use using HTTP GET:
# $ curl -O out.png "http://localhost:8080?url=http://www.cnn.com"
#
## ### To use using HTTP POST:
# $ curl -O out.png -X POST -F 'url=http://politicalticker.blogs.cnn.com/2010/12/07/live-blog-president-obamas-news-conference/' "http://localhost:8080"



from webkit2png import WebkitRenderer, init_qtgui
from PyQt4.QtCore import QTimer

def generate_thumbnail(url):
	renderer = WebkitRenderer()
	renderer.width = 1280
	renderer.height = 768
	renderer.timeout = 60
	renderer.wait = 3
	renderer.format = "png"
	renderer.scaleRatio = "crop"
	renderer.scaleToWidth = 640
	renderer.scaleToHeight = 480
	renderer.grabWholeWindow = False
	#outfile = open("stackoverflow.png", "w")
	#renderer.render_to_file(url=url, file=outfile)
	#outfile.close()
	return renderer.render_to_bytes(url)

SERVER_PORT = 8080

class WebServerMain(Resource):
	isLeaf = True

	def render_GET(self, request):
		if (not request.args.has_key("url")) or (len(request.args["url"])==0):
			return ""
		url = request.args["url"][0]
		print "[Python] Processing thumbnail   %s" % url
		img = generate_thumbnail(url)
		request.setHeader('Content-Type', 'img/png; charset=UTF-8')
		print "[Python] Completed OK thumbnail %s" % url
		return img

	def render_POST(self, request):
		return self.render_GET(request);


app = init_qtgui()
resource = WebServerMain()
factory = Site(resource)
reactor.listenTCP(SERVER_PORT, factory)
print "[Python] Server start listening on port %s..." % SERVER_PORT
reactor.run()

