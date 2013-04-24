#Level
import os
from xml.dom.minidom import parse, parseString
from sprite_sheet import *

#python xml parsing - http://wiki.python.org/moin/MiniDom
#tiled tutorial - http://gamedev.tutsplus.com/tutorials/implementation/parsing-tiled-tmx-format-maps-in-your-own-game-engine/

class Level():
	#dom: xml Data
	#tiles: [[tiles in layer1], [...], [tiles in layerN]]
	#size: [width, height] of level
	def __init__(self, f, screen):
		self.filePath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + '/levels/' + f
		self.dom = parse(self.filePath)
		self.tileSets = []
		self.tiles = [] 
		self.size = None
		self._parse()
		self.draw(screen, [800,800]) 
		self.screen = screen
		
	#Draw entire level at once for now, look up good optimizations and fix
	def draw(self, screen, size):
		for layer in self.tiles:
			x = y = i = j = 0
			for tile in layer:
				x = size[0] / tile.tileSet.tileW * i
				y = size[1] / tile.tileSet.tileH * j
				#screen.blit(tile.tileSet.src, (x,y))
				
				#print x,y
				if x >= self.size[0]:
					i = 0
				else:
					i += 1
				if y >= self.size[1]:
					j = 0
				else:
					j += 1
				

	def _parse(self):
		#self.size = (self.dom.getElementsByTagName('map').getAttribute('width'),
					#self.dom.getElementsByTagName('map').getAttribute('height'))

		print self.dom.getElementsByTagName('map')
		#Tile Sets
		for tileSet in self.dom.getElementsByTagName('tileset'):
			newTileSet = TileSet(tileSet.getAttribute('firstgid'),
							tileSet.getAttribute('name'),
							int(tileSet.getAttribute('tilewidth')),
							int(tileSet.getAttribute('tileheight')),
							tileSet.childNodes[1].getAttribute('source'), #tileset.childNodes[1] refers to <image>
							int(tileSet.childNodes[1].getAttribute('width')),
							int(tileSet.childNodes[1].getAttribute('height')))
			self.tileSets.append(newTileSet)
		#Layers
		for layer in self.dom.getElementsByTagName('layer'):
			newLayer = Layer((layer.getAttribute('width'),layer.getAttribute('height')))
			newTiles = []
			for tile in layer.childNodes[1].getElementsByTagName('tile'):
				gid = tile.getAttribute('gid')
				tileSet= self.getTileSet(gid)
				newTiles.append(Tile(gid,tileSet))
			self.tiles.append(newTiles)

	#return appropriate Tile Set for grid ID, assumes tileSets are in ascending order by first grid ID
	def getTileSet(self, gid):
		previous = self.tileSets[0]
		for tileSet in self.tileSets:
			if tileSet.firstgid <= gid:
				previous = tileSet
			else:
				return previous

#Stores information about each tile set
class TileSet(SpriteSheet):
	#firstgid - first grid ID of this tile set
	#tile width, tile heigh, source image, image width, image height
	def __init__(self, firstgid, name, tileW, tileH, src, imageW, imageH):
		SpriteSheet.__init__(self, src)
		self.firstgid = firstgid
		self.name = name
		self.tileW = tileW
		self.tileH = tileH
		self.src = src
		self.imageW = imageW
		self.imageH = imageH

#Stores the tiles in one layer		
class Layer:
	def __init__(self, size):
		self.tiles = []
		self.size = size

	#adds a list of tiles
	def addTiles(self, tiles):
		self.tiles.append(tile)

#Each tile in the map
class Tile:
	#grid id of tile
	#size [width, height]
	#source image
	def __init__(self, gid, tileSet):
		self.gid = gid
		self.tileSet = tileSet

