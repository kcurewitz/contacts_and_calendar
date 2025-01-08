# Welcome to Juno!
# 
# Here, we tackle the same Iris classification problem that we explore in the introductory Jupyter notebook.
# We start by loading a sample dataset, and then proceed to build and train a classifier model utilizing a multi-layer neural network — all executed locally on your device!

import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn import metrics

def pretty_format(text, color=None, font_weight=None):
    """
    Formats text with specified color and font weight using ANSI escape sequences.
    """
    colors = {
        'green': '\033[32m',
        'red': '\033[31m',
        'blue': '\033[34m',
        'gray': '\033[90m'
    }
    weights = {
        'bold': '\033[1m',
        'italic': '\033[3m'
    }
    reset = '\033[0m'
    color_code = colors.get(color, '')
    weight_code = weights.get(font_weight, '')
    return f"{weight_code}{color_code}{text}{reset}"

if __name__ == '__main__':
    # The dataset is stored in the `iris.csv` file located in Juno's on-device storage, in the `/Documents/welcome-data` folder.
    Boolean = input("type True or False: ")
    if Boolean == "True":
        print(pretty_format(Boolean,'blue', 'italic'))
    else:
        print(pretty_format(Boolean,'green', 'bold'))
    print(pretty_format('Dataset', font_weight='bold'))
    print('Reading from ' + pretty_format('iris.csv', 'gray', 'italic') + ' file on disk...')
    df = pd.read_csv("welcome-data/iris.csv")
    print('Data loaded successfully.')
    print('\n')

    # All unique Iris species from the data set
    species = pd.unique(df['Species'].sort_values())
    # List of measured features in the data set
    features = ['Sepal length (cm)', 'Sepal width (cm)', 'Petal length (cm)', 'Petal width (cm)']
    # Number of samples for each species
    counts = df['Species'].value_counts().sort_index()
    print(pretty_format('Sample counts', font_weight='bold'))
    for species, count in counts.items():
        print(pretty_format(f'  {species}', font_weight='italic') + ': ' + pretty_format(f'{count}', font_weight='bold') + ' samples')
    print('\n')

    # Scale features and encode data labels
    feature_scaler = StandardScaler()
    X = feature_scaler.fit_transform(df[features].values)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['Species'])
    
    # Allocate 30% of original dataset to test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print(pretty_format('Data split', font_weight='bold'))
    print(pretty_format('  Training', font_weight='italic') + ' set: ' + pretty_format(f'{len(X_train)}', font_weight='bold') + ' samples')
    print(pretty_format('  Test', font_weight='italic') + ' set: ' + pretty_format(f'{len(X_test)}', font_weight='bold') + ' samples')
    print('\n')

    # Training and hyperparameters
    solver = 'sgd' # Use stochastic gradient descent as optimization method
    max_iter = 500
    learning_rate_init = 0.1
    hidden_layer_sizes = (5, 3)
    random_state = 42
    model = MLPClassifier(solver=solver, max_iter=max_iter, learning_rate_init=learning_rate_init, hidden_layer_sizes=hidden_layer_sizes, random_state=random_state)
    print(pretty_format('Hyperparameters and architecture', font_weight='bold'))
    print('  Solver: ' + pretty_format(f'{solver}', font_weight='bold'))
    print('  Max iterations: ' + pretty_format(f'{max_iter}', font_weight='bold'))
    print('  Initial learning rate: ' + pretty_format(f'{learning_rate_init}', font_weight='bold'))
    print('  Hidden layers: ' + pretty_format(f'{hidden_layer_sizes}', font_weight='bold'))
    print('\n')

    # Fit the classifier model
    model.fit(X_train, y_train)
    print(pretty_format('Training', font_weight='bold'))
    print('Completed after ' + pretty_format(f'{model.n_iter_}', font_weight='bold') + ' iterations.')
    print('  Training loss: ' + pretty_format(f'{model.loss_:.4f}', color='green', font_weight='bold'))
    print('  Test set accuracy: ' + pretty_format(f'{metrics.accuracy_score(model.predict(X_test), y_test):.4f}', color='green', font_weight='bold'))
