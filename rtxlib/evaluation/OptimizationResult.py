from rtxlib import info, error
import pandas as pd
import time


def export_result_features(results_df: pd.DataFrame, output_param: str, pretrain_rounds=3):
    mean = results_df[output_param].iloc[pretrain_rounds * 5:].mean()
    variance = results_df[output_param].iloc[pretrain_rounds * 5:].var()
    return {"mean": mean, "variance": variance}

