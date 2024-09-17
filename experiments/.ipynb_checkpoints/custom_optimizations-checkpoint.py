import psutil
import numpy as np
import dask.array as da
from dask import distributed
from dask.core import get_deps

def get_input_nodes(dsk):
    dependencies, dependents = get_deps(dsk)
    
    return [node for node, deps in dependencies.items() if not deps]

# def get_random_branch(dsk):
#     dependencies, dependents = get_deps(dsk)
#     leaf_node = [node for node, deps in dependents.items() if not deps][0]
#     leaf_node_dependencies = dependencies.get(leaf_node)

#     x = next(iter(leaf_node_dependencies))
#     print(dependencies.get(x))


def custom_optimization(dsk, keys, **kwargs):
    #return dsk
    new_dsk = dict(dsk)  # Copy the graph

    for k, v in new_dsk.items():
        # Check if the task's output is a Dask array or not
        task = v
        if isinstance(task, tuple):
            func, *args = task
            
            # Look for functions that produce arrays (e.g., da.random, da.from_array, etc.)
            if callable(func):
                # If the function produces a Dask array, rechunk it
                if 'random' in func.__name__ or 'from_array' in func.__name__:
                    new_dsk[k] = (da.rechunk, (func, *args), (500, 500))
            else:
                new_dsk[k] = v
        else:
            # Non-tuple tasks remain unchanged
            new_dsk[k] = v

    return new_dsk

    
    input_nodes = get_input_nodes(dsk)

    # Before continuing, try finding a way to rechunk and continue executing the graph in here
    # Find a way to extract all the computations (without the aggregates and partials)
    # Execute a single sample of each operation
    # Gather the memory usage of each operation
    # Based on that, calculate the estimated memory usage for all
    # With that in mind, rechunk and change the graph structure
    
    client = distributed.get_client()
    
    return dsk

# def get_memory_info():
#     """Get the memory usage (RSS) of the current process."""
#     process = psutil.Process()
#     return process.memory_info().rss

# def get_available_memory():
#     """Get available memory from all workers."""
#     client = distributed.get_client()
#     worker_memory = client.run_on_scheduler(lambda: client.run(lambda: psutil.virtual_memory().available))
#     return sum(worker_memory.values())


    #     """Custom optimization function that adjusts the chunk size dynamically."""
    # # Measure memory before execution
    # initial_memory = get_memory_info()
    
    # # Retrieve the first key in the task graph
    # first_key = next(iter(dsk))
    
    # # Extract the chunk's metadata from the task graph (assuming the key holds the chunk info)
    # first_task = dsk[first_key]
    
    # # In a Dask task, the second item in the tuple holds the array-related information
    # array_info = first_task[1]  # Get the task's arguments, including shape and dtype

    # # Extract chunk size information from the task graph
    # # Usually, this is stored as tuples of dimensions, e.g., ((1000,), (1000,))
    # if isinstance(array_info, tuple):
    #     chunk_shape = array_info[0]  # Chunk size
    #     dtype = array_info[-1]       # Dtype (if available)
    # else:
    #     raise ValueError("Unexpected task structure.")
    
    # # Estimate memory usage based on chunk size and dtype
    # element_size = np.dtype(dtype).itemsize  # Size of one element in bytes
    # num_elements_in_chunk = np.prod(chunk_shape)
    # estimated_memory_for_chunk = num_elements_in_chunk * element_size
    
    # print(f"Estimated memory for first chunk: {estimated_memory_for_chunk} bytes")
    
    # # Execute the first chunk to measure actual memory usage
    # client = distributed.get_client()
    # client.get(dsk, [first_key])  # Execute the first chunk
    
    # # Measure memory after execution
    # used_memory = get_memory_info() - initial_memory
    # print(f"Memory used by first chunk: {used_memory} bytes")
    
    # # Estimate total memory usage based on chunk usage
    # total_chunks = len(dsk)
    # expected_memory = used_memory * total_chunks
    # print(f"Estimated total memory usage: {expected_memory} bytes")
    
    # # Get available memory from all workers
    # available_memory = get_available_memory()
    # print(f"Available memory on all workers: {available_memory} bytes")
    
    # # Calculate the optimal chunk size based on available memory
    # scaling_factor = available_memory / expected_memory
    # optimal_chunk_size = int(chunk_shape[0] * scaling_factor)
    
    # print(f"Optimal chunk size: {optimal_chunk_size}")
    
    # # Repartition the array with the new chunk size (this would typically involve modifying the graph)
    # # The code here would normally repartition the Dask array based on the optimization
    # # However, we are focusing on memory estimation for now
    
    # return dsk