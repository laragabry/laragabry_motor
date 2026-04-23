def bubble_sort(arr, key=None, reverse=False):
    arr = list(arr)
    n = len(arr)
    cmp = 0 

    get = key if key else lambda x: x

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            cmp += 1

            a = get(arr[j])
            b = get(arr[j + 1])
            if (a > b) if not reverse else (a < b):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

    return arr, cmp
def merge_sort(arr, key=None, reverse=False):
    arr = list(arr)
    cmp_count = [0]

    get = key if key else lambda x: x
    def merge(left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            cmp_count[0] += 1

            a = get(left[i])
            b = get(right[j])

            if (a <= b) if not reverse else (a >= b):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])

        return result
    def _sort(lst):
        if len(lst) <= 1:
            return lst

        mid = len(lst) // 2

        left = _sort(lst[:mid])
        right = _sort(lst[mid:])

        return merge(left, right)

    sorted_arr = _sort(arr)

    return sorted_arr, cmp_count[0]
def benchmark_sorts(arr, key=None, reverse=False):
    import time
    t0 = time.time()
    arr_b, cmp_b = bubble_sort(arr, key=key, reverse=reverse) 
    t_bubble = time.time() - t0

    t0 = time.time()
    arr_m, cmp_m = merge_sort(arr, key=key, reverse=reverse)
    t_merge = time.time() - t0

    return {
        "n": len(arr),
        "bubble": {
            "time_s": round(t_bubble, 6),
            "comparisons": cmp_b
        },
        "merge": {
            "time_s": round(t_merge, 6),
            "comparisons": cmp_m
        },
    }