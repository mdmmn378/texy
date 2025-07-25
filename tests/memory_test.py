#!/usr/bin/env python3
"""
Memory profiling script to test and demonstrate memory leak fixes.
"""
import gc
import psutil
import os
import time
from memory_profiler import profile
from typing import List

def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

@profile
def test_memory_leak_fix():
    """Test the memory usage with large text arrays."""
    
    # Test data - simulate real-world text processing
    base_texts = [
        "Hello, this is a sample text with\nnewlines and various 😊 emojis 🚀.",
        "Visit https://example.com for more information about our services!",
        "Send your feedback to feedback@example.com and we'll get back to you.",
        "<p>This is an HTML paragraph with <b>bold</b> and <i>italic</i> tags.</p>",
        "<xml>This is some XML content with nested <tag>elements</tag>.</xml>",
        "😃 Text with emoticons :) :( :D and emojis 😊 🚀 ⭐ that need removal.",
        "This text has infrequent punctuations: !@#$%^&*()_+{}|:<>?[];',./",
        "Multiple      spaces     between   words    that    need    cleanup.",
        "Mixed content with URLs like http://test.com and emails like test@domain.com",
        "Newlines\nand\ttabs\tand other\rwhitespace characters to normalize."
    ]
    
    # Create a large dataset
    large_data = base_texts * 50000  # 500,000 items
    
    print(f"Initial memory usage: {get_memory_usage():.2f} MB")
    print(f"Processing {len(large_data)} text items...")
    
    # Import here to avoid import issues during module loading
    from texy.pipelines import extreme_clean, strict_clean, relaxed_clean
    
    start_time = time.time()
    memory_before = get_memory_usage()
    
    # Test extreme cleaning
    result_extreme = extreme_clean(large_data)
    memory_after_extreme = get_memory_usage()
    
    print(f"Extreme clean completed in {time.time() - start_time:.2f}s")
    print(f"Memory after extreme_clean: {memory_after_extreme:.2f} MB")
    print(f"Memory increase: {memory_after_extreme - memory_before:.2f} MB")
    
    # Clear results and force garbage collection
    del result_extreme
    gc.collect()
    memory_after_gc = get_memory_usage()
    print(f"Memory after garbage collection: {memory_after_gc:.2f} MB")
    
    # Test strict cleaning
    start_time = time.time()
    result_strict = strict_clean(large_data)
    memory_after_strict = get_memory_usage()
    
    print(f"Strict clean completed in {time.time() - start_time:.2f}s")
    print(f"Memory after strict_clean: {memory_after_strict:.2f} MB")
    
    # Clear results
    del result_strict
    gc.collect()
    memory_after_gc2 = get_memory_usage()
    print(f"Memory after second garbage collection: {memory_after_gc2:.2f} MB")
    
    # Test relaxed cleaning
    start_time = time.time()
    result_relaxed = relaxed_clean(large_data)
    memory_after_relaxed = get_memory_usage()
    
    print(f"Relaxed clean completed in {time.time() - start_time:.2f}s")
    print(f"Memory after relaxed_clean: {memory_after_relaxed:.2f} MB")
    
    # Final cleanup
    del result_relaxed
    del large_data
    gc.collect()
    
    final_memory = get_memory_usage()
    print(f"Final memory usage: {final_memory:.2f} MB")
    
    return final_memory

if __name__ == "__main__":
    print("Testing memory usage with optimized texy library...")
    test_memory_leak_fix()
