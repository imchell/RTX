from colorama import Fore

from rtxlib import info, error
from rtxlib.execution import experimentFunction
from rtxlib.storage import State


def start_sequential_strategy(wf):
    """ executes all experiments from the definition file """
    info("> ExecStrategy   | Sequential", Fore.CYAN)
    wf.totalExperiments = len(wf.execution_strategy["knobs"])
    for kn in wf.execution_strategy["knobs"]:
        State.opti_values.append(kn["route_random_sigma"])
        result = experimentFunction(wf, {
            "knobs": kn,
            "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
            "sample_size": wf.execution_strategy["sample_size"],
        })
        State.result_values.append(result)
