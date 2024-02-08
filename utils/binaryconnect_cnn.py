# -*- coding: utf-8 -*-
"""BinaryConnect_CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZXRgdmYMF0ZZd0n__8F0EJfTvuiXhY-0
"""

import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import time
import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras import initializers
from tensorflow.keras import backend as K
from __future__ import print_function

import sys
import os
import time
import tensorflow as tf
from tensorflow.keras.layers import Input, Dropout, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError, Hinge
from tensorflow.keras.metrics import Mean, SparseCategoricalAccuracy
import numpy as np
fashion_mnist = tf.keras.datasets.fashion_mnist
import pandas as pd
from tensorflow.keras.layers import Input, Dropout, Flatten
from tensorflow.keras.models import Model

import numpy as np
np.random.seed(1234)  # for reproducibility

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from sklearn.utils import shuffle

from collections import OrderedDict

class BinaryConv2DLayer(Layer):
    def _init_(self, filters, kernel_size, binary=True, stochastic=True, H=1.0, W_LR_scale="Glorot", **kwargs):
        super(BinaryConv2DLayer, self)._init_(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.binary = binary
        self.stochastic = stochastic
        self.H = H
        self.W_LR_scale = W_LR_scale
        seed_value = 42  # You can use any desired seed value
        self.rng = tf.random.Generator.from_seed(seed_value)
    def build(self, input_shape):
        self.kernel = self.add_weight(
            name='kernel',
            shape=(self.kernel_size[0], self.kernel_size[1], input_shape[-1], self.filters),
            initializer='glorot_uniform',
            trainable=True
        )
        super(BinaryConv2DLayer, self).build(input_shape)

    def call(self, inputs, training=None, **kwargs):

        # Use the generator for other random operations as needed
        rand_int = self.rng.uniform(shape=(), minval=1, maxval=2147462579, dtype=tf.int32)

        Wb = binarization(self.kernel, self.H, self.binary, not training, seed = rand_int)
        Wr = self.kernel
        self.kernel = Wb
        output = tf.nn.conv2d(inputs, Wb, strides=[1, 1, 1, 1], padding='SAME')
        self.kernel = Wr
        return output