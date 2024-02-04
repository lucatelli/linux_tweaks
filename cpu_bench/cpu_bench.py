import time
import multiprocessing

def cpu_intensive_workload(n):
    result = 0
    for _ in range(n):
        result += sum(range(10**6))
    return result

def single_core_benchmark():
    start_time = time.time()
    num_iterations = 100  
    cpu_intensive_workload(num_iterations)
    elapsed_time = time.time() - start_time
    score = int(100 / elapsed_time) 
    return score

def multi_core_benchmark():
    num_cores = multiprocessing.cpu_count()
    start_time = time.time()
    num_iterations = 1000
    processes = []

    def worker():
        cpu_intensive_workload(num_iterations)

    for _ in range(num_cores):
        process = multiprocessing.Process(target=worker)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    elapsed_time = time.time() - start_time
    score = int(num_cores * 1000 / elapsed_time)
    return score

if __name__ == "__main__":
    """
    To run:
    $ python cpu_bench.py
    """
    
    single_core_score = single_core_benchmark()
    multi_core_score = multi_core_benchmark()

    print(f"Single-core benchmark score: {single_core_score}")
    print(f"Multi-core benchmark score: {multi_core_score}")
