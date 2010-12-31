#!/usr/bin/env python
from twisted.internet import reactor #sudo pip install -U twisted
from twisted.web.server import Site
from twisted.web.resource import Resource
from optparse import OptionParser
import re

# === Python Thumbnai Server
#
# ### To run:  
#
# $ sudo pip install -U twisted         
# $ python webserver_thumbnails.py
# 
# Or add optional params:
#
# $ python webserver_thumbnails.py [--port n] [--width x] [--height y]
# 
# For example:
# $ python webserver_thumbnails.py --port 8000 --width 320 --height 200
#
# ### To use using HTTP GET:
# $ curl -O out.png "http://localhost:8080?url=http://www.cnn.com"
#
## ### To use using HTTP POST:
# $ curl -O out.png -X POST -F 'url=http://politicalticker.blogs.cnn.com/2010/12/07/live-blog-president-obamas-news-conference/' "http://localhost:8080"
#
#
# ### To set width and height in the request:
# $ curl -O out.png "http://localhost:8080?width=320&height=240&url=http://www.cnn.com"
#

from webkit2png import WebkitRenderer, init_qtgui
from PyQt4.QtCore import QTimer

def generate_thumbnail(url, width, height):
	renderer = WebkitRenderer()
	renderer.width = 1280
	renderer.height = 768
	renderer.timeout = 60
	renderer.wait = 3
	renderer.format = "png"
	renderer.scaleRatio = "crop"
	renderer.scaleToWidth = width
	renderer.scaleToHeight = height
	renderer.grabWholeWindow = False
	#outfile = open("stackoverflow.png", "w")
	#renderer.render_to_file(url=url, file=outfile)
	#outfile.close()
	return renderer.render_to_bytes(url)


class WebServerMain(Resource):
	isLeaf = True
	def __init__(self):
		self.default_width = 640
		self.default_height = 480
#	def __init__(self,start_options):
#		self.default_width = start_options.width
#		self.default_height = start_options.height
	
	def render_GET(self, request):
		if (not request.args.has_key("url")) or (len(request.args["url"])==0):
			return ""
		url = request.args["url"][0]
		if None==re.search("^http(|s):\/\/", url):
			url = "http://"+url
		print "[Python] Processing thumbnail   %s" % url
		if request.args.has_key("width"):
			try:
				width=int(request.args["width"][0])
			except ValueError:
				width=self.default_width
		else:
			width=self.default_width
		if request.args.has_key("height"):
			try:
				height=int(request.args["height"][0])
			except ValueError:
				height=self.default_height
		else:
			height=self.default_height
		img = generate_thumbnail(url, width, height)
		request.setHeader('Content-Type', 'image/png; charset=UTF-8')
		request.setHeader('content-disposition', 'inline;filename=out.png')
		print "[Python] Completed OK thumbnail %s" % url
		return img

	def render_POST(self, request):
		return self.render_GET(request);



description = "Thumbnail generator webserver"

parser = OptionParser(usage="usage: %prog [options] <URL>",
                      description="Thumbnail generator webserver", 
                      add_help_option=True)
parser.add_option("-p", "--port", type="int", dest="port",default=8080,help="Server Port to listen on (default: %default)")
parser.add_option("-x", "--width", type="int", dest="width",default=640,help="Default thumbnail width (default: %default)")
parser.add_option("-y", "--height", type="int", dest="height",default=480,help="Default thumbnail height (default: %default)")
#parser.add_option("-a", "--aspect", type="string", dest="height",default=480,help="Default thumbnail height (default: %default)")

(start_options,args) = parser.parse_args()

app = init_qtgui()
resource = WebServerMain()
factory = Site(resource)
reactor.listenTCP(start_options.port, factory)
print "[Python] Server start listening on port %s..." % start_options.port
reactor.run()

