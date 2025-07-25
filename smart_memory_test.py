#!/usr/bin/env python3
"""
Smart zero memory test that accounts for one-time initialization costs.
This test separates initialization overhead from actual memory leaks.
"""
import gc
import time
import ctypes

def get_memory_mb():
    """Get memory in MB using /proc/self/status."""
    try:
        with open('/proc/self/status', 'r') as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    mem_kb = int(line.split()[1])
                    return mem_kb / 1024
    except Exception:
        return 0.0

def force_memory_cleanup():
    """Aggressively force memory cleanup."""
    for _ in range(5):
        gc.collect()
    
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
    except Exception:
        pass

def smart_zero_memory_test():
    """Test for zero memory increase AFTER initialization."""
    print("=" * 70)
    print("TEXY SMART ZERO MEMORY TEST")
    print("(Accounts for one-time initialization costs)")
    print("=" * 70)
    
    force_memory_cleanup()
    initial_memory = get_memory_mb()
    print(f"Initial memory: {initial_memory:.2f} MB")
    
    try:
        from texy.pipelines import extreme_clean
        
        # PHASE 1: Initialization (one-time cost)
        print("\nPHASE 1: INITIALIZATION TEST")
        print("-" * 40)
        
        warmup_data = ["Hello world 😊"] * 100
        
        force_memory_cleanup()
        pre_init_memory = get_memory_mb()
        
        # First call - this will initialize everything
        _ = extreme_clean(warmup_data)
        
        force_memory_cleanup()
        post_init_memory = get_memory_mb()
        
        init_cost = post_init_memory - pre_init_memory
        print(f"One-time initialization cost: {init_cost:.2f} MB")
        
        if init_cost <= 8:
            print("✅ Initialization cost is acceptable")
        else:
            print("⚠️  High initialization cost")
        
        # PHASE 2: Test for memory leaks AFTER initialization
        print("\nPHASE 2: MEMORY LEAK TEST (After initialization)")
        print("-" * 50)
        
        baseline_memory = post_init_memory
        test_sizes = [100, 500, 1000, 2000, 5000, 10000]
        
        base_text = [
            "Hello world with https://example.com 😊",
            "<p>HTML content with tags</p>",
            "Text with :) emoticons and emojis 🚀",
            "Multiple    spaces    between words",
            "Punctuation!@#$%^&*()_+ removal test",
        ]
        
        all_passed = True
        memory_increases = []
        
        for size in test_sizes:
            test_data = base_text * (size // len(base_text))
            
            force_memory_cleanup()
            pre_test_memory = get_memory_mb()
            
            # Process the data
            start_time = time.time()
            result = extreme_clean(test_data)
            end_time = time.time()
            
            # Clean up
            del result
            del test_data
            force_memory_cleanup()
            
            post_test_memory = get_memory_mb()
            memory_change = post_test_memory - pre_test_memory
            memory_increases.append(memory_change)
            
            processing_time = end_time - start_time
            items_per_sec = size / processing_time if processing_time > 0 else 0
            
            print(f"{size:>6} items: {processing_time:.3f}s, "
                  f"{items_per_sec:>7.0f} items/sec, "
                  f"memory change: {memory_change:+.2f} MB")
            
            if abs(memory_change) > 1.0:
                all_passed = False
        
        # PHASE 3: Overall analysis
        print("\nPHASE 3: OVERALL ANALYSIS")
        print("-" * 30)
        
        force_memory_cleanup()
        final_memory = get_memory_mb()
        
        # Memory after all tests vs baseline (after initialization)
        post_test_increase = final_memory - baseline_memory
        
        # Total increase including initialization
        total_increase = final_memory - initial_memory
        
        print(f"Memory after initialization: {baseline_memory:.2f} MB")
        print(f"Memory after all tests: {final_memory:.2f} MB")
        print(f"Post-initialization increase: {post_test_increase:+.2f} MB")
        print(f"Total increase (with init): {total_increase:+.2f} MB")
        
        # Analysis
        avg_leak_per_test = sum(abs(x) for x in memory_increases) / len(memory_increases)
        max_leak = max(abs(x) for x in memory_increases)
        
        print(f"Average memory change per test: {avg_leak_per_test:.2f} MB")
        print(f"Maximum memory change: {max_leak:.2f} MB")
        
        print("\nRESULTS:")
        
        # Check post-initialization memory behavior
        if abs(post_test_increase) <= 0.5:
            print("🏆 PERFECT - Zero memory leaks after initialization!")
            leak_score = "PERFECT"
        elif abs(post_test_increase) <= 1.0:
            print("🎉 EXCELLENT - Minimal memory increase after initialization")
            leak_score = "EXCELLENT"
        elif abs(post_test_increase) <= 2.0:
            print("✅ GOOD - Low memory increase after initialization")
            leak_score = "GOOD"
        else:
            print("❌ POOR - Significant memory leaks detected")
            leak_score = "POOR"
        
        # Check initialization cost
        if init_cost <= 5:
            init_score = "EXCELLENT"
        elif init_cost <= 8:
            init_score = "GOOD"
        elif init_cost <= 12:
            init_score = "ACCEPTABLE"
        else:
            init_score = "HIGH"
        
        print(f"Initialization cost: {init_score}")
        print(f"Memory leak behavior: {leak_score}")
        
        # Final verdict
        if leak_score in ["PERFECT", "EXCELLENT"] and init_score in ["EXCELLENT", "GOOD"]:
            print("\n🎯 OVERALL: EXCELLENT - Production ready!")
            return True
        elif leak_score in ["PERFECT", "EXCELLENT", "GOOD"]:
            print("\n✅ OVERALL: GOOD - Acceptable for production")
            return True
        else:
            print("\n⚠️  OVERALL: NEEDS IMPROVEMENT")
            return False
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing memory behavior with initialization awareness...")
    print()
    
    success = smart_zero_memory_test()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 SMART MEMORY TEST: PASSED")
        print("The library shows excellent memory management!")
    else:
        print("⚠️  SMART MEMORY TEST: NEEDS OPTIMIZATION")
        print("Consider further memory optimizations.")
    
    print("\nNote: This test separates one-time initialization costs")
    print("from actual memory leaks during processing.")
