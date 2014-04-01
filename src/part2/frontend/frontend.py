#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import client_config as cf
import threading
import SocketServer
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
#import SimpleXMLRPCServer
import xmlrpclib
import socket
import re
import numpy as np
import socket

# Threaded mix-in
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass 

tally_board = [[0 for x in xrange(2)] for x in xrange(3)]
score_board = [[0 for x in xrange(3)] for x in xrange(3)]

team_name_dict = {"Gauls":0, "Romans":1}
medal_type_dict = {"Gold":0, "Silver":1, "Bronze":2}
event_type_dict = {"Curling":0, "Skating":1, "Skiing":2}

t_file = None
s_file = None

t_file_name = './log/tally_board.out'
s_file_name = './log/score_board.out'

#global sb_lock
#global output_lock
#global s_file_lock

def get_team_name_index(teamName):
	team_name_index = -1
	if team_name_dict.has_key(teamName): 	
		team_name_index = team_name_dict[teamName]
	return team_name_index

def get_medal_type_index(medalType):
	medal_type_index = -1
	if medal_type_dict.has_key(medalType): 	
		medal_type_index = medal_type_dict[medalType]
	return medal_type_index

def get_event_type_index(eventType):
	event_type_index = -1
	if event_type_dict.has_key(eventType): 	
		event_type_index = event_type_dict[eventType]
	return event_type_index

class ClientObject:
	def __init__(self, host_name, port, remote_host_name, remote_port):
		self.address = (host_name, port)
		self.remote_address = (remote_host_name, remote_port)

        URL = "http://" + self.remote_address[0] + ":" + str(self.remote_address[1]);
        self.s = xmlrpclib.ServerProxy(URL)

	def get_medal_tally(self, team_name = 'Gauls'):
		result = self.s.getMedalTally(team_name)
#		team_name_index = get_team_name_index(team_name)
#
#		if team_name_index != -1 :
#			tally_board[team_name_index] = result
#
#			# write obtained medal tally into the output file
#			with open(t_file_name, 'r+') as t_file :
#				t_file_data = t_file.readlines()
#				t_file_data[team_name_index] = str(team_name) + ': ' + str(result) + '\n'
#				t_file.seek(0)
#				t_file.writelines(t_file_data)

		return result

	def get_score(self, event_type = 'Curling'):
		result = self.s.getScore(event_type)

#		event_type_index = get_event_type_index(event_type)
#		if event_type_index != -1:
#			score_board[event_type_index] = result
#
#			# write obtained scores into the output file
#			with open(s_file_name, 'r+') as s_file :
#				s_file_data = s_file.readlines()
#				s_file_data[event_type_index] = str(event_type) + ': ' + str(result)  + '\n'
#				s_file.seek(0)
#				s_file.writelines(s_file_data)
		return result

	def incrementMedalTally(self, teamName, medalType):
        return self.s.incrementMedalTally(teamName, medalType)

	def setScore(self, eventType, score): # score is a list (score_of_Gauls, score_of_Romans, flag_whether_the_event_is_over)
        return self.s.setScore(eventType, score)

if __name__ == "__main__":
	if cf.self_ip == '' :
		host_name = socket.gethostbyname(socket.gethostname()) # try to automatically find the local ip, sometimes it may fail, so I suggest to denote the local ip in the configure file.
	else :
		host_name = cf.self_ip
	port = cf.self_port

	remote_host_name = cf.server_ip
	remote_port = cf.server_port

	server = AsyncXMLRPCServer(('', port), SimpleXMLRPCRequestHandler)

    try:
        server.register_instance(ClientObject(host_name, port, remote_host_name, remote_port))
    except socket.error, (value,message):
        print "Could not open socket to the server: " + message
        sys.exit(1)
    except :
        info = sys.exc_info()
        print "Unexpected exception, cannot connect to the server:", info[0],",",info[1]
        sys.exit(1)

    server.forever()