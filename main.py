import numpy as np
import matplotlib.pyplot as plt
import time
import concurrent.futures


def func(x: int):
    return x*x

def timer(func):
    def wrapper(*args):
        start = time.time() 
        res = func(*args)
        end = time.time()
        return res, end - start
    return wrapper

@timer
def for_loop(numbers):
    res = []
    for number in numbers:
        res.append(func(number))
    return res

@timer
def built_in_map(numbers):
    return list(map(func, numbers))

@timer
def np_vectorize(numbers):
    func_vec = np.vectorize(func)
    return func_vec(numbers)

@timer
def np_fromiter(numbers):
    iter = [func(number) for number in numbers]
    return np.fromiter(iter, float)

# @timer
# def concurrent_futures(numbers):
#     with concurrent.futures.ProcessPoolExecutor(2) as executor: 
#         res_iter = executor.map(func, numbers)
#         print('lol')
#         return list(res_iter)



mappings = [for_loop, built_in_map, np_vectorize, np_fromiter]
labels = ['for_loop', 'built_in_map', 'np_vectorize', 'np_fromiter']

numbers = np.random.uniform(size=(100000, 1))

if __name__ == "__main__":
    maximum = 5_000
    stepsize = 10
    t_lists = [[] for mapping in mappings]
    sizes = range(stepsize, maximum, stepsize)
    for size in sizes:
        numbers = np.random.uniform(size=(size, 1))
        for i, mapping in enumerate(mappings):
            _, t = mapping(numbers)
            t_lists[i].append(t)

    sizes = list(sizes)
    for i, t_list in enumerate(t_lists):
        plt.plot(sizes, t_list, label=labels[i])
    plt.legend()
    plt.xlabel("array lengths")
    plt.ylabel("seconds")
    plt.show()