#!/usr/bin/env python3
"""
Focused concurrency memory test with fixes for ProcessPoolExecutor.
"""

import gc
import psutil
import time
import os
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Dict, Any

# Import texy functions
from texy import texy
from texy.pipelines import extreme_clean, strict_clean, relaxed_clean
from texy.pipelines_efficient import (
    extreme_clean_efficient, 
    strict_clean_efficient, 
    relaxed_clean_efficient
)


def process_batch_worker(batch_data):
    """Worker function for ProcessPoolExecutor (must be at module level)."""
    from texy import texy
    return texy.extreme_clean(batch_data)


class FocusedMemoryTracker:
    """Simplified memory tracker for focused testing."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        
    def get_memory_mb(self) -> float:
        return self.process.memory_info().rss / 1024 / 1024
    
    def cleanup(self):
        for _ in range(3):
            gc.collect()
        time.sleep(0.05)


def create_test_data(size: int) -> List[str]:
    """Create test data."""
    base = "Complex text 😊 https://example.com <p>HTML</p> test@email.com"
    return [f"{base} sample {i}" for i in range(size)]


def test_concurrency_patterns():
    """Test different concurrency patterns for memory leaks."""
    print("🔍 FOCUSED CONCURRENCY MEMORY TEST")
    print("=" * 50)
    
    tracker = FocusedMemoryTracker()
    test_data = create_test_data(15000)
    
    print(f"Testing with {len(test_data):,} samples")
    print(f"Initial memory: {tracker.get_memory_mb():.1f} MB")
    
    results = {}
    
    # Test 1: Direct Rust functions (baseline)
    print(f"\n🔧 Direct Rust Functions")
    tracker.cleanup()
    start = tracker.get_memory_mb()
    
    for i in range(5):
        result = texy.extreme_clean(test_data.copy())
        del result
        tracker.cleanup()
    
    end = tracker.get_memory_mb()
    growth = end - start
    print(f"  Memory: {start:.1f} → {end:.1f} MB ({growth:+.1f} MB)")
    results['direct_rust'] = growth
    
    # Test 2: Original pipelines
    print(f"\n🧵 Original Pipelines")
    tracker.cleanup()
    start = tracker.get_memory_mb()
    
    for i in range(5):
        result = extreme_clean(test_data.copy())
        del result
        tracker.cleanup()
    
    end = tracker.get_memory_mb()
    growth = end - start
    print(f"  Memory: {start:.1f} → {end:.1f} MB ({growth:+.1f} MB)")
    results['original_pipelines'] = growth
    
    # Test 3: Efficient pipelines
    print(f"\n⚡ Efficient Pipelines")
    tracker.cleanup()
    start = tracker.get_memory_mb()
    
    for i in range(5):
        result = extreme_clean_efficient(test_data.copy(), max_workers=4)
        del result
        tracker.cleanup()
    
    end = tracker.get_memory_mb()
    growth = end - start
    print(f"  Memory: {start:.1f} → {end:.1f} MB ({growth:+.1f} MB)")
    results['efficient_pipelines'] = growth
    
    # Test 4: Manual ThreadPoolExecutor
    print(f"\n🔀 Manual ThreadPoolExecutor")
    tracker.cleanup()
    start = tracker.get_memory_mb()
    
    batch_size = len(test_data) // 4
    batches = [test_data[i:i + batch_size] for i in range(0, len(test_data), batch_size)]
    
    for iteration in range(5):
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(texy.extreme_clean, batch.copy()) for batch in batches]
            
            all_results = []
            for future in as_completed(futures):
                result = future.result()
                all_results.extend(result)
                del result
            
            del all_results
            del futures
        tracker.cleanup()
    
    end = tracker.get_memory_mb()
    growth = end - start
    print(f"  Memory: {start:.1f} → {end:.1f} MB ({growth:+.1f} MB)")
    results['manual_threading'] = growth
    
    # Test 5: ProcessPoolExecutor (fixed)
    print(f"\n🔄 ProcessPoolExecutor")
    tracker.cleanup()
    start = tracker.get_memory_mb()
    
    try:
        for iteration in range(3):  # Fewer iterations for process pool
            with ProcessPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(process_batch_worker, batch) for batch in batches]
                
                all_results = []
                for future in as_completed(futures):
                    result = future.result()
                    all_results.extend(result)
                    del result
                
                del all_results
                del futures
            tracker.cleanup()
        
        end = tracker.get_memory_mb()
        growth = end - start
        print(f"  Memory: {start:.1f} → {end:.1f} MB ({growth:+.1f} MB)")
        results['process_pool'] = growth
        
    except Exception as e:
        print(f"  ProcessPool error: {e}")
        results['process_pool'] = None
    
    # Test 6: Streaming vs Batch mode
    print(f"\n📊 Streaming vs Batch Mode")
    
    # Batch mode
    tracker.cleanup()
    start = tracker.get_memory_mb()
    
    for i in range(5):
        result = extreme_clean_efficient(test_data.copy(), streaming=False)
        del result
        tracker.cleanup()
    
    end = tracker.get_memory_mb()
    batch_growth = end - start
    print(f"  Batch mode:     {start:.1f} → {end:.1f} MB ({batch_growth:+.1f} MB)")
    
    # Streaming mode
    tracker.cleanup()
    start = tracker.get_memory_mb()
    
    for i in range(5):
        result = extreme_clean_efficient(test_data.copy(), streaming=True)
        del result
        tracker.cleanup()
    
    end = tracker.get_memory_mb()
    stream_growth = end - start
    print(f"  Streaming mode: {start:.1f} → {end:.1f} MB ({stream_growth:+.1f} MB)")
    
    results['batch_mode'] = batch_growth
    results['streaming_mode'] = stream_growth
    
    # Analysis
    print(f"\n📈 RESULTS ANALYSIS")
    print("=" * 50)
    
    leak_threshold = 5.0  # MB
    
    for test_name, growth in results.items():
        if growth is None:
            status = "❌ ERROR"
        elif growth > leak_threshold:
            status = "⚠️  LEAK"
        else:
            status = "✅ CLEAN"
        
        print(f"  {test_name:18}: {status:8} ({growth:+5.1f} MB)" if growth is not None else f"  {test_name:18}: {status}")
    
    # Conclusions
    print(f"\n🎯 CONCLUSIONS")
    print("-" * 30)
    
    clean_patterns = [name for name, growth in results.items() if growth is not None and growth <= leak_threshold]
    leak_patterns = [name for name, growth in results.items() if growth is not None and growth > leak_threshold]
    
    if leak_patterns:
        print(f"⚠️  Memory leaks detected in: {', '.join(leak_patterns)}")
        print(f"✅ Memory safe patterns: {', '.join(clean_patterns)}")
        print(f"\nRecommendation: Use efficient pipelines or original pipelines for production")
    else:
        print(f"✅ All tested patterns are memory safe!")
        print(f"   Safe for production use in multi-threading scenarios")
    
    # Best performing pattern
    if clean_patterns:
        clean_results = {name: results[name] for name in clean_patterns}
        best_pattern = min(clean_results.items(), key=lambda x: x[1])
        print(f"\nBest performing pattern: {best_pattern[0]} ({best_pattern[1]:+.1f} MB)")
    
    return results


def stress_test_threading():
    """Stress test with high concurrency to detect subtle leaks."""
    print(f"\n🏋️ STRESS TEST: High Concurrency")
    print("=" * 50)
    
    tracker = FocusedMemoryTracker()
    test_data = create_test_data(10000)  # Smaller dataset, more iterations
    
    print(f"Testing {len(test_data):,} samples with 20 iterations")
    
    # Test efficient pipelines under stress
    tracker.cleanup()
    start_memory = tracker.get_memory_mb()
    memories = [start_memory]
    
    for i in range(20):
        result = extreme_clean_efficient(test_data.copy(), max_workers=8)
        del result
        tracker.cleanup()
        
        current = tracker.get_memory_mb()
        memories.append(current)
        
        if i % 5 == 0:
            growth = current - start_memory
            print(f"  Iteration {i+1:2d}: {current:.1f} MB ({growth:+.1f} MB)")
    
    final_memory = memories[-1]
    total_growth = final_memory - start_memory
    
    # Analyze trend
    first_half = sum(memories[:11]) / 11
    second_half = sum(memories[11:]) / 10
    trend = second_half - first_half
    
    print(f"\nStress test results:")
    print(f"  Total growth: {total_growth:+.1f} MB")
    print(f"  Memory trend: {trend:+.2f} MB (first vs second half)")
    
    if total_growth > 10.0:
        print(f"  ⚠️  STRESS LEAK: Significant memory accumulation")
    elif trend > 1.0:
        print(f"  ⚠️  PROGRESSIVE LEAK: Upward memory trend")
    else:
        print(f"  ✅ STRESS CLEAN: Stable under high concurrency")
    
    return total_growth, trend


if __name__ == "__main__":
    # Set multiprocessing method
    if hasattr(mp, 'set_start_method'):
        try:
            mp.set_start_method('spawn', force=True)
        except RuntimeError:
            pass
    
    print("🚀 Starting Focused Concurrency Memory Tests")
    initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"Initial memory: {initial_memory:.1f} MB")
    
    try:
        # Main concurrency test
        results = test_concurrency_patterns()
        
        # Stress test
        stress_growth, stress_trend = stress_test_threading()
        
        # Final summary
        print(f"\n🏁 FINAL SUMMARY")
        print("=" * 50)
        
        safe_patterns = sum(1 for growth in results.values() if growth is not None and growth <= 5.0)
        total_patterns = sum(1 for growth in results.values() if growth is not None)
        
        print(f"Memory-safe patterns: {safe_patterns}/{total_patterns}")
        print(f"Stress test result: {stress_growth:+.1f} MB growth, {stress_trend:+.2f} MB trend")
        
        if safe_patterns == total_patterns and stress_growth <= 10.0 and stress_trend <= 1.0:
            print("✅ OVERALL VERDICT: Memory safe for multi-threading/processing")
        else:
            print("⚠️  OVERALL VERDICT: Some patterns show memory issues")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    final_memory = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"\nFinal memory: {final_memory:.1f} MB")
