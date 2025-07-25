import gc
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Callable, List, Tuple

from .texy import extreme_clean as _extreme_clean
from .texy import relaxed_clean as _relaxed_clean
from .texy import strict_clean as _strict_clean


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


def parallelize(
    strategy: Callable[[List[str]], List[str]], data: List[str], max_workers: int
) -> List[str]:
    """Parallelize a pipeline with Python multiprocessing and aggressive memory management."""
    if not max_workers:
        max_workers = multiprocessing.cpu_count()
    
    batch_size: int = max(len(data) // max_workers, 1)
    
    # For small datasets, don't use multiprocessing to avoid overhead
    if len(data) < max_workers * 16:  # Increased threshold
        try:
            result = strategy(data)
            return result
        finally:
            # Force multiple garbage collection cycles
            for _ in range(3):
                gc.collect()
    
    # Process data in smaller chunks to reduce memory pressure
    futures: List[Any] = []
    store: List[Any] = []
    
    try:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for i in range(0, len(data), batch_size):
                batch = data[i : i + batch_size]
                futures.append(executor.submit(_apply_strategy, strategy, batch, i))
            
            for future in as_completed(futures):
                try:
                    store.append(future.result())
                except Exception as e:
                    print(f"Error processing batch: {e}")
                    raise Exception(f"Exception occurred: {e}")
        
        # Sort and combine results
        store.sort(key=lambda x: x[0])
        result: List[str] = []
        for i in store:
            result.extend(i[1])
        
        return result
        
    finally:
        # Aggressive cleanup of intermediate data
        if 'store' in locals():
            del store
        if 'futures' in locals():
            del futures
        # Force multiple garbage collection cycles
        for _ in range(3):
            gc.collect()


def extreme_clean(data: List[str]) -> List[str]:
    """Extreme cleaning pipeline with aggressive memory management."""
    try:
        result = parallelize(_extreme_clean, data, 0)
        # Force immediate cleanup
        gc.collect()
        return result
    finally:
        # Ensure cleanup even on exceptions
        gc.collect()


def strict_clean(data: List[str]) -> List[str]:
    """Strict cleaning pipeline with aggressive memory management."""
    try:
        result = parallelize(_strict_clean, data, 0)
        # Force immediate cleanup
        gc.collect()
        return result
    finally:
        # Ensure cleanup even on exceptions
        gc.collect()


def relaxed_clean(data: List[str]) -> List[str]:
    """Relaxed cleaning pipeline with aggressive memory management."""
    try:
        result = parallelize(_relaxed_clean, data, 0)
        # Force immediate cleanup
        gc.collect()
        return result
    finally:
        # Ensure cleanup even on exceptions
        gc.collect()
