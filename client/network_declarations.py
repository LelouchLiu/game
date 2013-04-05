#Network Declarations
from twisted.protocols.amp import (AMP, Command, Integer, Float, Argument, String, Boolean, ListOf)
from struct import pack, unpack

class Direction(Argument):
   # Encode complex objects as two bytes.

    def toString(self, direction):
        #Convert the direction to two bytes.

        if direction is not None:
            x = direction[0]
            y = direction[1]
        else:
            x = y = 0
        return pack("bb", x, y)

    def fromString(self, encodedDirection):
        #Convert the direction from bytes.
        direction = list(unpack("bb", encodedDirection))
        return direction


class Introduce(Command):
	#Client greeting message used to retrieve initial model state.
	response = [('identifier', Integer()), ('granularity', Integer()), ('x', Float()), ('y', Float())]


class NewPlayer(Command):
	#Notify someone that a Player with the given identifier is at the given position.
	arguments = [('identifier', Integer()), ('x', Float()), ('y', Float())]

class RemovePlayer(Command):
	#Notify someone that a Player with the given identifier has been removed.
	arguments = [('identifier', Integer())]

class SetMyDirection(Command):
	#Set the direction of mPlayer. Client -> Server
	arguments = [('direction', Direction())]

class SetDirectionOf(Command):
	#Set the position, orientation, and direction of a Player
	#This is a server to client command which indicates the new direction and position of a Player.
	arguments = [('identifier', Integer()),('direction', Direction())]

class SetMyPosition(Command):
	#Set the position of a Player Client -> Server
	arguments = [('identifier', Integer()),('x', Integer()), ('y', Integer())]