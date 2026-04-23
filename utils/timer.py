import time

def measure_time(func, args):
    start = time.time()

    result = func(args)

    end = time.time()

    print(f"\nTempo de execução: {end - start:.4f} segundos")

    return result