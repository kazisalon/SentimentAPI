import time
from functools import wraps
from typing import Callable, Any

def log_inference_time(func: Callable) -> Callable:

    """
    A decorator that measures and print the execution time of a 
    funtions 
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        print(f"[TIMING] '{func.__name__}' executed in {execution_time: .4f} seconds")
        return result
    return wrapper
    

