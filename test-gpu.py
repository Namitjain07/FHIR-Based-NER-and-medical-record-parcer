import tensorflow as tf
import time

# Define a computation to stress the GPU
a = tf.random.normal([10000, 10000])
b = tf.random.normal([10000, 10000])

# Measure execution time
start = time.time()
c = tf.matmul(a, b)
end = time.time()

print("Time taken: ", end - start)
