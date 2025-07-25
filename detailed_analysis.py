#!/usr/bin/env python3
"""
Memory optimization analysis and comparison for Texy library.
This provides a comprehensive analysis of the memory improvements.
"""
import time
import gc

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

def memory_efficiency_test():
    """Test memory efficiency and provide detailed analysis."""
    print("=" * 70)
    print("TEXY MEMORY OPTIMIZATION - DETAILED ANALYSIS")
    print("=" * 70)
    
    # Test with progressively larger datasets
    base_text = [
        "Hello world with https://example.com and test@email.com 😊",
        "<p>HTML content with <b>bold</b> text</p>",
        "Text with :) emoticons and 🚀 emojis",
        "Multiple    spaces    and\nnewlines\there",
        "Punctuation!@#$%^&*()_+ removal test",
    ]
    
    test_sizes = [1000, 5000, 10000, 25000, 50000]
    results = []
    
    initial_memory = get_memory_mb()
    print(f"Initial memory: {initial_memory:.1f} MB")
    print()
    
    try:
        from texy.pipelines import extreme_clean
        
        print("Testing memory scaling with different dataset sizes:")
        print("-" * 70)
        
        for size in test_sizes:
            test_data = base_text * (size // len(base_text))
            actual_size = len(test_data)
            
            # Pre-test cleanup
            gc.collect()
            start_memory = get_memory_mb()
            start_time = time.time()
            
            # Process
            result = extreme_clean(test_data)
            
            end_time = time.time()
            peak_memory = get_memory_mb()
            
            # Cleanup and measure
            del result
            del test_data
            gc.collect()
            after_memory = get_memory_mb()
            
            # Calculate metrics
            processing_time = end_time - start_time
            memory_used = peak_memory - start_memory
            items_per_second = actual_size / processing_time if processing_time > 0 else 0
            mb_per_1k_items = (memory_used / actual_size * 1000) if actual_size > 0 else 0
            
            results.append({
                'size': actual_size,
                'time': processing_time,
                'memory_used': memory_used,
                'items_per_sec': items_per_second,
                'mb_per_1k': mb_per_1k_items,
                'after_memory': after_memory
            })
            
            print(f"{actual_size:>6} items: {processing_time:.3f}s, "
                  f"{memory_used:>5.1f} MB, {items_per_second:>8.0f} items/sec, "
                  f"{mb_per_1k_items:.2f} MB/1k items")
        
        print("-" * 70)
        
        # Analysis
        final_memory = get_memory_mb()
        total_increase = final_memory - initial_memory
        
        print("\nPERFORMANCE ANALYSIS:")
        avg_items_per_sec = sum(r['items_per_sec'] for r in results) / len(results)
        avg_mb_per_1k = sum(r['mb_per_1k'] for r in results) / len(results)
        
        print(f"Average throughput: {avg_items_per_sec:,.0f} items/second")
        print(f"Average memory efficiency: {avg_mb_per_1k:.3f} MB per 1,000 items")
        print(f"Total memory increase: {total_increase:.1f} MB")
        
        print("\nMEMORY SCALING ANALYSIS:")
        if len(results) >= 2:
            # Check if memory growth is linear vs exponential
            size_ratio = results[-1]['size'] / results[0]['size']
            memory_ratio = results[-1]['memory_used'] / max(results[0]['memory_used'], 0.1)
            
            print(f"Dataset size increased {size_ratio:.1f}x")
            print(f"Memory usage increased {memory_ratio:.1f}x")
            
            if memory_ratio <= size_ratio * 1.2:  # Allow 20% overhead
                print("✅ MEMORY SCALING: LINEAR - Excellent scaling behavior")
            elif memory_ratio <= size_ratio * 2:
                print("⚠️  MEMORY SCALING: ACCEPTABLE - Some overhead but manageable")
            else:
                print("❌ MEMORY SCALING: POOR - Super-linear growth detected")
        
        print("\nMEMORY LEAK ASSESSMENT:")
        
        # Memory increase per item processed
        total_items = sum(r['size'] for r in results)
        leak_per_item = (total_increase / total_items * 1000) if total_items > 0 else 0
        
        print(f"Total items processed: {total_items:,}")
        print(f"Memory increase per 1,000 items: {leak_per_item:.3f} MB")
        
        if leak_per_item < 0.1:  # Less than 0.1 MB per 1k items
            print("✅ MEMORY LEAK: MINIMAL - Excellent memory management")
        elif leak_per_item < 0.2:
            print("✅ MEMORY LEAK: LOW - Good memory management")
        elif leak_per_item < 0.5:
            print("⚠️  MEMORY LEAK: MODERATE - Acceptable for normal use")
        else:
            print("❌ MEMORY LEAK: HIGH - Significant memory retention")
        
        print("\nOVERALL ASSESSMENT:")
        
        # Score based on multiple factors
        performance_score = min(100, avg_items_per_sec / 1000)  # 100k+ items/sec = 100%
        memory_efficiency_score = max(0, 100 - (avg_mb_per_1k * 100))  # Lower is better
        leak_score = max(0, 100 - (leak_per_item * 200))  # Lower is better
        
        overall_score = (performance_score + memory_efficiency_score + leak_score) / 3
        
        print(f"Performance score: {performance_score:.0f}/100")
        print(f"Memory efficiency score: {memory_efficiency_score:.0f}/100") 
        print(f"Memory leak score: {leak_score:.0f}/100")
        print(f"Overall score: {overall_score:.0f}/100")
        
        if overall_score >= 80:
            print("🎉 EXCELLENT - Production ready with great performance!")
        elif overall_score >= 60:
            print("✅ GOOD - Suitable for production use")
        elif overall_score >= 40:
            print("⚠️  ACCEPTABLE - Usable but has room for improvement")
        else:
            print("❌ POOR - Needs significant optimization")
        
        print("=" * 70)
        
        return overall_score >= 60
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = memory_efficiency_test()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
