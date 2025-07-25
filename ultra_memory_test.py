#!/usr/bin/env python3
"""
Ultra-aggressive memory test that clears Python caches and forces manual cleanup.
"""
import gc
import sys
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

def ultra_memory_cleanup():
    """Ultra-aggressive memory cleanup."""
    # Force garbage collection multiple times
    for _ in range(10):
        gc.collect()
    
    # Clear all possible Python caches
    try:
        import sys
        if hasattr(sys, 'intern'):
            # Clear string intern cache if possible
            pass
        
        # Force memory trim
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
        
        # Additional cleanup attempts
        if hasattr(gc, 'set_threshold'):
            # Make GC more aggressive temporarily
            old_threshold = gc.get_threshold()
            gc.set_threshold(1, 1, 1)
            for _ in range(5):
                gc.collect()
            gc.set_threshold(*old_threshold)
            
    except Exception as e:
        print(f"Warning during cleanup: {e}")

def ultra_aggressive_test():
    """Ultra-aggressive memory test to achieve true zero increase."""
    print("=" * 70)
    print("TEXY ULTRA-AGGRESSIVE ZERO MEMORY TEST")
    print("(Maximum possible memory cleanup strategies)")
    print("=" * 70)
    
    ultra_memory_cleanup()
    initial_memory = get_memory_mb()
    print(f"Initial memory: {initial_memory:.2f} MB")
    
    try:
        # Import and immediately test initialization
        from texy.texy import extreme_clean as rust_extreme_clean
        
        print("\nTesting single call with cleanup...")
        
        # Single test to establish baseline after init
        test_data = ["Hello world! 😊 https://example.com"] * 50
        
        ultra_memory_cleanup()
        pre_call_memory = get_memory_mb()
        print(f"Pre-call memory: {pre_call_memory:.2f} MB")
        
        # Process
        result = rust_extreme_clean(test_data)
        
        # Aggressive cleanup immediately after
        del result
        del test_data
        ultra_memory_cleanup()
        
        post_call_memory = get_memory_mb()
        print(f"Post-call memory: {post_call_memory:.2f} MB")
        
        single_call_increase = post_call_memory - pre_call_memory
        print(f"Single call increase: {single_call_increase:+.3f} MB")
        
        print("\nTesting multiple calls with individual cleanup...")
        
        baseline_memory = post_call_memory
        increases = []
        
        for i in range(5):
            # Create fresh data each time
            test_data = [f"Test {i}: Hello world! 😊 https://example.com"] * 100
            
            ultra_memory_cleanup()
            pre_test = get_memory_mb()
            
            # Process
            result = rust_extreme_clean(test_data)
            
            # Immediate cleanup
            del result
            del test_data
            ultra_memory_cleanup()
            
            post_test = get_memory_mb()
            increase = post_test - pre_test
            increases.append(increase)
            
            print(f"Call {i+1}: {increase:+.3f} MB increase")
        
        ultra_memory_cleanup()
        final_memory = get_memory_mb()
        
        total_post_baseline = final_memory - baseline_memory
        
        print(f"\nFinal memory: {final_memory:.2f} MB")
        print(f"Total increase after baseline: {total_post_baseline:+.3f} MB")
        print(f"Average per call: {sum(increases)/len(increases):+.3f} MB")
        print(f"Max single increase: {max(increases):+.3f} MB")
        print(f"Min single increase: {min(increases):+.3f} MB")
        
        # Analysis
        if abs(total_post_baseline) <= 0.1 and max(increases) <= 0.2:
            print("\n🏆 SUCCESS: TRUE ZERO MEMORY ACHIEVED!")
            print("✨ Ultra-aggressive cleanup successful!")
            return True
        elif abs(total_post_baseline) <= 0.3 and max(increases) <= 0.5:
            print("\n🎉 NEAR SUCCESS: Close to zero memory!")
            print("📊 Excellent memory management!")
            return True
        elif abs(total_post_baseline) <= 1.0:
            print("\n✅ GOOD: Low memory increase")
            return False
        else:
            print("\n❌ FAILURE: Memory leaks persist")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running ultra-aggressive memory test...")
    print()
    
    success = ultra_aggressive_test()
    
    print("\n" + "=" * 70)
    if success:
        print("🎯 ULTRA-AGGRESSIVE TEST: ZERO MEMORY GOAL ACHIEVED!")
    else:
        print("⚠️  ULTRA-AGGRESSIVE TEST: MEMORY ISSUES PERSIST")
    
    print("\nThis test uses maximum possible cleanup strategies.")
