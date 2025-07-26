import gc
import threading
import weakref
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List, Tuple, Optional, Generator
import time

from .texy import extreme_clean as _extreme_clean
from .texy import relaxed_clean as _relaxed_clean
from .texy import strict_clean as _strict_clean


class MemoryEfficientThreadPool:
    """
    Thread pool with aggressive memory management for text processing.
    
    Features:
    - Immediate result processing to avoid accumulation
    - Per-thread garbage collection
    - Memory monitoring and cleanup
    - Streaming results to reduce peak memory
    """
    
    def __init__(self, max_workers: Optional[int] = None, batch_size: Optional[int] = None):
        self.max_workers = max_workers or min(4, threading.active_count() * 2)
        self.batch_size = batch_size
        self._executor = None
        self._memory_tracker = weakref.WeakSet()
        
    def __enter__(self):
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._executor:
            self._executor.shutdown(wait=True)
            # Force cleanup after shutdown
            self._aggressive_cleanup()
    
    def _aggressive_cleanup(self):
        """Perform aggressive garbage collection."""
        for _ in range(3):
            collected = gc.collect()
            if collected == 0:
                break
            time.sleep(0.01)  # Small delay to allow cleanup
    
    def _calculate_optimal_batch_size(self, data_size: int) -> int:
        """Calculate optimal batch size based on data size and workers."""
        if self.batch_size:
            return self.batch_size
            
        # Dynamic batch sizing based on data size
        if data_size < 1000:
            return data_size  # Process all at once for small datasets
        elif data_size < 10000:
            return max(100, data_size // self.max_workers)
        elif data_size < 100000:
            return max(500, data_size // (self.max_workers * 2))
        else:
            # For large datasets, use smaller batches to reduce memory pressure
            return max(1000, min(5000, data_size // (self.max_workers * 4)))
    
    def process_streaming(
        self, 
        strategy: Callable[[List[str]], List[str]], 
        data: List[str]
    ) -> Generator[str, None, None]:
        """
        Process data in batches and yield results immediately to minimize memory usage.
        
        This streaming approach prevents accumulation of large result sets in memory.
        """
        if not data:
            return
            
        batch_size = self._calculate_optimal_batch_size(len(data))
        
        # Pre-cleanup
        self._aggressive_cleanup()
        
        try:
            # Submit all batches
            futures = []
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                future = self._executor.submit(self._process_batch_with_cleanup, strategy, batch, i)
                futures.append(future)
            
            # Process results as they complete (streaming)
            for future in as_completed(futures):
                try:
                    batch_idx, results = future.result()
                    
                    # Yield results immediately to avoid accumulation
                    for result in results:
                        yield result
                    
                    # Immediate cleanup after processing each batch
                    del results
                    self._aggressive_cleanup()
                    
                except Exception as e:
                    print(f"Error processing batch: {e}")
                    raise
                    
        finally:
            # Final aggressive cleanup
            del futures
            self._aggressive_cleanup()
    
    def process_batch_collected(
        self, 
        strategy: Callable[[List[str]], List[str]], 
        data: List[str]
    ) -> List[str]:
        """
        Process data and collect all results, but with memory optimization.
        
        Uses streaming internally but collects results for compatibility.
        """
        results = list(self.process_streaming(strategy, data))
        self._aggressive_cleanup()
        return results
    
    @staticmethod
    def _process_batch_with_cleanup(
        strategy: Callable[[List[str]], List[str]], 
        batch: List[str], 
        batch_idx: int
    ) -> Tuple[int, List[str]]:
        """
        Process a batch with immediate cleanup.
        
        This runs in a worker thread and includes thread-local cleanup.
        """
        try:
            # Process the batch
            result = strategy(batch)
            
            # Immediate cleanup of input batch
            del batch
            
            # Thread-local garbage collection
            gc.collect()
            
            return batch_idx, result
            
        except Exception as e:
            # Cleanup on error
            if 'batch' in locals():
                del batch
            gc.collect()
            raise e


def _create_memory_efficient_processor(strategy: Callable) -> Callable:
    """Create a memory-efficient processor for a cleaning strategy."""
    
    def processor(data: List[str], max_workers: Optional[int] = None, 
                 streaming: bool = False) -> List[str]:
        """
        Process data with memory-efficient threading.
        
        Args:
            data: List of strings to process
            max_workers: Number of worker threads (auto-calculated if None)
            streaming: If True, uses streaming mode for lower memory usage
        
        Returns:
            List of processed strings
        """
        if not data:
            return []
        
        # For very small datasets, use direct processing
        if len(data) < 100:
            try:
                result = strategy(data)
                gc.collect()
                return result
            finally:
                gc.collect()
        
        # Use memory-efficient thread pool
        with MemoryEfficientThreadPool(max_workers=max_workers) as pool:
            if streaming:
                # Streaming mode - lowest memory usage
                return list(pool.process_streaming(strategy, data))
            else:
                # Batch mode - better for compatibility
                return pool.process_batch_collected(strategy, data)
    
    return processor


# Create memory-efficient versions of the cleaning functions
def extreme_clean_efficient(data: List[str], max_workers: Optional[int] = None, 
                           streaming: bool = False) -> List[str]:
    """
    Memory-efficient extreme cleaning with threading optimization.
    
    Args:
        data: List of strings to clean
        max_workers: Number of worker threads (auto-calculated if None)
        streaming: Use streaming mode for minimal memory usage
    
    Returns:
        List of cleaned strings
    """
    processor = _create_memory_efficient_processor(_extreme_clean)
    return processor(data, max_workers, streaming)


def strict_clean_efficient(data: List[str], max_workers: Optional[int] = None,
                          streaming: bool = False) -> List[str]:
    """
    Memory-efficient strict cleaning with threading optimization.
    
    Args:
        data: List of strings to clean
        max_workers: Number of worker threads (auto-calculated if None)  
        streaming: Use streaming mode for minimal memory usage
    
    Returns:
        List of cleaned strings
    """
    processor = _create_memory_efficient_processor(_strict_clean)
    return processor(data, max_workers, streaming)


def relaxed_clean_efficient(data: List[str], max_workers: Optional[int] = None,
                           streaming: bool = False) -> List[str]:
    """
    Memory-efficient relaxed cleaning with threading optimization.
    
    Args:
        data: List of strings to clean
        max_workers: Number of worker threads (auto-calculated if None)
        streaming: Use streaming mode for minimal memory usage
    
    Returns:
        List of cleaned strings
    """
    processor = _create_memory_efficient_processor(_relaxed_clean)
    return processor(data, max_workers, streaming)


# Enhanced versions of original functions with auto-detection
def extreme_clean(data: List[str], efficient: bool = True, **kwargs) -> List[str]:
    """
    Extreme cleaning with optional efficiency mode.
    
    Args:
        data: List of strings to clean
        efficient: Use memory-efficient threading (default: True)
        **kwargs: Additional arguments for efficient mode
    
    Returns:
        List of cleaned strings
    """
    if efficient and len(data) > 100:
        return extreme_clean_efficient(data, **kwargs)
    else:
        # Fall back to original implementation for small datasets
        try:
            result = _extreme_clean(data)
            gc.collect()
            return result
        finally:
            gc.collect()


def strict_clean(data: List[str], efficient: bool = True, **kwargs) -> List[str]:
    """
    Strict cleaning with optional efficiency mode.
    
    Args:
        data: List of strings to clean
        efficient: Use memory-efficient threading (default: True)
        **kwargs: Additional arguments for efficient mode
    
    Returns:
        List of cleaned strings
    """
    if efficient and len(data) > 100:
        return strict_clean_efficient(data, **kwargs)
    else:
        # Fall back to original implementation for small datasets
        try:
            result = _strict_clean(data)
            gc.collect()
            return result
        finally:
            gc.collect()


def relaxed_clean(data: List[str], efficient: bool = True, **kwargs) -> List[str]:
    """
    Relaxed cleaning with optional efficiency mode.
    
    Args:
        data: List of strings to clean
        efficient: Use memory-efficient threading (default: True)
        **kwargs: Additional arguments for efficient mode
    
    Returns:
        List of cleaned strings
    """
    if efficient and len(data) > 100:
        return relaxed_clean_efficient(data, **kwargs)
    else:
        # Fall back to original implementation for small datasets  
        try:
            result = _relaxed_clean(data)
            gc.collect()
            return result
        finally:
            gc.collect()


# Legacy functions for backward compatibility (now use efficient versions by default)
def parallelize(strategy: Callable, data: List[str], max_workers: int = 0) -> List[str]:
    """
    Legacy parallelize function - now uses efficient threading by default.
    
    Maintained for backward compatibility.
    """
    if max_workers == 0:
        max_workers = None
    
    processor = _create_memory_efficient_processor(strategy)
    return processor(data, max_workers, streaming=False)
