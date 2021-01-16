import numpy as np
import matplotlib.pyplot as plt
import time
import concurrent.futures


def func(x: int):
    return x**2

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



numbers = np.random.uniform(size=(100000, 1))

if __name__ == "__main__":
    maximum = 20_00
    stepsize = 10
    t1_list = []
    t2_list = []
    t3_list = []
    t4_list = []
    t5_list = []
    sizes = range(stepsize, maximum, stepsize)
    for size in sizes:
        numbers = np.random.uniform(size=(size, 1))

        _, t1 = for_loop(numbers)
        t1_list.append(t1)

        _, t2 = built_in_map(numbers)
        t2_list.append(t2)

        _, t3 = np_vectorize(numbers)
        t3_list.append(t3)

        _, t4 = np_fromiter(numbers)
        t4_list.append(t4)

        # _, t5 = concurrent_futures(numbers)
        # t5_list.append(t5)

    sizes = list(sizes)
    plt.plot(sizes, t1_list, label='standard for loop')
    plt.plot(sizes, t2_list, label='built in map')
    plt.plot(sizes, t3_list, label='np.vectorize')
    plt.plot(sizes, t4_list, label='np.fromiter')
    
    # plt.yscale('log')
    # plt.xscale('log')
    plt.legend()
    plt.show()