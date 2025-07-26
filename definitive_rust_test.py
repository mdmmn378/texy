#!/usr/bin/env python3
"""
Definitive test: Do Rust bindings leak memory?

This test provides a clear yes/no answer about memory leaks in texy Rust bindings.
"""

import gc
import psutil
import time
import os
from typing import List, Tuple

from texy import texy


def test_rust_binding_memory_leak() -> Tuple[bool, str, dict]:
    """
    Definitive test for memory leaks in Rust bindings.
    
    Returns:
        (has_leak, conclusion, details)
    """
    print("🎯 DEFINITIVE RUST BINDING MEMORY LEAK TEST")
    print("=" * 50)
    
    process = psutil.Process(os.getpid())
    
    def get_memory():
        return process.memory_info().rss / 1024 / 1024
    
    # Test data - moderate size
    test_data = [
        "Complex text with emoji 😊 URLs https://example.com and <p>HTML</p>"
    ] * 15000
    
    print(f"Test setup: {len(test_data):,} samples")
    
    # Phase 1: Warmup (allow initial memory allocation)
    print("\n🔥 Phase 1: Warmup (5 calls)")
    for _ in range(5):
        gc.collect()
    
    warmup_start = get_memory()
    
    for i in range(5):
        result = texy.extreme_clean(test_data.copy())
        del result
        gc.collect()
        current = get_memory()
        print(f"  Warmup call {i+1}: {current:.1f} MB")
    
    warmup_end = get_memory()
    warmup_growth = warmup_end - warmup_start
    
    print(f"Warmup growth: {warmup_growth:+.1f} MB")
    
    # Phase 2: Stability Test (20 calls to detect leaks)
    print(f"\n🔍 Phase 2: Leak Detection (20 calls)")
    
    stable_start = get_memory()
    memories = []
    
    for i in range(20):
        result = texy.extreme_clean(test_data.copy())
        del result
        gc.collect()
        current = get_memory()
        memories.append(current)
        
        if i % 5 == 0:
            growth = current - stable_start
            print(f"  Call {i+1:2d}: {current:.1f} MB ({growth:+.1f} MB)")
    
    stable_end = get_memory()
    stable_growth = stable_end - stable_start
    
    # Phase 3: Analysis
    print(f"\n📊 Analysis:")
    print(f"  Warmup growth: {warmup_growth:+.1f} MB (expected)")
    print(f"  Stable growth: {stable_growth:+.1f} MB (leak indicator)")
    
    # Memory trend analysis
    first_half = sum(memories[:10]) / 10
    second_half = sum(memories[10:]) / 10
    trend = second_half - first_half
    
    print(f"  Memory trend: {trend:+.2f} MB (first vs second half)")
    
    # Leak criteria
    leak_threshold = 2.0  # MB
    trend_threshold = 0.5  # MB
    
    has_leak = stable_growth > leak_threshold or trend > trend_threshold
    
    # Detailed analysis
    details = {
        'warmup_growth': warmup_growth,
        'stable_growth': stable_growth,
        'memory_trend': trend,
        'final_memory': stable_end,
        'test_samples': len(test_data),
        'leak_threshold': leak_threshold,
        'trend_threshold': trend_threshold
    }
    
    if has_leak:
        if stable_growth > leak_threshold:
            conclusion = f"❌ MEMORY LEAK: {stable_growth:.1f} MB growth in stable phase"
        else:
            conclusion = f"❌ PROGRESSIVE LEAK: {trend:.2f} MB upward trend detected"
    else:
        conclusion = f"✅ NO MEMORY LEAK: {stable_growth:+.1f} MB growth, {trend:+.2f} MB trend"
    
    return has_leak, conclusion, details


def test_all_functions():
    """Test all three Rust functions for memory leaks."""
    print(f"\n🔬 TESTING ALL FUNCTIONS")
    print("=" * 50)
    
    functions = [
        ("extreme_clean", texy.extreme_clean),
        ("strict_clean", texy.strict_clean),
        ("relaxed_clean", texy.relaxed_clean)
    ]
    
    test_data = ["Test string with content 😊 https://example.com"] * 10000
    
    results = {}
    
    for name, func in functions:
        print(f"\n🧪 Testing {name}")
        
        # Cleanup
        for _ in range(5):
            gc.collect()
        
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024
        
        # Run 15 calls
        for i in range(15):
            result = func(test_data.copy())
            del result
            gc.collect()
        
        end_memory = process.memory_info().rss / 1024 / 1024
        growth = end_memory - start_memory
        
        print(f"  Start: {start_memory:.1f} MB")
        print(f"  End:   {end_memory:.1f} MB")
        print(f"  Growth: {growth:+.1f} MB")
        
        has_leak = growth > 3.0
        status = "❌ LEAK" if has_leak else "✅ CLEAN"
        print(f"  Status: {status}")
        
        results[name] = {
            'start': start_memory,
            'end': end_memory,
            'growth': growth,
            'has_leak': has_leak
        }
    
    return results


if __name__ == "__main__":
    print("🚀 Starting Definitive Rust Binding Test")
    print(f"PID: {os.getpid()}")
    print(f"Initial memory: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB")
    
    try:
        # Main leak test
        has_leak, conclusion, details = test_rust_binding_memory_leak()
        
        print(f"\n{conclusion}")
        
        # Test all functions  
        all_results = test_all_functions()
        
        # Final summary
        print(f"\n🏆 FINAL VERDICT")
        print("=" * 50)
        
        any_leaks = has_leak or any(r['has_leak'] for r in all_results.values())
        
        if any_leaks:
            print("❌ RUST BINDINGS HAVE MEMORY ISSUES")
            print("   Some functions retain memory across calls")
            print("   Recommendation: Monitor memory usage in production")
        else:
            print("✅ RUST BINDINGS ARE MEMORY SAFE")
            print("   Functions properly clean up memory")
            print("   Safe for production use")
        
        print(f"\nDetailed results:")
        for name, result in all_results.items():
            status = "LEAK" if result['has_leak'] else "CLEAN"
            print(f"  {name:15}: {status:5} ({result['growth']:+.1f} MB)")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    final_memory = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"\n🏁 Test completed. Final memory: {final_memory:.1f} MB")
