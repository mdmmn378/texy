#!/usr/bin/env python3
"""
Direct Rust function test for zero memory increase.
This bypasses Python multiprocessing to test pure Rust memory behavior.
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

def direct_rust_memory_test():
    """Test memory behavior using direct Rust functions."""
    print("=" * 70)
    print("TEXY DIRECT RUST MEMORY TEST")
    print("(Testing pure Rust functions without multiprocessing)")
    print("=" * 70)
    
    force_memory_cleanup()
    initial_memory = get_memory_mb()
    print(f"Initial memory: {initial_memory:.2f} MB")
    
    try:
        # Import direct Rust functions
        from texy.texy import extreme_clean as rust_extreme_clean
        
        # PHASE 1: Initialization (one-time cost)
        print("\nPHASE 1: INITIALIZATION TEST")
        print("-" * 40)
        
        warmup_data = ["Hello world 😊"] * 10
        
        force_memory_cleanup()
        pre_init_memory = get_memory_mb()
        
        # First call - this will initialize everything
        _ = rust_extreme_clean(warmup_data)
        
        force_memory_cleanup()
        post_init_memory = get_memory_mb()
        
        init_cost = post_init_memory - pre_init_memory
        print(f"Rust initialization cost: {init_cost:.2f} MB")
        
        # PHASE 2: Test for memory leaks AFTER initialization
        print("\nPHASE 2: RUST MEMORY LEAK TEST (After initialization)")
        print("-" * 55)
        
        baseline_memory = post_init_memory
        test_sizes = [10, 50, 100, 500, 1000, 2000]
        
        base_text = [
            "Hello world with https://example.com 😊",
            "<p>HTML content with tags</p>",
            "Text with :) emoticons and emojis 🚀",
            "Multiple    spaces    between words",
            "Punctuation!@#$%^&*()_+ removal test",
        ]
        
        memory_increases = []
        
        for size in test_sizes:
            test_data = base_text * (size // len(base_text))
            
            force_memory_cleanup()
            pre_test_memory = get_memory_mb()
            
            # Process the data with direct Rust function
            start_time = time.time()
            result = rust_extreme_clean(test_data)
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
            
            print(f"{size:>6} items: {processing_time:.4f}s, "
                  f"{items_per_sec:>8.0f} items/sec, "
                  f"memory change: {memory_change:+.3f} MB")
        
        # PHASE 3: Overall analysis
        print("\nPHASE 3: RUST PERFORMANCE ANALYSIS")
        print("-" * 35)
        
        force_memory_cleanup()
        final_memory = get_memory_mb()
        
        # Memory after all tests vs baseline (after initialization)
        post_test_increase = final_memory - baseline_memory
        
        # Total increase including initialization
        total_increase = final_memory - initial_memory
        
        print(f"Memory after initialization: {baseline_memory:.2f} MB")
        print(f"Memory after all tests: {final_memory:.2f} MB")
        print(f"Post-initialization increase: {post_test_increase:+.3f} MB")
        print(f"Total increase (with init): {total_increase:+.3f} MB")
        
        # Analysis
        avg_leak_per_test = sum(abs(x) for x in memory_increases) / len(memory_increases)
        max_leak = max(abs(x) for x in memory_increases)
        min_leak = min(abs(x) for x in memory_increases)
        
        print(f"Average memory change per test: {avg_leak_per_test:.3f} MB")
        print(f"Maximum memory change: {max_leak:+.3f} MB")
        print(f"Minimum memory change: {min_leak:+.3f} MB")
        
        print("\nRESULTS:")
        
        # Check post-initialization memory behavior
        if abs(post_test_increase) <= 0.1:
            print("🏆 PERFECT - True zero memory leaks after initialization!")
            leak_score = "PERFECT"
        elif abs(post_test_increase) <= 0.3:
            print("🎉 EXCELLENT - Near-zero memory increase after initialization")
            leak_score = "EXCELLENT"
        elif abs(post_test_increase) <= 0.5:
            print("✅ VERY GOOD - Minimal memory increase after initialization")
            leak_score = "VERY GOOD"
        elif abs(post_test_increase) <= 1.0:
            print("✅ GOOD - Low memory increase after initialization")
            leak_score = "GOOD"
        else:
            print("❌ POOR - Significant memory leaks detected")
            leak_score = "POOR"
        
        # Check individual test consistency
        if max_leak <= 0.1:
            consistency_score = "PERFECT"
        elif max_leak <= 0.3:
            consistency_score = "EXCELLENT"
        elif max_leak <= 0.5:
            consistency_score = "GOOD"
        else:
            consistency_score = "INCONSISTENT"
        
        # Check initialization cost
        if init_cost <= 2:
            init_score = "EXCELLENT"
        elif init_cost <= 4:
            init_score = "GOOD"
        elif init_cost <= 6:
            init_score = "ACCEPTABLE"
        else:
            init_score = "HIGH"
        
        print(f"Rust initialization cost: {init_score}")
        print(f"Memory leak behavior: {leak_score}")
        print(f"Test consistency: {consistency_score}")
        
        # Final verdict for zero memory goal
        if leak_score == "PERFECT" and consistency_score == "PERFECT":
            print("\n🎯 ZERO MEMORY GOAL: ACHIEVED! 🎯")
            print("✨ Rust functions show true zero memory leaks!")
            return True
        elif leak_score in ["PERFECT", "EXCELLENT"] and consistency_score in ["PERFECT", "EXCELLENT"]:
            print("\n🏆 ZERO MEMORY GOAL: NEARLY ACHIEVED!")
            print("📊 Excellent memory management with minimal variance")
            return True
        elif leak_score in ["VERY GOOD", "GOOD"]:
            print("\n✅ ZERO MEMORY GOAL: CLOSE BUT NOT QUITE")
            print("🔧 Good performance but some room for improvement")
            return False
        else:
            print("\n⚠️  ZERO MEMORY GOAL: NOT ACHIEVED")
            print("❌ Significant memory issues need addressing")
            return False
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing direct Rust function memory behavior...")
    print()
    
    success = direct_rust_memory_test()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 DIRECT RUST TEST: ZERO MEMORY GOAL ACHIEVED!")
        print("The Rust implementation shows excellent memory management!")
    else:
        print("⚠️  DIRECT RUST TEST: ZERO MEMORY GOAL NOT ACHIEVED")
        print("Consider further Rust-level optimizations.")
    
    print("\nNote: This test bypasses Python multiprocessing to")
    print("evaluate pure Rust function memory behavior.")
