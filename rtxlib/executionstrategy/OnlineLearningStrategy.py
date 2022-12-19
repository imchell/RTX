from colorama import Fore

from rtxlib.executionstrategy.EvolutionaryStrategy import start_evolutionary_strategy, result_values, opti_values, \
    evolutionary_execution
from rtxlib.execution import experimentFunction
from river import compose, linear_model, preprocessing, metrics, utils
from rtxlib import info


def wrap_with_online_learning(wf, strategy=start_evolutionary_strategy, rounds=3):
    model = init_model_pipeline()
    for i in range(rounds):
        info("> Round      | " + str(i))
        strategy(wf)
        info("> opti_values| " + str(opti_values))
        info("> result     | " + str(result_values))
        info("# Online Learning Model Updating", Fore.CYAN)
        feed_new_values(model, opti_values, result_values)
        info("# Online Learning Updated", Fore.CYAN)
        online_model_execution(wf, model, opti_values[-1], result_values[-1], 3)
        info("# End of Round ", Fore.CYAN)


def feed_new_values(model, opti, result):
    for i in range(len(result) - 1):
        model.learn_one({'result_value_prev': result[i], 'opti_value': opti[i]}, opti[i + 1])


def init_model_pipeline():
    model = compose.Pipeline(
        ('lin_reg', linear_model.LinearRegression())
    )
    return model


def online_model_execution(wf, model, current_opti, current_result, iteration):
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
