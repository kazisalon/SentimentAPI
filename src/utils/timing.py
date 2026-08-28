import time
import asyncio
from functools import wraps
from typing import Callable, Any

def log_inference_time(func: Callable) -> Callable:

    """
    A decorator that measures and print the execution time of a 
    for both sync and async function
    """
    if asyncio.iscoroutinefunction(func):
           @wraps(func)
           async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                
                start_time = time.perf_counter()
                result = await func(*args, **kwargs)
                end_time = time.perf_counter()
        
                print(f"[TIMING] '{func.__name__}' executed in {end_time - start_time: .4f} seconds")
                return result
           return async_wrapper
        
    else:
         @wraps(func)
         def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
              start_time = time.perf_counter()
              result = func(*args, **kwargs)
              end_time = time.perf_counter()
              print(f"[TIMING] '{func.__name__}' executed in {end_time - start_time: 4f} seconds")
              return result
    return sync_wrapper
                  

        

    
    

