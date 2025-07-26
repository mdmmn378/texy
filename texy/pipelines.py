from concurrent.futures.thread import ThreadPoolExecutor
import gc
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Callable, List, Tuple

from .texy import extreme_clean as _extreme_clean
from .texy import relaxed_clean as _relaxed_clean
from .texy import strict_clean as _strict_clean
from .texy import clean_all 


def _apply_strategy(
    strategy: Callable[[List[str]], List[str]], batch: List[str], idx: int
) -> Tuple[int, List[Any]]:
    try:
        result = idx, strategy(batch)
        # Explicitly release the batch memory
        del batch
        gc.collect()
        return result
    except Exception as e:
        del batch
        gc.collect()
        raise e


def parallelize(strategy: Callable, data: List[str], max_workers: int = 0) -> List[str]:
    """
    Ultra-memory-efficient parallel processing.
    """
    if not data:
        return []
    
    # For small datasets, use direct processing to avoid multiprocessing overhead
    if len(data) < 1000:
        return strategy(data)
    
    if max_workers == 0:
        max_workers = min(4, (multiprocessing.cpu_count() or 1))  # Limit workers
    
    # Use smaller batches to reduce memory pressure
    batch_size = max(100, len(data) // (max_workers * 4))
    
    # Force cleanup before processing
    for _ in range(3):
        gc.collect()
    
    # Process data in smaller chunks to reduce memory pressure
    futures: List[Any] = []
    store: List[Any] = []
    
    try:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit batches
            for i in range(0, len(data), batch_size):
                batch = data[i : i + batch_size]
                futures.append(executor.submit(_apply_strategy, strategy, batch, i))
            
            # Process results immediately to reduce memory buildup
            for future in as_completed(futures):
                try:
                    result = future.result()
                    store.append(result)
                    # Force cleanup after each result
                    del result
                    gc.collect()
                except Exception as e:
                    print(f"Error processing batch: {e}")
                    raise Exception(f"Exception occurred: {e}")
                    
    except Exception as e:
        raise e
    finally:
        # Aggressive cleanup
        for _ in range(5):
            gc.collect()
    
    # Sort results by batch index and flatten
    store.sort(key=lambda x: x[0])  # Sort by batch index
    result = []
    for _, data_batch in store:
        result.extend(data_batch)
    
    # Final cleanup
    del store
    gc.collect()
    
    return result


def extreme_clean(data: List[str]) -> List[str]:
    """Extreme cleaning pipeline with aggressive memory management."""
    try:
        result = parallelize(_extreme_clean, data, 0)
        # result = _extreme_clean(data)
        # Force immediate cleanup
        gc.collect()
        # clean_all()
        return result
    finally:
        # Ensure cleanup even on exceptions
        gc.collect()


def strict_clean(data: List[str]) -> List[str]:
    """Strict cleaning pipeline with aggressive memory management."""
    try:
        result = parallelize(_strict_clean, data, 0)
        # result = _strict_clean(data)
        # Force immediate cleanup
        gc.collect()
        # clean_all()
        return result
    finally:
        # Ensure cleanup even on exceptions
        gc.collect()


def relaxed_clean(data: List[str]) -> List[str]:
    """Relaxed cleaning pipeline with aggressive memory management."""
    try:
        result = parallelize(_relaxed_clean, data, 0)
        # result = _relaxed_clean(data)
        # Force immediate cleanup
        gc.collect()
        # clean_all() 
        return result
    finally:
        # Ensure cleanup even on exceptions
        gc.collect()
