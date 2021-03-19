# Example for using TCP (with SWIM)
#
# Start SWIM first
name = "Example-TCP-Swim"

host = '127.0.0.1'
port = 4242

execution_strategy = {
    "ignore_first_n_results": 0,
    "sample_size": 10,
    "type": "simple_am",
    "knobs": [ ]
}


def primary_data_reducer(state, newData, wf):
 
    state = newData

    return state


primary_data_provider = {
    "type": "swim_data",
    "host": '127.0.0.1',
    "port" : 4242,
    "server_metrics": ["dimmer", "servers", "active_servers", "basic_rt", "opt_rt", "basic_throughput", "opt_throughput", "max_servers", "total_util"],
    "data_reducer": primary_data_reducer
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
