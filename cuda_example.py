'''
this will be an example on how to use cuda on python
'''

from numba import cuda
import numpy
import time

# print(cuda.gpus) # <- shows the cuda gpus the device has

@cuda.jit
def randomize_matrix(matrix):
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    # Block width, i.e. number of threads per block
    bw = cuda.blockDim.x
    # Compute flattened index inside the array
    pos = tx + ty * bw
    if pos < matrix.size:  # Check array boundaries
        matrix[pos] *= 2 # do the computation

# Create the data array - usually initialized some other way
data = numpy.ones(1000000)

# Set the number of threads in a block
threadsperblock = 32 

# Calculate the number of thread blocks in the grid
blockspergrid = (data.size + (threadsperblock - 1)) // threadsperblock

#------------- ONE THREAD ------------
start_time = time.time()
# Now start the kernel
randomize_matrix[1, 1](data)

# Print the result
print(data)
print(f'it took {time.time() - start_time} seconds')

#------------- MULTIPLE THREADS ------------
start_time = time.time()
# Now start the kernel
randomize_matrix[blockspergrid, threadsperblock](data)

# Print the result
print(data)
print(f'it took {time.time() - start_time} seconds')