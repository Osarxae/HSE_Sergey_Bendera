import random
import time

def generate_sorted_array(array_size=5, min_val=10, max_val=250_000_000):

    arr = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr.sort()
    return arr

def generate_random_numbers(array_size=10, min_val=0, max_val=100):

   return [random.randint(min_val, max_val) for _ in range(array_size)]

def linear_search(arr, target):

    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def binary_search(arr, target):

    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def search_and_time(arr, search_func):

    sorted_arr = sorted(arr.copy())
    start_time = time.time()
    for num in sorted_arr:
        search_func(sorted_arr, num)
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":

    sorted_array = generate_sorted_array()
    random_numbers = generate_random_numbers()
    print(f"Sorted array: {sorted_array}")
    print(f"Random numbers: {random_numbers}")

    linear_search_time = search_and_time(random_numbers, linear_search)
    binary_search_time = search_and_time(random_numbers, binary_search)
    print(f"Time taken for linear search: {linear_search_time:.6f} seconds")
    print(f"Time taken for binary search: {binary_search_time:.6f} seconds")

