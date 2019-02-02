#!/usr/bin/python

import sys, socket, csv, time, random
-
def main():
    #Define CLI given variables
    type = sys.argv[1]

    #directory = sys.argv[2] #data/
    try: directory = sys.argv[2]
    except IndexError: directory = 'data/'

    #rounds = sys.argv[3] #20
    try: rounds = sys.argv[3]
    except IndexError: rounds = 20

    #Begin traffic gen for client or server
    if str(type) == 'client':
        print 'Client generation starting...'
        for i in range(rounds):
            trafficGenClient.client((i + 1), directory)

    if str(type) == 'server':
        print 'Server generation starting...'
        for i in range(rounds):
            trafficGenServer.server((i + 1), directory)

    else:
        print 'Invalid host type. Please choose \'client\' or \'server\''

def client(n, directory):
	###Variables###

	#Network Variables
	s = socket.socket()
	host = '10.0.0.2'
	port = 5161

	###Testing Operations###

	#Connect to the server
	s.connect((host, port))

	#Client
	filename = str(directory + 'output_' + str(n) + '.csv')
	print 'STATUS: Currently on file ', filename

	with open(filename) as f:
		readCSV = csv.reader(f, delimiter=',')

		rowCount = 0
		for row in readCSV:
			print 'STATUS: Currently on row ', rowCount
			print 'NETWORK: Sent ', s.send(row[5])
			time.sleep(random.uniform(0.01,0.1))
			print 'NETWORK: Recevied ', s.recv(1024)
			rowCount=rowCount + 1
		s.close

def server(n, directory):
	###Variables###

	#Network Variables
	s = socket.socket()
	host = '10.0.0.2'
	port = 5161

	###Testing Operations###

	#Bind IP/Port to socket
	s.bind((host, port))

	#Listen for connections
	s.listen(5)
	c, addr = s.accept()
	print 'NETWORK: Got connection from ', addr

	#Server
	filename = str(directory + 'output_' + str(n) + '.csv')
	print 'STATUS: Currently on file ', filename

	with open(filename) as f:
		readCSV = csv.reader(f, delimiter=',')

		rowCount = 0
		for row in readCSV:
			print 'STATUS: Currently on row ', rowCount
			print 'NETWORK: Sent ', c.send(row[5])
			time.sleep(random.uniform(0.01, 0.1))
			print 'NETWORK: Recevied ', c.recv(1024)
			rowCount=rowCount + 1
		c.close()

main()
