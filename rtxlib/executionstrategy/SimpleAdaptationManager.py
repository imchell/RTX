from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction

NUMBER_OF_DIMMER_LEVELS = 5
DIMMER_STEP = 1.0/ (NUMBER_OF_DIMMER_LEVELS - 1)
RT_THRESHOLD = 0.75
PERIOD = 60
import time

def start_simple_am(wf):
    """ executes forever - changes must come from definition file """
    info("> ExecStrategy   | simple_am ", Fore.CYAN)
    wf.totalExperiments = -1
    while True:

        server_state = effector(wf, '')
        response_time = 0
        is_server_boot = False
        print(server_state)
        dimmer = float(server_state['dimmer'])
        response_time = float(server_state['average_rt'])
        activeServers = float(server_state["active_servers"])
        servers = float(server_state["servers"])
        max_servers = float(server_state["max_servers"])
        total_util = server_state["total_util"]
        #["dimmer", "servers", "active_servers", "basic_rt", "optional_rt", "basic_throughput", "opt_throughput"]

        if(response_time > RT_THRESHOLD):
            if( (not is_server_boot) and servers < max_servers ):
                effector(wf, "add_server")
            elif(dimmer > 0.0):
                new_dimmer = max(0.0, dimmer - DIMMER_STEP)
                effector(wf, "set_dimmer " + str(new_dimmer))
        elif(response_time < RT_THRESHOLD):
            spare_util = activeServers - total_util

            if(spare_util > 1):
                if(dimmer < 1.0):
                    new_dimmer = min(1.0, dimmer + DIMMER_STEP)
                    effector(wf, "set_dimmer " + str(new_dimmer))
                elif( (not is_server_boot) and servers > 1):
                    effector(wf, "remove_server")
        
        time.sleep(PERIOD)






def effector(wf, action):
    return experimentFunction(wf, {
                "knobs": action,
                "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
                "sample_size": wf.execution_strategy["sample_size"]
            })