#An entity that is collidable, movable, rotatable
import pymunk
from pymunk import Vec2d

class Entity():
	#orientation - angle body is facing in radians
	#shape - {"rectange": (width, height)}  or {"circle": radius}
	#angularVel - used for player turning speed
	def __init__(self, worldPos, orientation, velocity, mass, elasticity, shape, maxVel, angularVel=None):
		self.mass = mass
		self.elasticity = elasticity
		self.maxVel = maxVel
		self.angularVel = angularVel
		self._getSahpe(self, shape)
		self._setPhysics(self, worldPos):

	def _getShape(self, shape):
		if shape.has_key("rectangle"):
			self.shape = "rectangle"
			self.width, self.heigh = shape["rectangle"]
		elif shape.has_key("circle"):
			self.shape = "circle"
			self.radius = shape["circle"]
				
	def _setPhysics(self, worldPos):
		#pymunk initializations
		self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius) #mass, width, height
		self.body = pymunk.Body(self.mass,  self.inertia) #Mass, Moment of inertia
		self.shape = pymunk.Circle(self.body, self.radius)
		self.body.position = pymunk.Vec2d(worldPos[0], worldPos[1])
		self.body._set_velocity_limit(self.maxVel)
		self.shape.elasticity = self.elasticity
		self.applyForce()

	#Applies the initial impulse from velocity * 100
	def applyImpulse(self, impulse):
		thrust = self.velocity
		force = pymunk.Vec2d(100 * thrust * self.vector.x, 100 *thrust * self.vector.y)
		offset = [0, 0]
		self.body.apply_impulse(force, r=offset)