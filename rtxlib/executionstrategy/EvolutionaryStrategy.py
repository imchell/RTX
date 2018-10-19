from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction

# TODO extend code below to call the evolutionary search
def start_evolutionary_strategy(wf):
    info("> ExecStrategy   | Evolutionary", Fore.CYAN)
    # we look at the ranges the user has specified in the knobs
    knobs = wf.execution_strategy["knobs"]

    info("Knobs: "+str(knobs[0].keys()),Fore.YELLOW)
    info("Sample size: " + str(wf.execution_strategy["sample_size"]), Fore.YELLOW)

# TODO set knob values and call experimentFunction
# TODO check what the experimentFunction is doing
# TODO code below is copied
def evolutionary_execution(wf, opti_values, variables):
    """ this is the function we call and that returns a value for optimization """
    knob_object = recreate_knob_from_optimizer_values(variables, opti_values)
    # create a new experiment to run in execution
    exp = dict()
    exp["ignore_first_n_results"] = wf.execution_strategy["ignore_first_n_results"]
    exp["sample_size"] = wf.execution_strategy["sample_size"]
    exp["knobs"] = knob_object
    return experimentFunction(wf, exp)