def binary_search(arr, target, key=None):
    
    get = key if key else lambda x: x
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        val = get(arr[mid])  

        if val == target:
            return mid    
        elif val < target:
            left = mid + 1     
        else:
            right = mid - 1     

    return -1                

def binary_search_range(arr, lo, hi, key=None):
    

    get = key if key else lambda x: x
    left, right = 0, len(arr)

    while left < right:
        mid = (left + right) // 2

        if get(arr[mid]) < lo:
            left = mid + 1
        else:
            right = mid

    start = left
    left, right = 0, len(arr)

    while left < right:
        mid = (left + right) // 2

        if get(arr[mid]) <= hi:
            left = mid + 1
        else:
            right = mid

    end = left
    return arr[start:end]

def _build_failure(pattern):
    

    m = len(pattern)
    fail = [0] * m

    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = fail[j - 1]
        if pattern[i] == pattern[j]:
            j += 1

        fail[i] = j

    return fail


def kmp_search(text, pattern):
    

    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return []
    fail = _build_failure(pattern)

    result = []
    j = 0 
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = fail[j - 1]

        if text[i] == pattern[j]:
            j += 1
        if j == m:
            result.append(i - m + 1)
            j = fail[j - 1]

    return result


def kmp_count(text, pattern):
    
    return len(kmp_search(text, pattern))