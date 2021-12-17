"""
Authors:
    Damian Brzoskowski (s18499)
    Rafał Sochacki (s20047)

Description:
    Animal Recognition based on CIFAR-10

    1. Install:
        pip install tensorflow
        pip install numpy (if not installed with tensorflow)
    2. Docs/Help
        https://www.tensorflow.org/tutorials/images/cnn
        https://www.tensorflow.org/tutorials/images/classification
        https://www.tensorflow.org/tutorials/images/transfer_learning
"""


import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import models

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle', 'boot'
]

train_images, test_images = train_images / 255.0, test_images / 255.0

plt.figure(figsize=(10, 10))

for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()


model = models.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10)
])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

model.summary()
history = model.fit(train_images, train_labels, epochs=10)

loss = history.history['loss']
acc = history.history['accuracy']

epochs_range = range(10)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.legend(loc='lower right')
plt.title('Training Loss and Accuracy')

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

predictions = probability_model.predict(test_images)

np.argmax(predictions[0])


def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img)
    predicted_label = np.argmax(predictions_array)

    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'
    plt.xlabel("{} {:2.0f}% ({})".format(
        class_names[predicted_label],
        100 * np.max(predictions_array),
        class_names[true_label]),
        color=color
    )


def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    plot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    plot[predicted_label].set_color('red')
    plot[true_label].set_color('blue')


first_element = 0  # Show element 0

plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(first_element, predictions[first_element], test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(first_element, predictions[first_element],  test_labels)
plt.show()

num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plt.figure(figsize=(10, 10))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
    plot_value_array(i, predictions[i], test_labels)
    plt.tight_layout()
plt.show()
