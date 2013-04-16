#Level
import os
from xml.dom.minidom import parse, parseString
#http://wiki.python.org/moin/MiniDom
#http://gamedev.tutsplus.com/tutorials/implementation/parsing-tiled-tmx-format-maps-in-your-own-game-engine/
class Level():

	def __init__(self, f):
		self.filePath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + '/levels/' + f
		self.dom = parse(self.filePath)
		#print self.dom.toxml()
		self.tileSets = []
		self._parse()

	def _parse(self):
		for tileSet in self.dom.getElementsByTagName('tileset'):
			tmp = TileSet(tileSet.getAttribute('firstgid'),
							tileSet.getAttribute('name'),
							tileSet.getAttribute('tilewidth'),
							tileSet.getAttribute('tileheight'),
							tileSet.getAttribute('source'),
							tileSet.getAttribute('width'),
							tileSet.getAttribute('imageheight'))
			self.tileSets.append(tmp)
			

class TileSet:
	
	def __init__(self, firstgid, name, tileW, tileH, src, imageW, imageH):
		self.firstgid = firstgid
		self.name = name
		self.tileW = tileW
		self.tileH = tileH
		self.src = src
		self.imageW = imageW
		self.imageH = imageH