#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 10:12:49 2021

@author: raghhav
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
# import mitdeeplearning as mdl

## 1.1 Why is TensorFlow called TensorFlow?

# TensorFlow is called 'TensorFlow' because it handles the flow 
# (node/mathematical operation) of Tensors, which are data structures 
# that you can think of as multi-dimensional arrays. Tensors are represented 
# as n-dimensional arrays of base dataypes such as a string or integer 
# -- they provide a way to generalize vectors and matrices to higher dimensions.

# The ```shape``` of a Tensor defines its number of dimensions and the size of each dimension. The ```rank``` of a Tensor provides the number of dimensions (n-dimensions) -- you can also think of this as the Tensor's order or degree.

# Let's first look at 0-d Tensors, of which a scalar is an example:
sport = tf.constant("Tennis",tf.string)
number = tf.constant(1.413443222,tf.float64)

print("sport is {}-d Tensor".format(tf.rank(sport).numpy()))
print("number is {}-d Tensor".format(tf.rank(number).numpy()))

# Vectors and lists can be used to create 1-d Tensors:

sports = tf.constant(["Tennis", "Basketball"], tf.string)
numbers = tf.constant([3.141592, 1.414213, 2.71821], tf.float64)

print("`sports` is a {}-d Tensor with shape: {}".format(tf.rank(sports).numpy(), tf.shape(sports)))
print("`numbers` is a {}-d Tensor with shape: {}".format(tf.rank(numbers).numpy(), tf.shape(numbers)))

# Next we consider creating 2-d (i.e., matrices) and higher-rank Tensors. 
# For examples, in future labs involving image processing and computer vision, 
# we will use 4-d Tensors. Here the dimensions correspond to 
# 1)the number of example images in our batch, 
# 2)image height, 
# 3)image width, and 
# 4)the number of color channels.

### Defining higher-order Tensors ###

'''TODO: Define a 2-d Tensor'''
matrix = tf.constant([[1,2],[3,4]],tf.int16)

assert isinstance(matrix, tf.Tensor), "matrix must be a tf Tensor object"
assert tf.rank(matrix).numpy() == 2
print("Rank of matrix is {}".format(tf.rank(matrix).numpy()))

'''TODO: Define a 4-d Tensor.'''
# Use tf.zeros to initialize a 4-d Tensor of zeros with size 10 x 256 x 256 x 3. 
#   You can think of this as 10 images where each image is RGB 256 x 256.
images = tf.zeros([10,256,256,3],tf.int32)

assert isinstance(images, tf.Tensor), "matrix must be a tf Tensor object"
assert tf.rank(images).numpy() == 4, "matrix must be of rank 4"
assert tf.shape(images).numpy().tolist() == [10, 256, 256, 3], "matrix is incorrect shape"
print("rank of images matrix is {}".format(tf.rank(images).numpy()))

# As you have seen, the ```shape``` of a Tensor provides the number of 
# elements in each Tensor dimension. The ```shape``` is quite useful, and 
# we'll use it often. You can also use slicing to access subtensors within 
# a higher-rank Tensor:

row_vector = matrix[1]
column_vector = matrix[:,1]
scalar = matrix[1, 1]

print("`row_vector`: {}".format(row_vector.numpy()))
print("`column_vector`: {}".format(column_vector.numpy()))
print("`scalar`: {}".format(scalar.numpy()))



## 1.2 Computations on Tensors

# A convenient way to think about and visualize computations in TensorFlow 
# is in terms of graphs. We can define this graph in terms of Tensors, 
# which hold data, and the mathematical operations that act on these Tensors 
# in some order. Let's look at a simple example, and define this 
# computation using TensorFlow:

# Create nodes in the graph
a = tf.constant(10)
b = tf.constant(15)

c1 = tf.add(a,b)
c2 = a + b      #Tensorflow overrides + operation so that it is 
                # is able to act on Tensors
print(c1)
print(c2)

### Defining Tensor computations ###

# Construct a simple computation function
def func(a,b):
  '''TODO: Define the operation for c, d, e (use tf.add, tf.subtract, tf.multiply).'''
  c = tf.add(a,b)
  d = tf.subtract(b,1)
  e = tf.multiply(c, d)
  return e

print(func(a,b))

## 1.3 Neural networks in TensorFlow
# We can also define neural networks in TensorFlow. 
# TensorFlow uses a high-level API called [Keras]
# (https://www.tensorflow.org/guide/keras) that provides a powerful, 
# intuitive framework for building and training deep learning models.

# Let's first consider the example of a simple perceptron defined by 
# just one dense layer: $ y = \sigma(Wx + b)$, where $W$ represents 
# a matrix of weights, $b$ is a bias, $x$ is the input, $\sigma$ is 
# the sigmoid activation function, and $y$ is the output. We can also 
# visualize this operation using a graph: 


# Tensors can flow through abstract types called 
# [```Layers```](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Layer)
#  -- the building blocks of neural networks. ```Layers``` implement common 
#  neural networks operations, and are used to update weights, compute losses,
#  and define inter-layer connectivity. 
 
#  We will first define a ```Layer``` to implement the simple perceptron 
#  defined above.

### Defining a neural network using the Sequential API ###

# Import relevant packages
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

# Define the number of outputs
n_output_nodes = 3

# First define the model 
model = Sequential()

'''TODO: Define a dense (fully connected) layer to compute z'''
# Remember: dense layers are defined by the parameters W and b!
# You can read more about the initialization of W and b in the TF documentation :) 
# https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense?version=stable
dense_layer = Dense(3,use_bias=True,
                    kernel_initializer='glorot_uniform',
                    bias_initializer='zeros',
                    activation='relu')

# Add the dense layer to the model
model.add(dense_layer)

# Test model with example input
x_input = tf.constant([[1,2.]], shape=(1,2))

'''TODO: feed input into the model and predict the output!'''
model_output = model(x_input).numpy()
print(model_output)


# In addition to defining models using the `Sequential` API, we can also 
# define neural networks by directly subclassing the [`Model`]
# (https://www.tensorflow.org/api_docs/python/tf/keras/Model?version=stable)
#  class, which groups layers together to enable model training and inference.
#  The `Model` class captures what we refer to as a "model" or as a "network".
#  Using Subclassing, we can create a class for our model, and then define 
#  the forward pass through the network using the `call` function. 
 
#  Subclassing affords the flexibility to define custom layers, 
#  custom training loops, custom activation functions, and custom models. 
#  Let's define the same neural network as above now using Subclassing rather
#  than the `Sequential` model.

### Defining a model using subclassing ###

from tensorflow.keras import Model
from tensorflow.keras.layers import Dense

class SubclassModel(tf.keras.Model):

  # In __init__, we define the Model's layers
  def __init__(self, n_output_nodes):
    super(SubclassModel, self).__init__()
    '''TODO: Our model consists of a single Dense layer. Define this layer.''' 
    self.dense_layer = Dense(units=n_output_nodes,
                             activation='sigmoid',
                             )

  # In the call function, we define the Model's forward pass.
  def call(self, inputs):
    return self.dense_layer(inputs)

n_output_nodes = 3
model = SubclassModel(n_output_nodes)

x_input = tf.constant([[1,2.]], shape=(1,2))

print(model.call(x_input))

# Importantly, Subclassing affords us a lot of flexibility to 
# define custom models. For example, we can use boolean arguments in 
# the `call` function to specify different network behaviors, 
# for example different behaviors during training and inference. 
# Let's suppose under some instances we want our network to simply 
# output the input, without any perturbation. We define a boolean 
# argument `isidentity` to control this behavior:
    
### Defining a model using subclassing and specifying custom behavior ###

from tensorflow.keras import Model
from tensorflow.keras.layers import Dense

class IdentityModel(tf.keras.Model):

  # As before, in __init__ we define the Model's layers
  # Since our desired behavior involves the forward pass, this part is unchanged
  def __init__(self, n_output_nodes):
    super(IdentityModel, self).__init__()
    self.dense_layer = tf.keras.layers.Dense(n_output_nodes, activation='sigmoid')

  '''TODO: Implement the behavior where the network outputs the input, unchanged, 
      under control of the isidentity argument.'''
  def call(self, inputs, isidentity=False):
    x = self.dense_layer(inputs)
    '''TODO: Implement identity behavior'''
    if (isidentity == True):
      return inputs
    else:
      return x

n_output_nodes = 3
model = IdentityModel(n_output_nodes)

x_input = tf.constant([[1,2.]], shape=(1,2))
'''TODO: pass the input into the model and call with and without the input identity option.'''
out_activate = model.call(x_input)
out_identity = model.call(x_input,True)

print("Network output with activation: {}; network identity output: {}".format(out_activate.numpy(), out_identity.numpy()))

## 1.4 Automatic differentiation in TensorFlow

# [Automatic differentiation](https://en.wikipedia.org/wiki/Automatic_differentiation)
# is one of the most important parts of TensorFlow and is the backbone 
# of training with [backpropagation]
# (https://en.wikipedia.org/wiki/Backpropagation). 
# We will use the TensorFlow GradientTape [`tf.GradientTape`]
# (https://www.tensorflow.org/api_docs/python/tf/GradientTape?version=stable) 
# to trace operations for computing gradients later. 

# When a forward pass is made through the network, all forward-pass 
# operations get recorded to a "tape"; then, to compute the gradient, 
# the tape is played backwards. By default, the tape is discarded after 
# it is played backwards; this means that a particular `tf.GradientTape` 
# can only compute one gradient, and subsequent calls throw a runtime error.
#  However, we can compute multiple gradients over the same computation 
#  by creating a ```persistent``` gradient tape. 

# First, we will look at how we can compute gradients using GradientTape 
# and access them for computation. We define the simple function 
# $ y = x^2$ and compute the gradient:
    
### Gradient computation with GradientTape ###

# y = x^2
# Example: x = 3.0
x = tf.Variable(3.0)

# Initiate the gradient tape
with tf.GradientTape() as tape:
  # Define the function
  y = x * x
# Access the gradient -- derivative of y with respect to x
dy_dx = tape.gradient(y, x)

assert dy_dx.numpy() == 6.0
print((dy_dx).numpy())

# In training neural networks, we use differentiation and 
# stochastic gradient descent (SGD) to optimize a loss function. 
# Now that we have a sense of how `GradientTape` can be used to compute
#  and access derivatives, we will look at an example where we use automatic
#  differentiation and SGD to find the minimum of L=(x-x_f)^2. Here x_f is a
#  variable for a desired value we are trying to optimize for; L represents 
#  a loss that we are trying to  minimize. While we can clearly solve this 
#  problem analytically (x_{min}=x_f), considering how we can compute 
#  this using `GradientTape` sets us up nicely for future labs where 
#  we use gradient descent to optimize entire neural network losses.




## Function minimization with automatic differentiation and SGD ###

# Initialize a random value for our initial x
x = tf.Variable([tf.random.normal([1])])
print("Initializing x={}".format(x.numpy()))

learning_rate = 1e-2 # learning rate for SGD
history = []
# Define the target value
x_f = 4

# We will run SGD for a number of iterations. At each iteration, we compute the loss, 
#   compute the derivative of the loss with respect to x, and perform the SGD update.
for i in range(500):
  with tf.GradientTape() as tape:
    '''TODO: define the loss as described above'''
    loss = (x - x_f)** 2

  # loss minimization using gradient tape
  grad = tape.gradient(loss, x) # compute the derivative of the loss with respect to x
  new_x = x - learning_rate*grad # sgd update
  x.assign(new_x) # update the value of x
  history.append(x.numpy()[0])

# Plot the evolution of x as we optimize towards x_f!
plt.plot(history)
plt.plot([0, 500],[x_f,x_f])
plt.legend(('Predicted', 'True'))
plt.xlabel('Iteration')
plt.ylabel('x value')