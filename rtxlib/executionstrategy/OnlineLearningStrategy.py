from colorama import Fore

from rtxlib.executionstrategy.EvolutionaryStrategy import start_evolutionary_strategy, result_values, opti_values, \
    evolutionary_execution
from rtxlib.execution import experimentFunction
from river import compose, linear_model, preprocessing, metrics, utils
from rtxlib import info, warn


def wrap_with_online_learning(wf, pretrain_rounds=3, strategy=start_evolutionary_strategy, rounds=3,
                              control_group=False, online_model_iteration=26):
    """
    A wrapper for other strategies. Works like inserting an online learning algorithm into the underlying strategy.
    @param pretrain_rounds: How many rounds of data gathered by online learning model before formally executed.
    @param wf: Config defined in definition.py.
    @param strategy: The underlying strategy function (start_evolutionary_strategy, e.g.).
    @param rounds: The count of rounds of repeating the strategy.
    @param control_group: Initialize an experiment contains no online learning model.
    @param online_model_iteration: The count of rounds of repeating the execution of online learning model.
    Note that the actual result count is iteration - 1
    @return: None
    """
    if not control_group:
        model = init_model_pipeline()
        info("# Pretrain ML Model", Fore.CYAN)
        for i in range(pretrain_rounds):
            strategy(wf)
            feed_new_values(model, opti_values, result_values)
        for i in range(rounds):
            info("> Round      | " + str(i))
            strategy(wf)
            info("> opti_values| " + str(opti_values))
            info("> result     | " + str(result_values))
            info("# Online Learning Model Updating", Fore.CYAN)
            feed_new_values(model, opti_values, result_values)
            info("# Online Learning Updated", Fore.CYAN)
            online_model_execution(wf, model, opti_values[-1], result_values[-1], online_model_iteration)
            info("# End of Round ", Fore.CYAN)
    else:
        if (online_model_iteration - 1) % 5 is not 0:
            warn("# This is not a legitimate control group.")
        else:
            for i in range(pretrain_rounds):
                strategy(wf)
            for i in range(rounds):
                strategy(wf)
                for j in range(int((online_model_iteration - 1) / 5)):
                    strategy(wf)


def feed_new_values(model, opti, result):
    """
    Add newly generated results and knob input params into the online learning model.
    @param model: The online learning model.
    @param opti: A series of newly tested optimal input params.
    @param result: A series of newly tested output params.
    @return None
    """
    for i in range(len(result) - 1):
        model.learn_one({'result_value_prev': result[i], 'opti_value': opti[i]}, opti[i + 1])


def init_model_pipeline():
    """
    Initialize an online learning model pipeline.
    @return: Online learning model.
    """
    model = compose.Pipeline(
        ('lin_reg', linear_model.LinearRegression())
    )
    return model


def online_model_execution(wf, model, current_opti, current_result, iteration=10):
    """
    Execute online learning model to get the predicted optimal input param from it.
    @param wf: Config defined in definition.py.
    @param model: The online learning model.
    @param current_opti: The latest optimal input params.
    @param current_result: The latest optimal output params.
    @param iteration: The count of rounds of repeating the execution of online learning model.
    Note that the actual result count is iteration - 1
    @return: None
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
        next_opti = model.predict_one({'result_value_prev': result,
                                       'opti_value': next_opti})
        new_knobs = {'route_random_sigma': next_opti}

    experimentFunction(wf, {
        "knobs": new_knobs,
        "ignore_first_n_results": wf.execution_strategy["ignore_first_n_results"],
        "sample_size": wf.execution_strategy["sample_size"],
    })
