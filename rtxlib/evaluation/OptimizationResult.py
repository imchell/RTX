import pandas as pd
import psutil
import statistics

algorithm_running_time = 0
CPU_percentage_utilization = []


def export_result_features(results_df: pd.DataFrame, output_param: str, pretrain_rounds=3):
    """
    Get the mean and variance of results (Pretrain stage is ignored).
    Args:
        results_df: The dataframe representation of results.csv
        output_param: A single column name of the dataframe of results.csv
        pretrain_rounds: How many rounds is the online learning model pretrained

    Returns: mean & variance

    """
    mean = results_df[output_param].iloc[pretrain_rounds * 5:].mean()
    variance = results_df[output_param].iloc[pretrain_rounds * 5:].var()
    return {"mean": mean, "variance": variance, "time": algorithm_running_time}


def add_time(time_span):
    """
    Add up the algorithm running time
    Args:
        time_span: Time span

    Returns: None

    """
    global algorithm_running_time
    algorithm_running_time += time_span


def record_cpu():
    """
    Record the current CPU utilization
    Returns: None

    """
    global CPU_percentage_utilization
    CPU_percentage_utilization.append(psutil.cpu_percent(interval=1))
