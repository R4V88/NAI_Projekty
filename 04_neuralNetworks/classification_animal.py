"""
Authors:
    Damian Brzoskowski (s18499)
    Rafał Sochacki (s20047)

Description:
    Animal Recognition based on CIFAR-10

    1. Install:
        pip install tensorflow
    2. Docs/Help
        https://www.tensorflow.org/tutorials/images/cnn
"""


# Resolve problem with SSL certificate
# https://programmerah.com/python-error-certificate-verify-failed-certificate-has-expired-40374/
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np


(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()


# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0


def return_animals(images, labels):
    """
        Filter animals by class_name label
        {
            'airplane': 0,
            'automobile': 1,
            'bird': 2,
            'cat': 3,
            'deer': 4,
            'dog': 5,
            'frog': 6,
            'horse': 7,
            'ship': 8,
            'truck': 9
        }
        omits these:
        {
            'airplane': 0,
            'automobile': 1,
            'ship': 8,
            'truck': 9
        }
        2 separated lists:
        return: animal_images <list>, animals_label <list>
    """
    images = np.array([
        images[i] for i in range(len(labels)) if
        labels[i][0] not in [0, 1, 8, 9]
    ])
    labels = np.array([
        labels[i][0] for i in range(len(labels)) if
        labels[i][0] not in [0, 1, 8, 9]
    ])
    return images, labels


ow = {
    'airplane': 0,
    'automobile': 1,
    'bird': 2,
    'cat': 3,
    'deer': 4,
    'dog': 5,
    'frog': 6,
    'horse': 7,
    'ship': 8,
    'truck': 9
 }

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

plt.figure(figsize=(10, 10))

train_animals_images, train_animals_labels = return_animals(train_images, train_labels)

for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_animals_images[i])
    # The CIFAR labels happen to be arrays,
    # which is why you need the extra index
    plt.xlabel(class_names[train_animals_labels[i]])
plt.show()


model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.summary()

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))
model.summary()


model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

test_animal_images, test_animal_labels = return_animals(test_images, test_labels)

history = model.fit(train_animals_images, train_animals_labels, epochs=10,
                    validation_data=(test_animal_images, test_animal_labels))


plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print(test_acc)
