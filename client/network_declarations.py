#Network Declarations
from twisted.protocols.amp import (AMP, Command, Integer, Float, Argument, String, Boolean, ListOf)
from struct import pack, unpack

class Dir(Argument):
	#Encode L{complex} objects as two bytes.
	def toString(self, list):
		#Convert the direction to two bytes.
		if list is not None:
			x = list[0]
			y = list[1]
		else:
			x = y = 0
		return pack("bb", x, y)

	def fromString(self, encodedList):
		#Convert the list from bytes.
		direction = unpack("bb", encodedList)
		return list	

class Introduce(Command):
	#Client greeting message used to retrieve initial model state.
	response = [('identifier', Integer()), ('granularity', Integer()), ('x': Float()), ('y': Float())]


class NewPlayer(Command):
	#Notify someone that a L{Player} with the given C{identifier} is at the given position.

	arguments = [('identifier', Integer()), ('x': Float()), ('y': Float())]

	
class RemovePlayer(Command):
	#Notify someone that a L{Player} with the given C{identifier} has been removed.
	arguments = [('identifier', Integer())]
