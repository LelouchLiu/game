#A class that is collidable, movable, rotatable
import pymunk
from pymunk import Vec2d
from math import sin,cos,sqrt
class Physical():
	#orientation - angle body is facing in radians
	#shape - {"rectange": (width, height)}  or {"circle": radius}
	#resolution - screen resolution 
	#collisionType - used in collision handlers, 0: player, 1:projectile
	#angularVel - used for player turning speed, radians per update
	def __init__(self, worldPos, orientation, velocity, mass, elasticity, shape, maxVel, collisionType, angularVel=None):
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
		self.shape.collision_type = collisionType

	def _getShape(self, shape):
		if shape.has_key("circle"):
			self.shapeStr = "circle"
			self.radius = shape["circle"]
		elif shape.has_key("rectangle"):
			self.shapeStr = "rectangle"
			self.width, self.heigh = shape["rectangle"]

	def _setPhysics(self, worldPos):
		#pymunk initializations
		if self.shapeStr == "circle":
			self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius) #inner radius, outer
			self.body = pymunk.Body(self.mass,  self.inertia)
			self.shape = pymunk.Circle(self.body, self.radius)

		self.body.position = pymunk.Vec2d(worldPos[0], worldPos[1])
		self.body._set_velocity_limit(self.maxVel)
		self.shape.elasticity = self.elasticity

	#Projectile has an initial impule rather than using updatePos
	def applyImpulse(self):
		thrust = self.velocity
		force = pymunk.Vec2d(100 * thrust * self.vector.x, 100 *thrust * self.vector.y)
		offset = [0, 0]
		self.body.apply_impulse(force, r=offset)

	def updatePos(self):
		x = cos(self.orientation)
		y = sin(self.orientation)
		thrust = self.velocity * -self.direction[1]
		force = pymunk.Vec2d(thrust * x, thrust * y)
		#TODO: figure out the offset behind the ship. see if it is any different
		offset = [0, 0]
		self.body.apply_impulse(force, r=offset)