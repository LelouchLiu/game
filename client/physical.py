#An entity that is collidable, movable, rotatable
import pymunk
from projectile import Projectile
from math import sin,cos,sqrt
from pymunk import Vec2d

class Physical():
	#orientation - angle body is facing in radians
	#shape - {"rectange": (width, height)}  or {"circle": radius}
	#resolution - screen resolution 
	#angularVel - used for player turning speed, radians per update
	def __init__(self, worldPos, orientation, velocity, mass, elasticity, shape, maxVel, resolution, angularVel=None):
		self.orientation = orientation
		self.velocity = velocity
		self.mass = mass
		self.elasticity = elasticity
		self.maxVel = maxVel
		self.angularVel = angularVel
		self.vector = Vec2d(cos(orientation), sin(orientation))
		self.radius = self.width = self.heigh = None
		self._getShape(shape)
		self._setPhysics(worldPos)

	def _getShape(self, shape):
		if shape.has_key("circle"):
			self.shape = "circle"
			self.radius = shape["circle"]
		elif shape.has_key("rectangle"):
			self.shape = "rectangle"
			self.width, self.heigh = shape["rectangle"]

	def _setPhysics(self, worldPos):
		#pymunk initializations
		if self.shape == "circle":
			self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius) #inner radius, outer
			self.body = pymunk.Body(self.mass,  self.inertia)
			self.shape = pymunk.Circle(self.body, self.radius)

		self.body.position = pymunk.Vec2d(worldPos[0], worldPos[1])
		self.body._set_velocity_limit(self.maxVel)
		self.shape.elasticity = self.elasticity

	#Applies the initial impulse from velocity * 100
	def applyImpulse(self, impulse):
		thrust = self.velocity
		force = pymunk.Vec2d(100 * thrust * self.vector.x, 100 *thrust * self.vector.y)
		offset = [0, 0]
		self.body.apply_impulse(force, r=offset)

	#fire projectile of given id
	def fireProj(self, identifier):
		#need to fire projectile in front of entity
		if not self.coolDowns[identifier]:
			x = self.body.position[0] + (cos(self.orientation) * (self.radius + 2))
			y = (self.body.position[1] + (sin(self.orientation) * (self.radius + 2)))
			proj = Projectile([x, self.flipy(y)], [x, y], self.orientation, 
								0, self.seconds, identifier)
			self.manager.addProjectile(proj)
			self.coolDowns[identifier] = True
			reactor.callLater(.25, self.resetCoolDown, identifier=identifier)
		#for observer in self.observers:
			#observer.createProjectile(proj)

	#Used to flip y coordinate, pymunk and pygame are inverted :/
	def flipy(self, y):
		return -y + self.resolution[1]