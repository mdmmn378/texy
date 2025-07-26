#!/usr/bin/env python3
"""
Simple Executor Memory Comparison Script

This script demonstrates why ProcessPoolExecutor and ThreadPoolExecutor
show different memory usage patterns in your tests.
"""

import gc
import os
import psutil
import time
import sys
from typing import Dict, List, Any
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing


def get_memory_mb() -> float:
    """Get current RSS memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def create_test_text() -> str:
    """Create test text for memory testing."""
    return """
    Complex text with emojis 😊🚀⭐, URLs https://example.com,
    emails test@domain.com, HTML <b>bold</b>, XML <tag>content</tag>,
    special chars !@#$%^&*(), unicode café naïve résumé,
    numbers 1,234.56, currencies $100.00 €50.00 £25.00,
    and very long words like pneumonoultramicroscopicsilicovolcanoconiosis.
    """ * 10  # Make it larger


def simulate_extreme_clean(texts: List[str]) -> List[str]:
    """Simulate the extreme_clean function for testing."""
    import re
    
    results = []
    for text in texts:
        # Simulate complex processing that uses memory
        
        # Remove URLs
        text = re.sub(r'https?://[^\s]+', '', text)
        
        # Remove emails  
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove emojis (simple version)
        text = re.sub(r'[😊🚀⭐]', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip and store
        results.append(text.strip())
    
    return results


def test_executor_memory(executor_type: str, test_data: List[str], sample_size: int) -> Dict[str, Any]:
    """Test memory usage with specific executor type."""
    print(f"\n{'='*60}")
    print(f"TESTING {executor_type.upper()} WITH {sample_size:,} SAMPLES")
    print(f"{'='*60}")
    
    # Get initial memory
    initial_memory = get_memory_mb()
    print(f"Initial memory: {initial_memory:.2f} MB")
    
    # Test processing
    start_time = time.time()
    
    if executor_type == "process":
        max_workers = min(4, multiprocessing.cpu_count())
        print(f"Using {max_workers} worker processes")
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Split data into chunks
            chunk_size = len(test_data) // max_workers
            chunks = [test_data[i:i + chunk_size] for i in range(0, len(test_data), chunk_size)]
            
            # Submit work
            futures = [executor.submit(simulate_extreme_clean, chunk) for chunk in chunks]
            
            # Track memory during processing
            peak_memory = initial_memory
            for i, future in enumerate(futures):
                result = future.result()
                current_memory = get_memory_mb()
                peak_memory = max(peak_memory, current_memory)
                print(f"  Chunk {i+1} completed, memory: {current_memory:.2f} MB")
                del result  # Clean up immediately
    
    elif executor_type == "thread":
        max_workers = min(8, (os.cpu_count() or 1) * 2)
        print(f"Using {max_workers} worker threads")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Split data into chunks
            chunk_size = len(test_data) // max_workers
            chunks = [test_data[i:i + chunk_size] for i in range(0, len(test_data), chunk_size)]
            
            # Submit work
            futures = [executor.submit(simulate_extreme_clean, chunk) for chunk in chunks]
            
            # Track memory during processing
            peak_memory = initial_memory
            for i, future in enumerate(futures):
                result = future.result()
                current_memory = get_memory_mb()
                peak_memory = max(peak_memory, current_memory)
                print(f"  Chunk {i+1} completed, memory: {current_memory:.2f} MB")
                del result  # Clean up immediately
    
    else:
        # Sequential processing for comparison
        print("Using sequential processing")
        peak_memory = initial_memory
        result = simulate_extreme_clean(test_data)
        current_memory = get_memory_mb()
        peak_memory = max(peak_memory, current_memory)
        print(f"  Sequential completed, memory: {current_memory:.2f} MB")
        del result
    
    end_time = time.time()
    
    # Force cleanup
    if 'chunks' in locals():
        del chunks
    gc.collect()
    
    # Get final memory
    final_memory = get_memory_mb()
    
    duration = end_time - start_time
    rate = sample_size / duration if duration > 0 else 0
    memory_growth = final_memory - initial_memory
    
    print(f"Duration: {duration:.2f}s")
    print(f"Rate: {rate:,.0f} items/sec")
    print(f"Memory growth: {memory_growth:+.2f} MB")
    print(f"Peak memory: {peak_memory:.2f} MB")
    print(f"Final memory: {final_memory:.2f} MB")
    
    return {
        'executor_type': executor_type,
        'duration': duration,
        'rate': rate,
        'memory_growth': memory_growth,
        'initial_memory': initial_memory,
        'peak_memory': peak_memory,
        'final_memory': final_memory,
        'sample_size': sample_size
    }


def explain_memory_differences():
    """Explain why the memory differences occur."""
    print(f"\n{'='*80}")
    print("WHY PROCESSPOOL AND THREADPOOL SHOW DIFFERENT MEMORY PATTERNS")
    print(f"{'='*80}")
    
    print("""
🔄 ProcessPoolExecutor Memory Behavior:
    
   Main Process Memory Space:
   ┌─────────────────────────┐
   │     Main Process        │  ← psutil measures this
   │   - Script code         │
   │   - Test data           │
   │   - Communication       │
   └─────────────────────────┘
   
   Worker Process Memory Spaces (ISOLATED):
   ┌───────────┐ ┌───────────┐ ┌───────────┐
   │ Worker 1  │ │ Worker 2  │ │ Worker 3  │  ← Memory here is NOT
   │ - Data    │ │ - Data    │ │ - Data    │    measured by main
   │ - Results │ │ - Results │ │ - Results │    process psutil
   └───────────┘ └───────────┘ └───────────┘
   
   Result: Main process memory stays relatively stable because
          worker memory allocations are in separate processes.

🧵 ThreadPoolExecutor Memory Behavior:
    
   Shared Memory Space (ALL threads share this):
   ┌─────────────────────────────────────────┐
   │          Single Process Memory          │  ← psutil measures ALL of this
   │                                         │
   │  Main Thread    Thread 1   Thread 2    │
   │  - Script      - Data      - Data       │
   │  - Test data   - Results   - Results    │
   │  - GIL mgmt    - Objects   - Objects    │
   │                                         │
   └─────────────────────────────────────────┘
   
   Result: All memory allocations from all threads accumulate
          in the same memory space, causing higher memory usage.

💡 Key Differences:

1. Memory Isolation:
   - ProcessPool: Worker memory is isolated from main process
   - ThreadPool: All memory is shared in single process space

2. Garbage Collection:
   - ProcessPool: Each worker can GC independently  
   - ThreadPool: GIL can delay GC, causing memory buildup

3. Memory Measurement:
   - ProcessPool: psutil only sees main process memory
   - ThreadPool: psutil sees ALL thread memory allocations

4. Communication Overhead:
   - ProcessPool: Serialization/pickling overhead in main process
   - ThreadPool: Direct memory sharing, no serialization

5. Large Dataset Behavior:
   - ProcessPool: Stable main memory, high worker memory (unmeasured)
   - ThreadPool: High measured memory as all allocations accumulate

This explains your observations:
- ThreadPool shows +529MB for 1M samples (all allocations visible)
- ProcessPool shows +16MB for 1M samples (only communication overhead visible)
- Smaller samples in ThreadPool benefit from shared memory efficiency
""")


def compare_all_executors():
    """Compare all executor types with different sample sizes."""
    print("="*80)
    print("MEMORY BEHAVIOR COMPARISON: PROCESS vs THREAD EXECUTORS")
    print("="*80)
    
    # System info
    system_memory = psutil.virtual_memory()
    print(f"System: {system_memory.total / 1024**3:.2f} GB total")
    print(f"CPUs: {multiprocessing.cpu_count()}")
    
    sample_sizes = [100_000, 50_000, 10_000]  # Smaller sizes for demo
    all_results = []
    
    for sample_size in sample_sizes:
        print(f"\n🔄 Testing with {sample_size:,} samples")
        
        # Create test data
        base_text = create_test_text()
        test_data = [base_text] * sample_size
        
        # Test all executor types
        for executor_type in ["process", "thread", "sequential"]:
            try:
                result = test_executor_memory(executor_type, test_data, sample_size)
                all_results.append(result)
                
                # Wait between tests
                time.sleep(2)
                
            except Exception as e:
                print(f"ERROR with {executor_type}: {e}")
        
        # Cleanup
        del test_data
        del base_text
        gc.collect()
        
        print("\nWaiting 3 seconds before next sample size...")
        time.sleep(3)
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY OF RESULTS")
    print(f"{'='*80}")
    
    for sample_size in sample_sizes:
        print(f"\n📊 {sample_size:,} samples:")
        
        size_results = [r for r in all_results if r['sample_size'] == sample_size]
        
        for result in size_results:
            print(f"  {result['executor_type']:>10}: "
                  f"{result['duration']:>6.2f}s, "
                  f"{result['rate']:>8,.0f} items/sec, "
                  f"{result['memory_growth']:>+6.1f} MB growth, "
                  f"{result['peak_memory']:>6.1f} MB peak")
    
    explain_memory_differences()


if __name__ == "__main__":
    try:
        compare_all_executors()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
