# Example for using TCP (with SWIM)
#
# Start SWIM first
import socket

name = "Example-TCP-Swim"

host = '127.0.0.1'
port = 4242

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 1,
    "type": "simple_am",
    "knobs": [ ]
}

require_delays = ["set_dimmer", "add_server", "remove_server", "data"]

def primary_data_reducer(state, newData, wf):
 
    state = newData

    return state


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((host, port))

def send_message(msg):
    sock.sendall(msg.encode('UTF-8'))
    return sock.recv(1024).decode('UTF-8')

def close_socket():
    sock.close()

def last_action():
    return primary_data_provider["last_action"]

primary_data_provider = {
    "type": "swim_data",
    "server_metrics": ["dimmer", "servers", "active_servers", "basic_rt", "opt_rt", "basic_throughput", "opt_throughput", "max_servers", "total_util"],
    "data_reducer": primary_data_reducer,
    "last_action" : ""
}

change_provider = {
    "type": "swim_change",
}


def evaluator(resultState, wf):
    basicTput = float(resultState["basic_throughput"].strip('\n'))
    optTput = float(resultState["opt_throughput"].strip('\n'))
    
    resultState["average_rt"] = basicTput * float(resultState["basic_rt"].strip('\n')) \
        + optTput * float(resultState["opt_rt"].strip('\n')) / (basicTput + optTput)

    return resultState


def state_initializer(state, wf):
    #state["metrics"] = None
    #state["events"] = None
    # state["average_result"] = 0
    # state["chosen_metric"] = "response_time"
    return state


# def change_event_creator(variables, wf):
#     return variables
