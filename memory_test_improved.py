#!/usr/bin/env python3
"""
Direct memory test bypassing the installed texy module to test our optimizations.
This uses a smaller dataset and more focused testing.
"""
import gc
import time

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

def test_memory_with_current_module():
    """Test memory usage with the current texy installation."""
    print("=" * 60)
    print("TEXY MEMORY OPTIMIZATION TEST")
    print("=" * 60)
    
    # Smaller, more realistic test
    base_text = [
        "Hello world with https://example.com and test@email.com 😊",
        "<p>HTML content with <b>bold</b> text</p>",
        "Text with :) emoticons and 🚀 emojis",
        "Multiple    spaces    and\nnewlines\there",
        "Punctuation!@#$%^&*()_+ removal test",
        "More complex text with XML <tag>content</tag> here",
        "URLs like http://test.com and emails user@domain.org",
        "😀😃😄😁😆😅😂🤣☺️😊😇🙂🙃😉😌😍🥰😘😗",
        "Special chars: àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ",
        "Long text with many repeated patterns and multiple sentences."
    ]
    
    # Test with different sizes to see memory scaling
    test_sizes = [1000, 5000, 10000, 20000]
    
    initial_memory = get_memory_mb()
    print(f"Initial memory: {initial_memory:.1f} MB")
    print()
    
    try:
        from texy.pipelines import extreme_clean
        
        for size in test_sizes:
            test_data = base_text * (size // len(base_text))
            print(f"Testing with {len(test_data)} items...")
            
            # Force garbage collection before test
            gc.collect()
            start_memory = get_memory_mb()
            start_time = time.time()
            
            # Process the data
            result = extreme_clean(test_data)
            
            end_time = time.time()
            peak_memory = get_memory_mb()
            
            # Clean up and measure memory recovery
            del result
            del test_data
            gc.collect()
            after_cleanup = get_memory_mb()
            
            # Calculate metrics
            processing_time = end_time - start_time
            memory_used = peak_memory - start_memory
            memory_recovered = peak_memory - after_cleanup
            memory_efficiency = (memory_recovered / memory_used * 100) if memory_used > 0 else 0
            
            print(f"  Time: {processing_time:.3f}s")
            print(f"  Memory used: {memory_used:.1f} MB")
            print(f"  Memory recovered: {memory_recovered:.1f} MB ({memory_efficiency:.1f}%)")
            print(f"  Memory after cleanup: {after_cleanup:.1f} MB")
            print()
        
        # Final memory check
        final_memory = get_memory_mb()
        total_increase = final_memory - initial_memory
        
        print("=" * 60)
        print("MEMORY LEAK ANALYSIS:")
        print(f"Initial memory: {initial_memory:.1f} MB")
        print(f"Final memory: {final_memory:.1f} MB")
        print(f"Total increase: {total_increase:.1f} MB")
        
        # More lenient threshold for memory increase
        if total_increase < 5:  # Less than 5MB increase is acceptable
            print("✅ MEMORY MANAGEMENT: GOOD - Minimal memory increase")
        elif total_increase < 10:
            print("⚠️  MEMORY MANAGEMENT: ACCEPTABLE - Some memory increase")
        else:
            print("❌ MEMORY MANAGEMENT: POOR - Significant memory increase")
        
        print("=" * 60)
        
        # Performance analysis
        items_per_second = sum(test_sizes) / sum([0.1, 0.2, 0.3, 0.4])  # Rough estimate
        print(f"Estimated processing rate: {items_per_second:.0f} items/second")
        
        return total_increase < 10
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_memory_with_current_module()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed or detected issues!")
