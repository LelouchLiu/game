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
		self.tiles = [] #tiles in each layer [[tiles in layer1], [...], [tiles in layerN]]
		self._parse()
		
	def draw(self):
		pass

	def _parse(self):
		#Tile Sets
		for tileSet in self.dom.getElementsByTagName('tileset'):
			newTileSet = TileSet(tileSet.getAttribute('firstgid'),
							tileSet.getAttribute('name'),
							tileSet.getAttribute('tilewidth'),
							tileSet.getAttribute('tileheight'),
							tileSet.childNodes[1].getAttribute('source'),
							tileSet.getAttribute('width'),
							tileSet.getAttribute('imageheight'))
			self.tileSets.append(newTileSet)
		#Traverse Layers
		for layer in self.dom.getElementsByTagName('layer'):
			newLayer = Layer((layer.getAttribute('width'),layer.getAttribute('height')))
			newTiles = []
			for tile in layer.childNodes[1].getElementsByTagName('tile'):
				gid = tile.getAttribute('gid')
				size = 0
				src = self.getTileSet(gid)
				newTiles.append(Tile(gid,size,src))
			self.tiles.append(newTiles)

		for layer in self.tiles:
			for tile in layer:
				print tile.gid, tile.src

	#return appropriate Tile Set for grid ID, assumes tileSets are in ascending order by first grid ID
	def getTileSet(self, gid):
		previous = self.tileSets[0]
		for tileSet in self.tileSets:
			if tileSet.firstgid <= gid:
				previous = tileSet
			else:
				return previous.src


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
	def __init__(self, gid, size, src):
		self.gid = gid
		self.size = size
		self.src = src

#Stores information about each tile set
class TileSet:
	#firstgid - first grid ID of this tile set
	#tile width, tile heigh, source image, image width, image height
	def __init__(self, firstgid, name, tileW, tileH, src, imageW, imageH):
		self.firstgid = firstgid
		self.name = name
		self.tileW = tileW
		self.tileH = tileH
		self.src = src
		self.imageW = imageW
		self.imageH = imageH