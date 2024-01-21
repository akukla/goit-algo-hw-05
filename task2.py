import numpy as np

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    iterations = 0

    while low <= high:
        mid = (low + high) // 2
        iterations += 1

        if arr[mid] < target:
            low = mid + 1
        elif arr[mid] > target:
            high = mid - 1
        else:
            return iterations, arr[mid]

    if high >= 0:
        return iterations, arr[high]
    else:
        return iterations, None


print(binary_search(np.array([1, 2, 3, 4, 5])/10, 3/10))
print(binary_search(np.array([1, 2, 3, 4, 5])/10, 4/10))
print(binary_search(np.array([1, 2, 3, 4, 5, 6, 7, 8, 12, 20, 25])/10, 20/10))
