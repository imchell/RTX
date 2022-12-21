from river import compose, tree, linear_model, neural_net, optim

naive_SGTR = compose.Pipeline(
    ('tree', tree.SGTRegressor())
)

naive_LR = compose.Pipeline(
    ('lr', linear_model.LinearRegression())
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
