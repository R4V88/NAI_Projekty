"""
Authors:
    Damian Brzoskowski (s18499)
    Rafał Sochacki (s20047)

Description:
    6. Iris Flower Dataset:
        The Iris Flowers Dataset involves predicting the flower species given measurements of iris flowers.
    https://machinelearningmastery.com/standard-machine-learning-datasets/

    1. Install:
        pip install tensorflow
    2. Docs/Help
        https://www.tensorflow.org/tutorials/load_data/csv
        https://www.tensorflow.org/tutorials/customization/custom_training_walkthrough
"""
import matplotlib.pyplot as plt
import tensorflow as tf

train_dataset_fp = 'data/iris.csv'
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

feature_names = column_names[:-1]
label_name = column_names[-1]

class_names = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']

batch_size = 32

train_dataset = tf.data.experimental.make_csv_dataset(
    train_dataset_fp,
    batch_size,
    column_names=column_names,
    label_name=label_name,
    header=False,
    num_epochs=1)

features, labels = next(iter(train_dataset))

plt.scatter(features['petal_length'],
            features['sepal_length'],
            c=labels,
            cmap='viridis')

plt.xlabel("Petal length")
plt.ylabel("Sepal length")
plt.show()
