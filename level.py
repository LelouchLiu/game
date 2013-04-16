#Level
import os
from xml.dom.minidom import parse, parseString
#http://wiki.python.org/moin/MiniDom
#http://gamedev.tutsplus.com/tutorials/implementation/parsing-tiled-tmx-format-maps-in-your-own-game-engine/
class Level():

	def __init__(self, f):
		self.filePath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/game/levels/" + f
		self.dom = parse(self.filePath)
		print self.dom.toxml()