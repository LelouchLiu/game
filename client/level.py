import pygame
import math
import random
import os

class Level():

	#how large of squares to divide world into
	cellSize = 50
	def __init__(self, screenSize, manager, path):
		self.screenSize = screenSize
		self.tiles = []
		self.geometry = pygame.sprite.Group()
		self.screen = None
		self.manager = manager
		self.loadLevel(path)
					
	def loadLevel(self, path):
		lines = []
		fullpath = "levels/" + path
		with open(fullpath) as file:
			for line in file:
				line = line.rstrip()
				lines.append(line)
		self.worldSize = [len(lines[0]),len(lines)]
		for i in range(len(lines)): #y
			self.tiles.append([])
			for j in range(len(lines[0])): #x
				self.tiles[i].append(Tile((j * self.cellSize, i * self.cellSize), self.cellSize, False,))
				if lines[i][j] == '#':
					self.tiles[i][j].geometry = Geometry(self.tiles[i][j].rect.center, '/images/brick.png', True, False)
				if lines[i][j] == '+':
					self.tiles[i][j].geometry = Geometry(self.tiles[i][j].rect.center, '/images/cross.png', False, True)
					
		
	def drawGrid(self, screen):
		for i in range(len(self.tiles)):
			for j in range(len(self.tiles[0])):
				pygame.draw.rect(screen, pygame.Color('yellow'), self.tiles[i][j],1)
				
	def draw(self, screen, camera):
		self.drawTiles(screen,camera)
			
	#pos = worldPos of client
	def drawTiles(self, screen, camera):
		#playerScreen = left, right, top, bottom
		#playerScreen = (pos[0] - self.screenSize[0]/2, pos[0] + self.screenSize[0]/2, pos[1] - self.screenSize[1]/2, pos[1] + self.screenSize[1]/2)
		#Only want to draw part of level that overlaps with playerscreen
		
		pos = camera.center
		
		xstart = int(math.floor(camera.left))/self.cellSize
		xend = int(math.ceil(camera.right))/self.cellSize + 1
		ystart = int(math.floor(camera.top))/self.cellSize
		yend = int(math.ceil(camera.bottom))/self.cellSize + 1
		
		if xend >= len(self.tiles[0]):
			xend = len(self.tiles[0])
		if yend > len(self.tiles):
			yend = len(self.tiles)
		
		self.geometry.empty()
		#returnUpdate moves rectangles relative to client's position for display purposes
		for i in range(ystart, yend):
			for j in range(xstart, xend):
				if self.isObjectInside(self.tiles[i][j]):
					if self.tiles[i][j].geometry:
						self.tiles[i][j].geometry.rect = self.tiles[i][j].returnUpdate(pos)
						self.geometry.add(self.tiles[i][j].geometry)
					else:
						pygame.draw.rect(screen, pygame.Color('red'), self.tiles[i][j].returnUpdate(pos), 1)
				else:
					if self.tiles[i][j].geometry:
						self.tiles[i][j].geometry.rect = self.tiles[i][j].returnUpdate(pos)
						self.geometry.add(self.tiles[i][j].geometry)
					else:
						pygame.draw.rect(screen, pygame.Color('white'), self.tiles[i][j].returnUpdate(pos), 1)
		self.geometry.draw(self.screen)

	#returns True if object hits geometry
	def geometryCollision(self, obj):
		x = obj.worldPos[0]
		y = obj.worldPos[1]
		tile = self.getTile((x,y))
		if tile:
			if tile.geometry:
				if tile.geometry.collidable:
					return True
		return False
	
		
	#size of 'pos' object
	@staticmethod
	def collide(rect, pos, size):
		if rect.bottom < (pos[1] - size[1]/2):
			return False
		if rect.top > (pos[1] + size[1]/2):
			return False
		if rect.right < (pos[0] - size[0]/2):
			return False
		if rect.left > (pos[0] + size[0]/2):
			return False
		return True

	#is object inside the camera
	def isObjectInside(self, obj):
		tmpRect = obj.rect.move(self.screenSize[0]/2- self.manager.client.camera.centerx, 
					self.screenSize[1]/2- self.manager.client.camera.centery)
		#tmpRect = obj.rect.move(self.screenSize[0]/2- self.manager.client.worldPos[0], self.screenSize[1]/2- self.manager.client.worldPos[1])
		if tmpRect.colliderect(self.manager.client):
			return True
		else:
			for proj in self.manager.projectiles:
				if tmpRect.colliderect(proj):
					return True
		return False

	#moves an object and accouns for geometry collision, creep collision, 
	def moveObject(self, object, newPos):
		newX = newPos[0]
		newY = newPos[1]
			
		for player in self.manager.players:
			if player.id != object.id:
				rect = pygame.Rect(player.worldPos[0] - player.rect.size[0]/2, player.worldPos[1] - player.rect.size[1]/2,
						player.rect.size[0], player.rect.size[1])
				if self.collide(rect, [newX,object.worldPos[1]], player.rect.size):
					newX = object.worldPos[0]
				if self.collide(rect, [newX,newY], player.rect.size):
					newY = object.worldPos[1]	
					
		for creep in self.manager.creeps:
			if creep.id != object.id:
				rect = pygame.Rect(creep.worldPos[0] - creep.rect.size[0]/2, creep.worldPos[1] - creep.rect.size[1]/2,
						creep.rect.size[0], creep.rect.size[1])
				forceX = forceY = False
				if self.collide(rect, [newX,object.worldPos[1]], creep.rect.size):
					forceX = True
					newX = object.worldPos[0]
				if self.collide(rect, [newX,newY], creep.rect.size):
					forceY = True
					newY = object.worldPos[1]
				if forceX or forceY:
					x = player.direction[0]
					y = player.direction[1]
					#if forceX
					#creep.addForce(Force(player.id, 
					
				
		#Check for geometry
		tile = self.getTile([newX - object.rect.size[0]/2, object.worldPos[1]])
		flagX = flagY = False
		if tile:
			geometry = tile.geometry
			if geometry:
				if geometry.collidable:
					if geometry.worldPos[0] < object.worldPos[0]:
						newX = geometry.worldPos[0] + self.cellSize
						flagX = True

		if not flagX:
			tile = self.getTile([newX + object.rect.size[0]/2, object.worldPos[1]])
			if tile:
				geometry = tile.geometry
				if geometry:
					if geometry.collidable:
						if geometry.worldPos[0] > object.worldPos[0]:
							newX = geometry.worldPos[0] - self.cellSize
							flagX = True
							
		tile = self.getTile([newX, newY - object.rect.size[1]/2])
		if tile:
			geometry = tile.geometry
			if geometry:
				if geometry.collidable:
					if geometry.worldPos[1] < object.worldPos[1]:
						newY = geometry.worldPos[1] + self.cellSize
						flagY = True
		if not flagY:
			tile = self.getTile([newX, newY + object.rect.size[1]/2])
			if tile:
				geometry = tile.geometry
				if geometry:
					if geometry.collidable:
						if geometry.worldPos[1] > object.worldPos[1]:
							newY = geometry.worldPos[1] - self.cellSize	
							flagY = True
		return (newX,newY)
		
	#returns tile form tileList given a position
	def getTile(self, pos):
		if pos[0]/self.cellSize > len(self.tiles[0]) or pos[0]/self.cellSize < 0:
			return None
		if pos[1]/self.cellSize > len(self.tiles) or pos[1]/self.cellSize < 0:
			return None
		return self.tiles[int(pos[1]/self.cellSize)][int(pos[0]/self.cellSize)]

class Tile(pygame.sprite.Sprite):
	#pos = left, top
	screenSize = 400,400
	cellSize = 50,50

	def __init__(self, pos, cellSize, occupied):
		pygame.sprite.Sprite.__init__(self)
		self.cellSize = cellSize
		self.occupied = occupied
		self.rect = pygame.Rect(pos, (cellSize, cellSize))
		self.geometry = None

	def returnUpdate(self, pos):
		#return self.rect.move(self.rect.centerx-pos[0], self.rect.centery-pos[1])
		return self.rect.move(self.screenSize[0]/2-pos[0], self.screenSize[1]/2-pos[1])


class Geometry(pygame.sprite.Sprite):
	#filePath: which sprite to load i.e. "images/player.png"
	#collidable: True for collisions, False for none
	#destructable: Either False or amount of HP
	cellSize = 50
	
	def __init__(self,pos, filePath, collidable, destructable):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + filePath
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.worldPos = pos
		self.collidable = collidable

