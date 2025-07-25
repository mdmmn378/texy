#!/usr/bin/env python3
"""
Pinpoint memory leak sources by testing individual components.
"""
import gc
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

def cleanup():
    """Aggressive cleanup."""
    for _ in range(5):
        gc.collect()
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
    except Exception:
        pass

def pinpoint_memory_leaks():
    """Identify specific sources of memory leaks."""
    print("=" * 70)
    print("TEXY MEMORY LEAK PINPOINT ANALYSIS")
    print("=" * 70)
    
    try:
        from texy.texy import extreme_clean, relaxed_clean, strict_clean
        
        # Test data
        test_data = [
            "Hello world with https://example.com and test@email.com 😊",
            "<p>HTML content with <b>bold</b> text</p>",
            "Text with :) emoticons and 🚀 emojis",
            "Multiple    spaces    and\nnewlines\there",
            "Punctuation!@#$%^&*()_+ removal test",
        ] * 1000  # 5000 items
        
        print(f"Test dataset: {len(test_data)} items")
        print()
        
        # Initialize first
        cleanup()
        baseline_memory = get_memory_mb()
        _ = extreme_clean(["init"])
        cleanup()
        post_init_memory = get_memory_mb()
        
        print(f"Baseline memory: {baseline_memory:.2f} MB")
        print(f"After initialization: {post_init_memory:.2f} MB")
        print(f"Initialization cost: {post_init_memory - baseline_memory:.2f} MB")
        print()
        
        # Test each pipeline function
        functions_to_test = [
            ("relaxed_clean", relaxed_clean),
            ("strict_clean", strict_clean), 
            ("extreme_clean", extreme_clean),
        ]
        
        print("INDIVIDUAL FUNCTION ANALYSIS:")
        print("-" * 50)
        
        baseline = post_init_memory
        
        for func_name, func in functions_to_test:
            cleanup()
            pre_memory = get_memory_mb()
            
            # Test the function
            result = func(test_data.copy())
            
            post_memory = get_memory_mb()
            
            # Cleanup
            del result
            cleanup()
            
            final_memory = get_memory_mb()
            
            during_increase = post_memory - pre_memory
            net_increase = final_memory - pre_memory
            
            print(f"{func_name:>12}: +{during_increase:.2f} MB during, +{net_increase:.2f} MB net")
        
        print()
        print("SPECIFIC COMPONENT ANALYSIS:")
        print("-" * 40)
        
        # Test individual operations by examining the pipeline
        pipeline_steps = [
            "remove_newlines",
            "remove_urls", 
            "remove_emails",
            "remove_html",
            "remove_xml",
            "remove_emoticons",
            "remove_emojis",
            "remove_all_punctuations",
            "merge_spaces"
        ]
        
        # Test Python multiprocessing overhead (skip if it hangs)
        try:
            from texy.pipelines import extreme_clean as py_extreme_clean
            
            cleanup()
            pre_py_memory = get_memory_mb()
            
            # Use a smaller dataset to avoid hanging
            small_test = test_data[:100]  # Only 100 items to avoid multiprocessing issues
            result = py_extreme_clean(small_test)
            
            post_py_memory = get_memory_mb()
            del result
            cleanup()
            final_py_memory = get_memory_mb()
            
            py_during = post_py_memory - pre_py_memory
            py_net = final_py_memory - pre_py_memory
            
            print(f"Python multiprocessing (100 items): +{py_during:.2f} MB during, +{py_net:.2f} MB net")
            
        except Exception as e:
            print(f"Python multiprocessing: SKIPPED (blocked or failed: {e})")
            py_during = 0
            py_net = 0
        
        print()
        print("MEMORY LEAK SOURCES IDENTIFIED:")
        print("-" * 35)
        
        # Compare rust vs python versions
        if py_net > net_increase * 1.5:
            print("🔍 PRIMARY LEAK SOURCE: Python multiprocessing overhead")
            print("   - ProcessPoolExecutor creates worker processes")
            print("   - Inter-process communication overhead")
            print("   - Process startup/shutdown costs")
            
        if net_increase > 0.5:
            print("🔍 SECONDARY LEAK SOURCE: Rust PyO3 string conversion")
            print("   - Python string interning")
            print("   - PyO3 reference counting")
            print("   - String allocation overhead")
            
        # Check for specific patterns
        total_final = get_memory_mb()
        total_increase = total_final - baseline_memory
        
        if total_increase > 5:
            print("🔍 ACCUMULATION DETECTED: Memory increases with each test")
            print("   - Static initialization keeps growing")
            print("   - Global state accumulation")
            print("   - Python reference cycles")
        
        print()
        print("RECOMMENDATIONS:")
        print("-" * 15)
        
        if py_net > 3:
            print("1. ✅ Consider disabling multiprocessing for small datasets")
            print("2. ✅ Use direct Rust functions when possible")
            
        if net_increase > 1:
            print("3. ✅ Implement string pooling/reuse")
            print("4. ✅ Force more aggressive garbage collection")
            
        if total_increase > 8:
            print("5. ⚠️  Consider memory-mapped processing for large datasets")
            print("6. ⚠️  Implement manual memory management")
        
        # Final assessment
        print()
        if total_increase < 3:
            print("🏆 LEAK ASSESSMENT: MINIMAL - Production ready!")
        elif total_increase < 6:
            print("✅ LEAK ASSESSMENT: LOW - Acceptable for most use cases")
        elif total_increase < 10:
            print("⚠️  LEAK ASSESSMENT: MODERATE - Monitor in production")
        else:
            print("❌ LEAK ASSESSMENT: HIGH - Needs optimization")
            
        print(f"Total memory increase: {total_increase:.2f} MB")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    pinpoint_memory_leaks()
