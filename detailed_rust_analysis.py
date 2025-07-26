#!/usr/bin/env python3
"""
Focused analysis of Rust binding memory behavior.

This test investigates the specific memory patterns observed in the initial test.
"""

import gc
import psutil
import time
import os
from typing import List

# Import direct Rust functions
from texy import texy


def detailed_memory_analysis():
    """Detailed analysis of memory behavior for each Rust function."""
    print("🔬 DETAILED RUST BINDING MEMORY ANALYSIS")
    print("=" * 60)
    
    process = psutil.Process(os.getpid())
    
    def get_memory():
        return process.memory_info().rss / 1024 / 1024
    
    def create_test_data(size: int) -> List[str]:
        """Create test data."""
        base = "This is a test string with emojis 😊 and URLs https://example.com"
        return [base + f" sample {i}" for i in range(size)]
    
    # Test different sample sizes
    test_sizes = [1000, 5000, 10000, 25000, 50000]
    
    for size in test_sizes:
        print(f"\n📊 Testing with {size:,} samples")
        print("-" * 40)
        
        # Force cleanup before test
        for _ in range(5):
            gc.collect()
        time.sleep(0.1)
        
        baseline = get_memory()
        print(f"Baseline: {baseline:.1f} MB")
        
        # Create test data
        test_data = create_test_data(size)
        data_memory = get_memory()
        data_overhead = data_memory - baseline
        print(f"Data created: {data_memory:.1f} MB (+{data_overhead:.1f} MB)")
        
        # Test extreme_clean (the one showing leaks)
        start_memory = get_memory()
        
        # Single call
        result = texy.extreme_clean(test_data.copy())
        
        after_call = get_memory()
        call_overhead = after_call - start_memory
        
        # Clean up result
        del result
        gc.collect()
        
        after_cleanup = get_memory()
        final_overhead = after_cleanup - baseline
        
        print(f"After extreme_clean: {after_call:.1f} MB (+{call_overhead:.1f} MB)")
        print(f"After cleanup: {after_cleanup:.1f} MB (+{final_overhead:.1f} MB)")
        
        # Calculate efficiency
        input_size_mb = len(str(test_data)) / (1024 * 1024)
        print(f"Input size estimate: {input_size_mb:.1f} MB")
        print(f"Memory efficiency: {final_overhead/input_size_mb:.2f}x input size")
        
        # Clean up test data
        del test_data
        for _ in range(5):
            gc.collect()
        
        final_final = get_memory()
        print(f"Final cleanup: {final_final:.1f} MB")
        
        if final_overhead > 2.0:
            print(f"⚠️  Significant retention: {final_overhead:.1f} MB")
        else:
            print(f"✅ Acceptable retention: {final_overhead:.1f} MB")


def repeated_calls_analysis():
    """Analyze memory behavior over repeated calls."""
    print(f"\n🔄 REPEATED CALLS ANALYSIS")
    print("=" * 60)
    
    process = psutil.Process(os.getpid())
    
    def get_memory():
        return process.memory_info().rss / 1024 / 1024
    
    # Create test data once
    test_data = ["Test string with emoji 😊 and URL https://example.com"] * 10000
    
    print(f"Testing repeated calls with {len(test_data):,} samples")
    
    # Force baseline
    for _ in range(5):
        gc.collect()
    time.sleep(0.1)
    baseline = get_memory()
    
    print(f"Baseline: {baseline:.1f} MB")
    
    # Run multiple calls and track memory
    memories = [baseline]
    
    for i in range(20):
        # Call Rust function
        result = texy.extreme_clean(test_data.copy())
        
        # Immediate cleanup
        del result
        gc.collect()
        
        current_memory = get_memory()
        memories.append(current_memory)
        
        if i % 5 == 0:
            growth = current_memory - baseline
            print(f"Call {i+1:2d}: {current_memory:.1f} MB (+{growth:+.1f} MB)")
    
    # Analyze trend
    final_memory = memories[-1]
    total_growth = final_memory - baseline
    
    print(f"\nMemory progression:")
    for i, mem in enumerate(memories[::5]):
        growth = mem - baseline
        print(f"  Call {i*5:2d}: {mem:.1f} MB (+{growth:+.1f} MB)")
    
    print(f"\nFinal result:")
    print(f"  Total growth: {total_growth:+.1f} MB over 20 calls")
    print(f"  Growth per call: {total_growth/20:+.2f} MB average")
    
    if total_growth > 10.0:
        print(f"⚠️  LIKELY MEMORY LEAK: {total_growth:.1f} MB accumulated")
    elif total_growth > 5.0:
        print(f"⚠️  POSSIBLE MEMORY INEFFICIENCY: {total_growth:.1f} MB accumulated")
    else:
        print(f"✅ CLEAN: Only {total_growth:.1f} MB growth")


def memory_pattern_comparison():
    """Compare memory patterns between the three functions."""
    print(f"\n🆚 FUNCTION COMPARISON")
    print("=" * 60)
    
    process = psutil.Process(os.getpid())
    
    def get_memory():
        return process.memory_info().rss / 1024 / 1024
    
    # Test data
    test_data = ["Complex test 😊 https://example.com <p>HTML</p>"] * 20000
    
    functions = [
        ("extreme_clean", texy.extreme_clean),
        ("strict_clean", texy.strict_clean),
        ("relaxed_clean", texy.relaxed_clean)
    ]
    
    for func_name, func in functions:
        print(f"\n🔧 Testing {func_name}")
        
        # Force cleanup
        for _ in range(5):
            gc.collect()
        baseline = get_memory()
        
        # Multiple calls
        memories = []
        for i in range(10):
            result = func(test_data.copy())
            del result
            gc.collect()
            memories.append(get_memory())
        
        final_memory = memories[-1]
        growth = final_memory - baseline
        
        print(f"  Baseline: {baseline:.1f} MB")
        print(f"  Final: {final_memory:.1f} MB")
        print(f"  Growth: {growth:+.1f} MB")
        
        if growth > 5.0:
            print(f"  ⚠️  HIGH RETENTION")
        elif growth > 2.0:
            print(f"  ⚠️  MODERATE RETENTION")  
        else:
            print(f"  ✅ LOW RETENTION")


if __name__ == "__main__":
    print("🚀 Starting Detailed Rust Binding Analysis")
    print(f"Python PID: {os.getpid()}")
    
    try:
        detailed_memory_analysis()
        repeated_calls_analysis()
        memory_pattern_comparison()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    final_memory = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"\n🏁 Analysis completed. Final memory: {final_memory:.1f} MB")
