from time import sleep

import logging

import requests
from colorama import Fore
from flask import json
import socket

from rtxlib import info, error, debug, warn, direct_print, inline_print
from rtxlib.dataproviders.DataProvider import DataProvider

class SWIMDataProvider(DataProvider):
    """ implements a data provider based on http """

    def __init__(self, wf, dp):
        self.callBackFunction = None
        # load config
        try:
            self.host = dp["host"]
            self.port = dp["port"]
            self.metricslist = dp["server_metrics"]
            info(">SWIMDataPro    | Metric: " +  self.host + ":" + str(self.port), Fore.CYAN)
        except KeyError as e:
            error("SWIMDataPro definition was incomplete: " + str(e))
            exit(1)

    def returnData(self):
        """Grabs some TCP data from SWIM"""
        server_details = {}

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((self.host, self.port))


        for metric in self.metricslist:
            send_string = "get_" + metric
            s.sendall(send_string.encode('UTF-8'))
            server_details[metric] = s.recv(1024).decode('UTF-8')

        if(("total_util" in self.metricslist) and "active_servers" in self.metricslist):
            total_util = 0.0
            for i in range(1,int(server_details["active_servers"])+1):
                util_string = "get_utilization server" + str(i)
                s.sendall(util_string.encode('UTF-8'))
                total_util += float(s.recv(1024).decode('UTF-8'))

        server_details["total_util"] = total_util
            
        
        s.close()
        
        return server_details

        
       
    def returnDataListNonBlocking(self):
        """ by logic this can not be non-blocking, so it is implemented as returnData """
        server_details = {}

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((self.host, self.port))


        for metric in self.metricslist:
            s.sendall(metric.encode('UTF-8'))
            server_details[metric] = s.recv(1024).decode('UTF-8')

        if(("total_util" in self.metricslist) and "active_servers" in self.metricslist):
            total_util = 0.0
            for i in range(1,int(server_details["active_servers"])+1):
                util_string = "get_utilization server" + str(i)
                s.sendall(util_string.encode('UTF-8'))
                total_util += float(s.recv(1024).decode('UTF-8'))

        server_details["total_util"] = total_util
            
        
        s.close()
        
        return server_details
    
