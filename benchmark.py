#!/usr/bin/env python3
"""
Simple benchmark script to test the memory and performance improvements.
Run this after building the optimized version to see the improvements.
"""
import time
import gc
import sys
import os

def simple_memory_test():
    """Simple test that doesn't require external dependencies."""
    
    # Get memory info using /proc/self/status on Linux
    def get_memory_mb():
        try:
            with open('/proc/self/status', 'r') as f:
                for line in f:
                    if line.startswith('VmRSS:'):
                        # Extract memory in kB and convert to MB
                        mem_kb = int(line.split()[1])
                        return mem_kb / 1024
        except:
            return 0
    
    print("=" * 60)
    print("TEXY MEMORY OPTIMIZATION BENCHMARK")
    print("=" * 60)
    
    # Create test data - reduced size for more realistic testing
    test_data = [
        "Hello world with https://example.com and test@email.com 😊",
        "<p>HTML content with <b>bold</b> text</p>",
        "Text with :) emoticons and 🚀 emojis",
        "Multiple    spaces    and\nnewlines\there",
        "Punctuation!@#$%^&*()_+ removal test",
    ] * 10000  # 50,000 items (more realistic size)
    
    initial_memory = get_memory_mb()
    print(f"Initial memory: {initial_memory:.1f} MB")
    print(f"Test data size: {len(test_data)} items")
    print()
    
    try:
        # Test each pipeline
        from texy.pipelines import relaxed_clean, strict_clean, extreme_clean
        
        # Test 1: Relaxed Clean
        print("Testing relaxed_clean...")
        start_time = time.time()
        start_memory = get_memory_mb()
        
        result = relaxed_clean(test_data)
        
        end_time = time.time()
        peak_memory = get_memory_mb()
        
        del result
        gc.collect()
        after_gc_memory = get_memory_mb()
        
        print(f"  Time: {end_time - start_time:.2f}s")
        print(f"  Peak memory: {peak_memory:.1f} MB (+{peak_memory - start_memory:.1f} MB)")
        print(f"  After cleanup: {after_gc_memory:.1f} MB")
        print(f"  Memory released: {peak_memory - after_gc_memory:.1f} MB")
        print()
        
        # Test 2: Strict Clean
        print("Testing strict_clean...")
        start_time = time.time()
        start_memory = get_memory_mb()
        
        result = strict_clean(test_data)
        
        end_time = time.time()
        peak_memory = get_memory_mb()
        
        del result
        gc.collect()
        after_gc_memory = get_memory_mb()
        
        print(f"  Time: {end_time - start_time:.2f}s")
        print(f"  Peak memory: {peak_memory:.1f} MB (+{peak_memory - start_memory:.1f} MB)")
        print(f"  After cleanup: {after_gc_memory:.1f} MB")
        print(f"  Memory released: {peak_memory - after_gc_memory:.1f} MB")
        print()
        
        # Test 3: Extreme Clean
        print("Testing extreme_clean...")
        start_time = time.time()
        start_memory = get_memory_mb()
        
        result = extreme_clean(test_data)
        
        end_time = time.time()
        peak_memory = get_memory_mb()
        
        del result
        gc.collect()
        after_gc_memory = get_memory_mb()
        
        print(f"  Time: {end_time - start_time:.2f}s")
        print(f"  Peak memory: {peak_memory:.1f} MB (+{peak_memory - start_memory:.1f} MB)")
        print(f"  After cleanup: {after_gc_memory:.1f} MB")
        print(f"  Memory released: {peak_memory - after_gc_memory:.1f} MB")
        print()
        
        # Final cleanup
        del test_data
        gc.collect()
        final_memory = get_memory_mb()
        
        print("=" * 60)
        print("SUMMARY:")
        print(f"Initial memory: {initial_memory:.1f} MB")
        print(f"Final memory: {final_memory:.1f} MB")
        print(f"Net memory change: {final_memory - initial_memory:.1f} MB")
        
        # More realistic thresholds for memory increase
        memory_increase = final_memory - initial_memory
        if memory_increase < 5:  # Less than 5MB increase
            print("✅ MEMORY LEAK TEST PASSED - Excellent memory management")
        elif memory_increase < 10:  # Less than 10MB increase
            print("✅ MEMORY MANAGEMENT GOOD - Acceptable memory increase")  
        elif memory_increase < 15:  # Less than 15MB increase
            print("⚠️  MEMORY MANAGEMENT FAIR - Some memory retention")
        else:
            print("❌ MEMORY LEAK DETECTED - Significant memory not released")
        
        print("=" * 60)
        
    except ImportError as e:
        print(f"Error: Could not import texy module: {e}")
        print("Make sure to build the project first with: maturin develop")
        return False
    except Exception as e:
        print(f"Error during testing: {e}")
        return False
    
    return True

if __name__ == "__main__":
    simple_memory_test()
