import sys
from twisted.internet import reactor
from twisted.python import log
#from client.player import *
#from client.environment import Environment
#from client.ui import *
sys.path.append('data')

def main():
	print 'Client'
	host = 'localhost'
	port = 1338
	multi = False
	
	if multi: 
		run(host,port)
	else:
		#environment = Environment(100, reactor)
		#environment.start()
		#window = Window(environment)
		#player = Player([200,200], 7, environment.seconds)
		#window.client = player
		#window.submitTo(PlayerController(player))
		#window.go()
		#reactor.run()
		
def run(host, port):
	log.startLogging(sys.stdout)
	#client = UI()
	a = client.start(host,port)
	#a.addErrback(log.err, "Problem Running UI")
	#client.addCallback(lambda ignored: self.reactor.stop())
	#reactor.connectTCP('localhost',1337, client)
	#client.reactor.run()
	

if __name__ == '__main__':
    main()