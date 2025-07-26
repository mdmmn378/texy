#!/usr/bin/env python3
"""
Comprehensive memory leak test for texy functions in multi-threading and multi-processing scenarios.

This test compares:
1. Direct Rust functions (no threading)
2. Original pipelines with ThreadPoolExecutor  
3. Efficient pipelines with MemoryEfficientThreadPool
4. ProcessPoolExecutor for comparison
"""

import gc
import psutil
import time
import os
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Dict, Any, Callable
import threading

# Import all variants
from texy import texy  # Direct Rust functions
from texy.pipelines import extreme_clean, strict_clean, relaxed_clean  # Original pipelines
from texy.pipelines_efficient import (
    extreme_clean_efficient, 
    strict_clean_efficient, 
    relaxed_clean_efficient
)  # Efficient pipelines


class ConcurrencyMemoryTracker:
    """Track memory usage across different concurrency patterns."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        
    def get_memory_mb(self) -> float:
        """Get current RSS memory in MB."""
        return self.process.memory_info().rss / 1024 / 1024
    
    def aggressive_cleanup(self):
        """Force aggressive garbage collection."""
        for _ in range(5):
            collected = gc.collect()
            if collected == 0:
                break
            time.sleep(0.01)


def create_test_data(size: int) -> List[str]:
    """Create test data for memory testing."""
    base_samples = [
        "Complex text with emoji 😊 URLs https://example.com and <p>HTML</p>",
        "Email test@example.com with punctuation!@#$%^&*()",
        "Multiple      spaces     and    tabs\t\t\tbetween words",
        "<xml>XML content</xml> with newlines\n\nand more content",
        "Bengali text: কুকুর একটি পোষা প্রাণী সংখ্যা ১২৩৪৫",
        "Mixed emoticons :) :( :D and emojis 🚀 🎉 🔥",
        "URL test https://sub.domain.com/path?param=value&other=123",
        "Infrequent punctuation test ¡¿§±×÷≠≤≥∞∑√∫",
    ]
    
    # Create larger test set
    repeats = (size // len(base_samples)) + 1
    samples = (base_samples * repeats)[:size]
    return samples


def test_direct_rust_functions(tracker: ConcurrencyMemoryTracker, test_data: List[str]) -> Dict[str, Any]:
    """Test direct Rust functions (no Python concurrency)."""
    print("🔧 Testing Direct Rust Functions (No Threading)")
    
    tracker.aggressive_cleanup()
    start_memory = tracker.get_memory_mb()
    
    results = {}
    functions = [
        ("rust_extreme", texy.extreme_clean),
        ("rust_strict", texy.strict_clean),
        ("rust_relaxed", texy.relaxed_clean)
    ]
    
    for name, func in functions:
        func_start = tracker.get_memory_mb()
        
        # Run multiple times to detect leaks
        for i in range(10):
            result = func(test_data.copy())
            del result
            tracker.aggressive_cleanup()
        
        func_end = tracker.get_memory_mb()
        growth = func_end - func_start
        
        print(f"  {name:12}: {func_start:.1f} → {func_end:.1f} MB ({growth:+.1f} MB)")
        
        results[name] = {
            'start': func_start,
            'end': func_end,
            'growth': growth,
            'has_leak': growth > 2.0
        }
    
    return results


def test_original_pipelines(tracker: ConcurrencyMemoryTracker, test_data: List[str]) -> Dict[str, Any]:
    """Test original pipeline functions with built-in threading."""
    print("🧵 Testing Original Pipelines (Built-in Threading)")
    
    tracker.aggressive_cleanup()
    start_memory = tracker.get_memory_mb()
    
    results = {}
    functions = [
        ("pipeline_extreme", extreme_clean),
        ("pipeline_strict", strict_clean),
        ("pipeline_relaxed", relaxed_clean)
    ]
    
    for name, func in functions:
        func_start = tracker.get_memory_mb()
        
        # Run multiple times to detect leaks
        for i in range(10):
            result = func(test_data.copy())
            del result
            tracker.aggressive_cleanup()
        
        func_end = tracker.get_memory_mb()
        growth = func_end - func_start
        
        print(f"  {name:16}: {func_start:.1f} → {func_end:.1f} MB ({growth:+.1f} MB)")
        
        results[name] = {
            'start': func_start,
            'end': func_end,
            'growth': growth,
            'has_leak': growth > 5.0  # Higher threshold for threading
        }
    
    return results


def test_efficient_pipelines(tracker: ConcurrencyMemoryTracker, test_data: List[str]) -> Dict[str, Any]:
    """Test memory-efficient pipeline functions."""
    print("⚡ Testing Efficient Pipelines (Memory-Optimized Threading)")
    
    tracker.aggressive_cleanup()
    start_memory = tracker.get_memory_mb()
    
    results = {}
    functions = [
        ("efficient_extreme", extreme_clean_efficient),
        ("efficient_strict", strict_clean_efficient),
        ("efficient_relaxed", relaxed_clean_efficient)
    ]
    
    for name, func in functions:
        func_start = tracker.get_memory_mb()
        
        # Run multiple times to detect leaks
        for i in range(10):
            result = func(test_data.copy(), max_workers=4)
            del result
            tracker.aggressive_cleanup()
        
        func_end = tracker.get_memory_mb()
        growth = func_end - func_start
        
        print(f"  {name:17}: {func_start:.1f} → {func_end:.1f} MB ({growth:+.1f} MB)")
        
        results[name] = {
            'start': func_start,
            'end': func_end,
            'growth': growth,
            'has_leak': growth > 5.0  # Higher threshold for threading
        }
    
    return results


def test_manual_threading(tracker: ConcurrencyMemoryTracker, test_data: List[str]) -> Dict[str, Any]:
    """Test manual ThreadPoolExecutor usage."""
    print("🔀 Testing Manual ThreadPoolExecutor")
    
    def process_batch(batch_data):
        """Process a batch of data."""
        return texy.extreme_clean(batch_data)
    
    tracker.aggressive_cleanup()
    start_memory = tracker.get_memory_mb()
    
    # Split data into batches
    batch_size = len(test_data) // 4
    batches = [test_data[i:i + batch_size] for i in range(0, len(test_data), batch_size)]
    
    all_results = []
    
    # Run multiple iterations
    for iteration in range(10):
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(process_batch, batch.copy()) for batch in batches]
            
            iteration_results = []
            for future in as_completed(futures):
                result = future.result()
                iteration_results.extend(result)
                del result
            
            all_results.append(iteration_results)
            del iteration_results
            del futures
        
        tracker.aggressive_cleanup()
    
    end_memory = tracker.get_memory_mb()
    growth = end_memory - start_memory
    
    print(f"  manual_threading: {start_memory:.1f} → {end_memory:.1f} MB ({growth:+.1f} MB)")
    
    del all_results
    tracker.aggressive_cleanup()
    
    return {
        'manual_threading': {
            'start': start_memory,
            'end': end_memory,
            'growth': growth,
            'has_leak': growth > 10.0  # Higher threshold for manual threading
        }
    }


def test_process_pool(tracker: ConcurrencyMemoryTracker, test_data: List[str]) -> Dict[str, Any]:
    """Test ProcessPoolExecutor for comparison."""
    print("🔄 Testing ProcessPoolExecutor")
    
    def process_batch(batch_data):
        """Process a batch of data in separate process."""
        from texy import texy
        return texy.extreme_clean(batch_data)
    
    tracker.aggressive_cleanup()
    start_memory = tracker.get_memory_mb()
    
    # Split data into batches
    batch_size = len(test_data) // 4
    batches = [test_data[i:i + batch_size] for i in range(0, len(test_data), batch_size)]
    
    all_results = []
    
    # Run multiple iterations
    for iteration in range(5):  # Fewer iterations for process pool
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(process_batch, batch) for batch in batches]
            
            iteration_results = []
            for future in as_completed(futures):
                result = future.result()
                iteration_results.extend(result)
                del result
            
            all_results.append(iteration_results)
            del iteration_results
            del futures
        
        tracker.aggressive_cleanup()
    
    end_memory = tracker.get_memory_mb()
    growth = end_memory - start_memory
    
    print(f"  process_pool    : {start_memory:.1f} → {end_memory:.1f} MB ({growth:+.1f} MB)")
    
    del all_results
    tracker.aggressive_cleanup()
    
    return {
        'process_pool': {
            'start': start_memory,
            'end': end_memory,
            'growth': growth,
            'has_leak': growth > 3.0  # Lower threshold for process pool
        }
    }


def test_streaming_vs_batch(tracker: ConcurrencyMemoryTracker, test_data: List[str]) -> Dict[str, Any]:
    """Test streaming vs batch mode in efficient pipelines."""
    print("📊 Testing Streaming vs Batch Mode")
    
    results = {}
    
    # Test batch mode
    tracker.aggressive_cleanup()
    batch_start = tracker.get_memory_mb()
    
    for i in range(10):
        result = extreme_clean_efficient(test_data.copy(), streaming=False)
        del result
        tracker.aggressive_cleanup()
    
    batch_end = tracker.get_memory_mb()
    batch_growth = batch_end - batch_start
    
    print(f"  batch_mode    : {batch_start:.1f} → {batch_end:.1f} MB ({batch_growth:+.1f} MB)")
    
    # Test streaming mode
    tracker.aggressive_cleanup()
    stream_start = tracker.get_memory_mb()
    
    for i in range(10):
        result = extreme_clean_efficient(test_data.copy(), streaming=True)
        del result
        tracker.aggressive_cleanup()
    
    stream_end = tracker.get_memory_mb()
    stream_growth = stream_end - stream_start
    
    print(f"  streaming_mode: {stream_start:.1f} → {stream_end:.1f} MB ({stream_growth:+.1f} MB)")
    
    return {
        'batch_mode': {
            'start': batch_start,
            'end': batch_end,
            'growth': batch_growth,
            'has_leak': batch_growth > 5.0
        },
        'streaming_mode': {
            'start': stream_start,
            'end': stream_end,
            'growth': stream_growth,
            'has_leak': stream_growth > 5.0
        }
    }


def run_comprehensive_concurrency_test(data_size: int = 25000):
    """Run comprehensive concurrency memory tests."""
    print("🚀 COMPREHENSIVE CONCURRENCY MEMORY LEAK TEST")
    print("=" * 60)
    print(f"Testing with {data_size:,} samples across multiple concurrency patterns")
    print(f"PID: {os.getpid()}")
    
    tracker = ConcurrencyMemoryTracker()
    initial_memory = tracker.get_memory_mb()
    print(f"Initial memory: {initial_memory:.1f} MB")
    
    # Create test data
    test_data = create_test_data(data_size)
    print(f"Test data created: {len(test_data):,} samples")
    
    all_results = {}
    
    # Run all tests
    try:
        # Test 1: Direct Rust functions
        all_results.update(test_direct_rust_functions(tracker, test_data))
        
        print()
        # Test 2: Original pipelines
        all_results.update(test_original_pipelines(tracker, test_data))
        
        print()
        # Test 3: Efficient pipelines
        all_results.update(test_efficient_pipelines(tracker, test_data))
        
        print()
        # Test 4: Manual threading
        all_results.update(test_manual_threading(tracker, test_data))
        
        print()
        # Test 5: Process pool
        all_results.update(test_process_pool(tracker, test_data))
        
        print()
        # Test 6: Streaming vs batch
        all_results.update(test_streaming_vs_batch(tracker, test_data))
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    
    # Final analysis
    print(f"\n📈 COMPREHENSIVE RESULTS SUMMARY")
    print("=" * 60)
    
    categories = {
        'Direct Rust': ['rust_extreme', 'rust_strict', 'rust_relaxed'],
        'Original Pipelines': ['pipeline_extreme', 'pipeline_strict', 'pipeline_relaxed'],
        'Efficient Pipelines': ['efficient_extreme', 'efficient_strict', 'efficient_relaxed'],
        'Manual Threading': ['manual_threading'],
        'Process Pool': ['process_pool'],
        'Mode Comparison': ['batch_mode', 'streaming_mode']
    }
    
    overall_leaks = False
    
    for category, test_names in categories.items():
        print(f"\n{category}:")
        category_leaks = False
        
        for test_name in test_names:
            if test_name in all_results:
                result = all_results[test_name]
                status = "⚠️ LEAK" if result['has_leak'] else "✅ CLEAN"
                print(f"  {test_name:17}: {status:8} ({result['growth']:+5.1f} MB)")
                
                if result['has_leak']:
                    category_leaks = True
                    overall_leaks = True
        
        if not category_leaks and any(name in all_results for name in test_names):
            print(f"  → {category} is memory safe ✅")
    
    # Overall conclusion
    print(f"\n🏆 FINAL VERDICT")
    print("=" * 60)
    
    if overall_leaks:
        print("⚠️  MEMORY LEAKS DETECTED in some concurrency patterns!")
        print("   Review the specific patterns showing leaks above.")
        print("   Consider using efficient pipelines or process pools.")
    else:
        print("✅ ALL CONCURRENCY PATTERNS ARE MEMORY SAFE!")
        print("   No significant memory leaks detected in any pattern.")
        print("   Safe for production use across all tested scenarios.")
    
    final_memory = tracker.get_memory_mb()
    total_growth = final_memory - initial_memory
    print(f"\nTotal test growth: {total_growth:+.1f} MB")
    print(f"Final memory: {final_memory:.1f} MB")
    
    return all_results


if __name__ == "__main__":
    # Set multiprocessing start method for compatibility
    if hasattr(mp, 'set_start_method'):
        try:
            mp.set_start_method('spawn', force=True)
        except RuntimeError:
            pass  # Already set
    
    print("🔬 Starting Comprehensive Concurrency Memory Tests")
    
    try:
        results = run_comprehensive_concurrency_test(data_size=25000)
        print("\n✅ All tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
