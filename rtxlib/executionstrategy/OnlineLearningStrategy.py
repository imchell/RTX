from colorama import Fore

from rtxlib.executionstrategy.EvolutionaryStrategy import start_evolutionary_strategy, result_values, opti_values, \
    evolutionary_execution
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

        info("# End of Round ", Fore.CYAN)


def feed_new_values(model, opti, result):
    for i in range(len(result) - 1):
        model.learn_one({'result_value_prev': result[i], 'opti_value': opti[i]}, opti[i + 1])


def init_model_pipeline():
    model = compose.Pipeline(
        ('lin_reg', linear_model.LinearRegression())
    )
    return model


def online_model_execution():
    pass
