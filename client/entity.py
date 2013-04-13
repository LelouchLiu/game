#Entity - base class of players and enemies 

from projectile import *
from physical import Physical
from pymunk import Vec2d
from math import sin,cos,sqrt, pi
from twisted.internet import reactor


class Entity(pygame.sprite.Sprite, Physical):

	def __init__(self, recPos, worldPos, resolution, collisionType):
		pygame.sprite.Sprite.__init__(self)
		Physical.__init__(self, worldPos, orientation=0, velocity=50, mass=10,
							elasticity=0.65, shape={"circle": 20}, maxVel=200, 
							angularVel=0.087, collisionType = collisionType)

		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/ship.gif"
		self.origImage = pygame.image.load(imgPath)
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = recPos

		self.resolution = resolution
		self.direction= Vec2d(0,0) 
		self.observers = []
		self.coolDowns = [False]
		self.alive = True

		self.hp = 100

	def takeDmg(self, dmg):
		self.hp -= dmg
		if self.hp <= 0:
			self.alive = False
		print self.hp
	def setDirection(self, direction):
		self.direction = direction
		#for observer in self.observers:
			#observer.directionChanged(self)

	def addObserver(self, observer):
		#Add the given object to the list of those notified about state changes in this entity
		self.observers.append(observer)

	def getPosition(self):
		return list(self.worldPos)

	def resetCoolDown(self, identifier):
		self.coolDowns[identifier] = False

	#fire projectile of given id
	def fireProj(self, identifier):
		#need to fire projectile in front of entity
		if not self.coolDowns[identifier]:
			x = self.body.position[0] + (cos(self.orientation) * (self.radius + 2))
			y = (self.body.position[1] + (sin(self.orientation) * (self.radius + 2)))
			proj = Projectile([x, self.flipy(y)], [x, y], self.orientation, 
								0, self.seconds, identifier, 2)
			self.manager.addProjectile(proj)
			self.coolDowns[identifier] = True
			reactor.callLater(.25, self.resetCoolDown, identifier=identifier)
		#for observer in self.observers:
			#observer.createProjectile(proj)

	#Used to flip y coordinate, pymunk and pygame are inverted :/
	def flipy(self, y):
		return -y + self.resolution[1]

	def isAlive(self):
		return self.alive

	def updatePos(self):
		super(Entity, self).updatePos()
		#update sprite
		pos = self.body.position
		self.rect.center = (pos.x, self.flipy(pos.y))
		self.updateRot()
		#for observer in self.observers:
			#observer.posChanged(self)
		
	def updateRot(self):
		#update selfects orientation to current body orientation. Commented out for now
		#self.orientation = self.toDegrees(self.body._get_angle())
		self.orientation += -self.direction[0] * self.angularVel
		if self.orientation > (2 * pi):
			self.orientation -= (2 * pi)
		elif self.orientation < 0:
			self.orientation += (2 * pi)
		oldPos = copy.deepcopy(self.rect.center)
		self.image = pygame.transform.rotate(self.origImage, self.toDegrees(self.orientation))
		self.rect = self.image.get_rect(center=oldPos)
		self.body._set_angle(self.orientation)

	def toRadians(self, angle):
		return angle * pi / 180.0

	def toDegrees(self, angle):
		return angle * 180 / pi