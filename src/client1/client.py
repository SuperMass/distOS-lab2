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
import random
import socket
import time

tally_board = [[0 for x in xrange(2)] for x in xrange(3)]
score_board = [[0 for x in xrange(3)] for x in xrange(3)]

team_name_list = ['Gauls', 'Romans']
medal_type_list = ['Gold', 'Silver', 'Bronze']
event_type_list = ['Curling', 'Skating', 'Skiing']

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

def get_rand_value(value_list):
    return value_list[random.randrange(0, len(value_list))]

class ClientObject:
	def __init__(self, remote_host_name, remote_port):
		self.remote_address = (remote_host_name, remote_port)

	def get_medal_tally(self, s, team_name = 'Gauls'):
		result = s.get_medal_tally(team_name)

		team_name_index = get_team_name_index(team_name)
		if team_name_index != -1 :
			tally_board[team_name_index] = result

			# write obtained medal tally into the output file
			with open(t_file_name, 'r+') as t_file :
				t_file_data = t_file.readlines()
				t_file_data[team_name_index] = str(team_name) + ': ' + str(result) + '\n'
				t_file.seek(0)
				t_file.writelines(t_file_data)
		return result

	def get_score(self, s, event_type = 'Curling'):
		result = s.get_score(event_type)

		event_type_index = get_event_type_index(event_type)
		if event_type_index != -1:
			score_board[event_type_index] = result

			# write obtained scores into the output file
			with open(s_file_name, 'r+') as s_file :
				s_file_data = s_file.readlines()
				s_file_data[event_type_index] = str(event_type) + ': ' + str(result)  + '\n'
				s_file.seek(0)
				s_file.writelines(s_file_data)
		return result

	def start(self, poisson_lambda, simu_len, get_score_pb):
        t = np.random.rand(poisson_lambda*simu_len) * simu_len
        t.sort()
        t[1:len(t)-1] = t[1:len(t)-1] - t[0:len(t)-2]

		try:
			URL = "http://" + self.remote_address[0] + ":" + str(self.remote_address[1]);

			s = xmlrpclib.ServerProxy(URL)
		except socket.error, (value,message):
			print "Could not open socket to the server: " + message
			return
		except :
			info = sys.exc_info()
			print "Unexpected exception, cannot connect to the server:", info[0],",",info[1]
			return

        for t_val in t:
            time.sleep(t_val)
            if np.random.rand(1) < get_score_pb:
                result = self.get_score(s, get_rand_value(event_type_list)):
            else:
                result = self.get_medal_tally(s, get_rand_value(team_name_list)):

if __name__ == "__main__":
    ips = cf.server_ips
    ports = cf.server_ports
    ips_len = len(ips)

    rand_index = random.randrange(1,3)
	remote_host_name = ips[rand_index]
	remote_port = ports[rand_index]

    poisson_lambda = cf.poisson_lambda
    simu_len = cf.simu_len
    get_score_pb = cf.get_score_pb

	client = ClientObject(remote_host_name, remote_port)
	client.start(poisson_lambda, simu_len, get_score_pb)
