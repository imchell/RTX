import time

from colorama import Fore
from rtxlib.storage.PipelineLib import naive_LR, naive_KNNR

from rtxlib import info, warn
from rtxlib.evaluation.OptimizationResult import add_time
from rtxlib.execution import experimentFunction
from rtxlib.executionstrategy.EvolutionaryStrategy import start_evolutionary_strategy
from rtxlib.storage import State


def wrap_with_online_learning(wf, pretrain_rounds=3, strategy=start_evolutionary_strategy, rounds=3,
                              online_model_iteration=26):
    """
    A wrapper for other strategies. Works like inserting an online learning algorithm into the underlying strategy.
    Args:
        wf: Config defined in definition.py.
        pretrain_rounds: How many rounds of data gathered by online learning model before formally executed.
        strategy: The underlying strategy function (start_evolutionary_strategy, e.g.).
        rounds: The count of rounds of repeating the strategy.
        online_model_iteration: The count of rounds of repeating the execution of online learning model.
    Note that the actual result count is iteration - 1

    Returns: None

    """
    online_learning_enabled = wf.execution_strategy["online_learning"]
    if online_learning_enabled:
        info("Online Learning Enabled")
        model = init_model_pipeline(naive_KNNR)  # select a machine learning model
        info("# Pretrain ML Model", Fore.CYAN)
        for i in range(pretrain_rounds):
            strategy(wf)
            feed_new_values(model, State.opti_values, State.result_values)
        for i in range(rounds):
            info("> Round      | " + str(i))
            strategy(wf)
            info("> opti_values| " + str(State.opti_values))
            info("> result     | " + str(State.result_values))
            info("# Online Learning Model Updating", Fore.CYAN)
            feed_new_values(model, State.opti_values, State.result_values)
            info("# Online Learning Updated", Fore.CYAN)
            online_model_execution(wf, model, State.opti_values[-1], State.result_values[-1], online_model_iteration)
            info("# End of Round ", Fore.CYAN)
    else:
        if (online_model_iteration - 1) % 5 is not 0:
            warn("# This is not a legitimate control group.")
        else:
            info("Online Learning Not Enabled")
            for i in range(pretrain_rounds):
                strategy(wf)
            for i in range(rounds):
                strategy(wf)
                for j in range(int((online_model_iteration - 1) / 5)):
                    strategy(wf)


def feed_new_values(model, opti, result):
    """
    Add newly generated results and knob input params into the online learning model.
    Args:
        model: The online learning model.
        opti: A series of newly tested optimal input params.
        result: A series of newly tested output params.

    Returns: None

    """
    for i in range(len(result) - 1):
        model.learn_one({'result_value_prev': result[i], 'opti_value': opti[i]}, opti[i + 1])


def init_model_pipeline(pipeline):
    """
    Initialize an online learning model pipeline.
    Args:
        pipeline: pipeline of online learning model
    Returns: Online learning model.

    """
    model = pipeline
    return model


def online_model_execution(wf, model, current_opti, current_result, iteration=10):
    """
    Execute online learning model to get the predicted optimal input param from it.
    Args:
        wf: Config defined in definition.py.
        model:
        current_opti: The latest optimal input params.
        current_result: The latest optimal output params.
        iteration: The count of rounds of repeating the execution of online learning model.
    Note that the actual result count is iteration - 1

    Returns: None

    """
    info("# Handled by Online Learning", Fore.CYAN)
    next_opti = model.predict_one({'result_value_prev': current_result,
                                   'opti_value': current_opti})
    new_knobs = {'route_random_sigma': next_opti}
    for i in range(iteration):
        result = experimentFunction(wf, {
            "knobs": new_knobs,
            "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
            "sample_size": wf.execution_strategy["sample_size"],
        })
        start_time = time.time()
        info("result_value_prev " + str(result))
        info("opti_value" + str(next_opti))
        next_opti = model.predict_one({'result_value_prev': result,
                                       'opti_value': next_opti})
        new_knobs = {'route_random_sigma': next_opti}
        add_time(time.time() - start_time)

    experimentFunction(wf, {
        "knobs": new_knobs,
        "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
        "sample_size": wf.execution_strategy["sample_size"],
    })
