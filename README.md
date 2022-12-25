# Online Learning Extension for RTX

The [original guide](ORIGINAL_README.md) focuses more on setup, while this readme serves as a guide on configuring this extension and observing the result.

## Setup for Local Development with Docker Desktop

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Install SUMO according to the [guide](https://sumo.dlr.de/docs/Installing/index.html).
3. Install Kafka by running
   ```shell
   docker run --name kafka --hostname kafka -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=localhost --env ADVERTISED_PORT=9092 spotify/kafka
   ```
   > **Note**
   > The command is different from the one provided in original guide because we work on macOS and Windows and it needs to be changed according to [this issue](https://github.com/Starofall/RTX/issues/3).
4. Download and install dependencies with **Python 2.7** in [CrowdNav](https://github.com/imchell/CrowdNav).
5. Make sure spotify/kafka is running in Docker.
   ![spotify/kafka](illustrations/docker.png)
6. Run `python run.py` in [CrowdNav](https://github.com/imchell/CrowdNav). The terminal will prompt
   ```shell
   #####################################
   #      Starting CrowdNav v0.2       #
   #####################################
   # Configuration:
   # Kafka-Host   -> localhost:9092
   # Kafka-Topic1 -> crowd-nav-trips
   # Kafka-Topic2 -> crowd-nav-performance
   # StreamForword OK!
   # KafkaConnector OK!
   # SUMO-Dependency check OK!
   # Map loading OK! 
   # Nodes: 426 / Edges: 1131
   
   Retrying in 1 seconds
   Could not connect to TraCI server at localhost:63396 [Errno 61] Connection refused
   
   # SUMO-Application started OK!
   # Start adding initial cars to the simulation
   0 -> Step:100 # Driving cars: 742/750 # avgTripDuration: 0(0) # avgTripOverhead: 0
   0 -> Step:200 # Driving cars: 745/750 # avgTripDuration: 0(0) # avgTripOverhead: 0
   0 -> Step:300 # Driving cars: 745/750 # avgTripDuration: 214.888888889(26) # avgTripOverhead: 2.29300312373
   0 -> Step:400 # Driving cars: 743/750 # avgTripDuration: 263.967741935(61) # avgTripOverhead: 2.12040051211
   ```
   A program called XQuartz shows up simultaneously.
   ![xquartz](illustrations/xquartz.png)
7. Download and install dependencies with **Python 3.7+** in [RTX](https://github.com/imchell/RTX).
8. Run `python rtx.py start examples/crowdnav-sequential` in RTX folder. The terminal will prompt
   ```shell
   > Starting RTX experiment...
   ######################################
   > Workflow       | CrowdNav-Sequential
   > KafkaProducer  | JSON | URI: localhost:9092 | Topic: crowd-nav-commands
   > KafkaConsumer  | JSON | URI: localhost:9092 | Topic: crowd-nav-trips
   sequential
   > ExecStrategy   | Sequential
   >
   > IgnoreSamples  | [##############################] Target: 100 | Done: 100  
   > CollectSamples | [##############################] Target: 100 | Done: 100
   > Statistics     | 1/4 took 44796ms - remaining ~134.388sec
   > FullState      | {'count': 100, 'avg_overhead': 2.466326980805825}
   > ResultValue    | 2.466326980805825
   ```

## Configurations

1. The extension works with its default presets by simply running `python rtx.py start examples/crowdnav-evolutionary` or `python rtx.py start examples/crowdnav-sequential`.
2. Turn on / off the extension by setting `"online_learning"` to `True` of `False` in `definition.py` of the corresponding strategy you want to use. For example, in `examples/crowdnav-evolutionary/definition.py` we have already set it to `True`.
3. In `rtxlib/executionstrategy/__init__.py` you will notice that we use the `wrap_with_online_learning` function to "wrap" the original strategy execution function. In fact, this function is more powerful under the hood, and you can calibrate your experiments with its parameters.
   ```python
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
   ```
4. Theoretically you can "wrap" any strategy you want in `rtxlib/executionstrategy/__init__.py` by simply assign the strategy execution function to `strategy` parameter, but there is a precondition for that - you need to append current input parameter and the corresponding output parameter into the online learning model yourself.
   This is really easy to achieve. As mentioned in our report, `rtxlib.storage` is born to do this job. 
   ```python
   from rtxlib.storage import State
   
   # your strategy implementation ...
   
   State.opti_values.append(current_input_parameter)
   State.result_values.append(corresponding_output_parameter)
   ```
   You may head to `rtxlib/executionstrategy/EvolutionaryStrategy.py` or `rtxlib/executionstrategy/SequencialStrategy.py` for hints.
5. Edit `rtxlib/workflow.py` to add or revise online learning models, which are in the form of [River pipelines](https://riverml.xyz/0.14.0/recipes/pipelines/). You do not need to be a master of machine learning to work on editing pipelines. There are many intuitive APIs and example available on its [website](https://riverml.xyz/0.14.0/api/linear-model/LinearRegression/). It is also possible to add standardizer, scaler, and model evaluator, etc. Remember to import it in `rtxlib/executionstrategy/OnlineLearningStrategy.py` like what we have already done in the file.
   ```python
   from rtxlib.storage.PipelineLib import your_Pipeline, naive_LR, naive_KNNR, Bayesian_LR
   ```


## Evaluation

The extension combines closely with RTX, so the plots are generated as `examples/crowdnav-xxx/scatter_plot.png`, which has the same meaning with the original RTX except the version is the result of many rounds of experiments (with or without online learning depending on `online_learning` value as stated in configuration step 2).

There will also be a file named feat.json, indicating the mean (`avg`), variance (`var`), and running time (`time`) so that we can compare between different online learning models and baseline (without online learning model).
