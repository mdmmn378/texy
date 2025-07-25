#!/usr/bin/env python3
"""
Zero Memory Increase Benchmark for Texy
This tests if we can achieve zero net memory increase after function calls.
"""
import gc
import time
import ctypes
import os

def get_memory_mb():
    """Get memory in MB using /proc/self/status."""
    try:
        with open('/proc/self/status', 'r') as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    mem_kb = int(line.split()[1])
                    return mem_kb / 1024
    except Exception:
        return 0

def force_memory_cleanup():
    """Aggressively force memory cleanup."""
    # Force multiple garbage collection cycles
    for _ in range(5):
        gc.collect()
    
    # Try to force malloc to release memory back to OS (Linux specific)
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
    except:
        pass

def zero_memory_test():
    """Test for zero memory increase after function calls."""
    print("=" * 70)
    print("TEXY ZERO MEMORY INCREASE TEST")
    print("=" * 70)
    
    # Force initial cleanup
    force_memory_cleanup()
    initial_memory = get_memory_mb()
    
    print(f"Initial memory: {initial_memory:.2f} MB")
    print()
    
    # Test data sizes from small to larger
    test_sizes = [100, 500, 1000, 2000, 5000]
    
    base_text = [
        "Hello world with https://example.com 😊",
        "<p>HTML content</p>",
        "Text with :) emoticons",
        "Multiple    spaces",
        "Punctuation!@#$%",
    ]
    
    try:
        # Import the direct functions (bypassing multiprocessing)
        from texy.texy import extreme_clean as direct_extreme_clean
        
        all_passed = True
        
        for size in test_sizes:
            print(f"Testing with {size} items...")
            
            # Create test data
            test_data = base_text * (size // len(base_text))
            
            # Force cleanup before test
            force_memory_cleanup()
            pre_test_memory = get_memory_mb()
            
            # Call the Rust function directly
            start_time = time.time()
            result = direct_extreme_clean(test_data)
            end_time = time.time()
            
            # Measure immediately after
            post_call_memory = get_memory_mb()
            
            # Clean up result and test data
            del result
            del test_data
            force_memory_cleanup()
            
            # Final memory measurement
            post_cleanup_memory = get_memory_mb()
            
            # Calculate metrics
            processing_time = end_time - start_time
            memory_during = post_call_memory - pre_test_memory
            memory_after = post_cleanup_memory - pre_test_memory
            
            print(f"  Time: {processing_time:.3f}s")
            print(f"  Memory during call: +{memory_during:.2f} MB")
            print(f"  Memory after cleanup: +{memory_after:.2f} MB")
            
            # Check for zero memory increase (allow tiny tolerance)
            if abs(memory_after) <= 0.1:  # Allow 0.1 MB tolerance
                print(f"  ✅ PERFECT - Zero memory increase!")
            elif abs(memory_after) <= 0.5:  # Allow 0.5 MB tolerance
                print(f"  ✅ EXCELLENT - Minimal memory increase")
            elif abs(memory_after) <= 1.0:  # Allow 1 MB tolerance
                print(f"  ⚠️  GOOD - Small memory increase")
            else:
                print(f"  ❌ POOR - Significant memory increase")
                all_passed = False
            
            print()
        
        # Final overall test
        force_memory_cleanup()
        final_memory = get_memory_mb()
        total_increase = final_memory - initial_memory
        
        print("=" * 70)
        print("OVERALL ZERO MEMORY TEST:")
        print(f"Initial memory: {initial_memory:.2f} MB")
        print(f"Final memory: {final_memory:.2f} MB")
        print(f"Total net change: {total_increase:+.2f} MB")
        
        if abs(total_increase) <= 0.1:
            print("🏆 PERFECT - Achieved zero memory increase!")
            success_level = "PERFECT"
        elif abs(total_increase) <= 0.5:
            print("🎉 EXCELLENT - Near-zero memory increase!")
            success_level = "EXCELLENT"
        elif abs(total_increase) <= 1.0:
            print("✅ VERY GOOD - Minimal memory increase")
            success_level = "VERY GOOD"
        elif abs(total_increase) <= 2.0:
            print("✅ GOOD - Low memory increase")
            success_level = "GOOD"
        else:
            print("❌ NEEDS IMPROVEMENT - Memory increase detected")
            success_level = "NEEDS IMPROVEMENT"
            all_passed = False
        
        print("=" * 70)
        
        return success_level in ["PERFECT", "EXCELLENT", "VERY GOOD"]
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing for zero memory increase after Rust function calls...")
    print()
    
    success = zero_memory_test()
    
    if success:
        print("\n🎯 ZERO MEMORY TEST: PASSED")
    else:
        print("\n⚠️  ZERO MEMORY TEST: NEEDS OPTIMIZATION")
    
    print("\nNote: This test aims for zero net memory increase.")
    print("Small increases (<1MB) may be acceptable depending on use case.")
