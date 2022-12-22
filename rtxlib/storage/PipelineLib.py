from river import compose, tree, linear_model, neural_net, optim, neighbors

"""
Please note that all models here are usable but not calibrated.
LinearRegression, BayesianLinearRegression, KNNRegressor are recommended.
Refer to https://riverml.xyz/0.14.0/api/overview/ to find out more about composing the machine learning pipeline, 
and it's very intuitive. 
"""


naive_LR = compose.Pipeline(
    ('lr', linear_model.LinearRegression())
)

Bayesian_LR = compose.Pipeline(
    ('lr', linear_model.BayesianLinearRegression())
)

naive_KNNR = compose.Pipeline(
    ('knn', neighbors.KNNRegressor())
)

naive_SGTR = compose.Pipeline(
    ('tree', tree.SGTRegressor())
)

naive_NN = compose.Pipeline(
    ('nn', neural_net.MLPRegressor(
        hidden_dims=(5,),
        activations=(
            neural_net.activations.ReLU,
            neural_net.activations.ReLU,
            neural_net.activations.Identity
        ),
        optimizer=optim.SGD(1e-3),
        seed=42
    ))
)
