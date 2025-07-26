#!/usr/bin/env python3
"""
Simple Memory Leak Detection Script for Texy Library

This script tests memory usage with varying sample sizes to detect potential memory leaks.
Tests with 1M, 500K, 100K, and 10K samples to observe memory release patterns.
"""

import gc
import os
import psutil
import time
import sys
from typing import Dict


class SimpleMemoryTracker:
    """Simple memory tracking utility."""
    
    def __init__(self):
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)
        
    def get_memory_mb(self) -> float:
        """Get current RSS memory usage in MB."""
        return self.process.memory_info().rss / 1024 / 1024
    
    def get_memory_info(self) -> Dict[str, float]:
        """Get detailed memory information."""
        memory_info = self.process.memory_info()
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'percent': self.process.memory_percent()
        }
    
    def force_cleanup(self):
        """Force garbage collection."""
        for i in range(3):
            collected = gc.collect()
            print(f"    GC round {i+1}: collected {collected} objects")
            time.sleep(0.1)


def create_hard_to_clean_text() -> str:
    """Create a complex text sample that's challenging to process."""
    return """
    🌟 COMPLEX TEXT SAMPLE FOR MEMORY TESTING 🌟
    
    This sample contains various challenging elements:
    
    📧 Emails: test@example.com, user.name+tag@domain.org, admin@company.co.uk
    🔗 URLs: https://example.com/path?param=value&other=123#section
    😊 Emojis: 😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 😇
    :) Emoticons: :) :( :D :P :o ;) :'( >:( :| :-) :-( :-D :-P :o) ;-) 8-)
    
    <html>
    <head><title>Test HTML</title></head>
    <body>
        <div class="container">
            <p>Paragraph with <b>bold</b>, <i>italic</i>, and <a href="#">links</a></p>
            <ul><li>Item 1</li><li>Item 2</li></ul>
        </div>
    </body>
    </html>
    
    <xml version="1.0">
        <root>
            <item id="1" type="test">
                <content>Nested XML content</content>
                <metadata>
                    <author>Test User</author>
                    <date>2024-01-01</date>
                </metadata>
            </item>
        </root>
    </xml>
    
    Special characters: !@#$%^&*()_+-={}[]|\\:";'<>?,./ ~`
    Unicode text: café naïve résumé jalapeño piñata Москва 北京 العربية
    
    Multiple      spaces     and\t\ttabs\nand\nnewlines\r\rcarriage\freturns
    
    Numbers and currencies: $1,234.56 €999.99 £500.00 ¥10000 ₹5000.50
    
    Code blocks:
    ```python
    def memory_intensive_function():
        data = [i for i in range(1000000)]
        return sum(data)
    ```
    
    Markdown: # Header ## Subheader **bold** *italic* `code` [link](url)
    
    Very long words: pneumonoultramicroscopicsilicovolcanoconiosis
    Repeated patterns: abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()
    
    This text is designed to be memory-intensive and challenging to process,
    containing nested structures, complex Unicode, special characters, and
    patterns that could potentially expose memory leaks in text processing.
    """


def test_sample_size(tracker: SimpleMemoryTracker, sample_size: int) -> Dict:
    """Test memory usage with a specific sample size."""
    print(f"\n{'='*70}")
    print(f"TESTING WITH {sample_size:,} SAMPLES (PID: {tracker.pid})")
    print(f"{'='*70}")
    
    # Get initial memory
    initial_memory = tracker.get_memory_info()
    print(f"Initial Memory: RSS={initial_memory['rss_mb']:.2f} MB, "
          f"VMS={initial_memory['vms_mb']:.2f} MB, "
          f"Percent={initial_memory['percent']:.2f}%")
    
    # Create test data
    print(f"Creating {sample_size:,} text samples...")
    base_text = create_hard_to_clean_text()
    start_time = time.time()
    test_data = [base_text] * sample_size
    creation_time = time.time() - start_time
    
    after_creation_memory = tracker.get_memory_info()
    print(f"After creation: RSS={after_creation_memory['rss_mb']:.2f} MB "
          f"(+{after_creation_memory['rss_mb'] - initial_memory['rss_mb']:.2f} MB) "
          f"in {creation_time:.2f}s")
    
    results = {
        'sample_size': sample_size,
        'creation_time': creation_time,
        'initial_memory': initial_memory,
        'after_creation_memory': after_creation_memory
    }
    
    # Try to import and test texy functions
    try:
        # Add current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from texy.pipelines import extreme_clean, strict_clean, relaxed_clean
        
        # Test extreme_clean
        print("\n--- Testing extreme_clean ---")
        before_memory = tracker.get_memory_mb()
        start_time = time.time()
        result_extreme = extreme_clean(test_data)
        end_time = time.time()
        after_memory = tracker.get_memory_mb()
        
        duration = end_time - start_time
        rate = sample_size / duration if duration > 0 else 0
        
        print(f"Duration: {duration:.2f}s, Rate: {rate:,.0f} items/sec")
        print(f"Memory before: {before_memory:.2f} MB, after: {after_memory:.2f} MB "
              f"(+{after_memory - before_memory:.2f} MB)")
        print(f"Output size: {len(result_extreme) if result_extreme else 0:,}")
        
        results['extreme_clean'] = {
            'duration': duration,
            'rate': rate,
            'memory_before': before_memory,
            'memory_after': after_memory,
            'output_size': len(result_extreme) if result_extreme else 0
        }
        
        # Cleanup
        del result_extreme
        print("Cleaning up extreme_clean result...")
        tracker.force_cleanup()
        cleanup_memory = tracker.get_memory_mb()
        print(f"Memory after cleanup: {cleanup_memory:.2f} MB")
        
        # Test strict_clean
        print("\n--- Testing strict_clean ---")
        before_memory = tracker.get_memory_mb()
        start_time = time.time()
        result_strict = strict_clean(test_data)
        end_time = time.time()
        after_memory = tracker.get_memory_mb()
        
        duration = end_time - start_time
        rate = sample_size / duration if duration > 0 else 0
        
        print(f"Duration: {duration:.2f}s, Rate: {rate:,.0f} items/sec")
        print(f"Memory before: {before_memory:.2f} MB, after: {after_memory:.2f} MB "
              f"(+{after_memory - before_memory:.2f} MB)")
        print(f"Output size: {len(result_strict) if result_strict else 0:,}")
        
        results['strict_clean'] = {
            'duration': duration,
            'rate': rate,
            'memory_before': before_memory,
            'memory_after': after_memory,
            'output_size': len(result_strict) if result_strict else 0
        }
        
        # Cleanup
        del result_strict
        print("Cleaning up strict_clean result...")
        tracker.force_cleanup()
        cleanup_memory = tracker.get_memory_mb()
        print(f"Memory after cleanup: {cleanup_memory:.2f} MB")
        
        # Test relaxed_clean
        print("\n--- Testing relaxed_clean ---")
        before_memory = tracker.get_memory_mb()
        start_time = time.time()
        result_relaxed = relaxed_clean(test_data)
        end_time = time.time()
        after_memory = tracker.get_memory_mb()
        
        duration = end_time - start_time
        rate = sample_size / duration if duration > 0 else 0
        
        print(f"Duration: {duration:.2f}s, Rate: {rate:,.0f} items/sec")
        print(f"Memory before: {before_memory:.2f} MB, after: {after_memory:.2f} MB "
              f"(+{after_memory - before_memory:.2f} MB)")
        print(f"Output size: {len(result_relaxed) if result_relaxed else 0:,}")
        
        results['relaxed_clean'] = {
            'duration': duration,
            'rate': rate,
            'memory_before': before_memory,
            'memory_after': after_memory,
            'output_size': len(result_relaxed) if result_relaxed else 0
        }
        
        # Cleanup
        del result_relaxed
        print("Cleaning up relaxed_clean result...")
        tracker.force_cleanup()
        
    except ImportError as e:
        print(f"WARNING: Could not import texy functions: {e}")
        print("This might be expected if texy is not installed or built yet.")
    
    # Final cleanup
    print("\n--- Final cleanup ---")
    del test_data
    del base_text
    print("Performing aggressive cleanup...")
    tracker.force_cleanup()
    
    final_memory = tracker.get_memory_info()
    print(f"Final Memory: RSS={final_memory['rss_mb']:.2f} MB, "
          f"VMS={final_memory['vms_mb']:.2f} MB, "
          f"Percent={final_memory['percent']:.2f}%")
    
    # Calculate memory efficiency
    memory_growth = final_memory['rss_mb'] - initial_memory['rss_mb']
    print(f"Net memory growth: {memory_growth:+.2f} MB")
    
    results['final_memory'] = final_memory
    results['memory_growth'] = memory_growth
    results['memory_efficient'] = abs(memory_growth) < 50  # Allow 50MB variance
    
    return results


def main():
    """Run the memory leak detection test."""
    print("="*80)
    print("MEMORY LEAK DETECTION FOR TEXY LIBRARY")
    print("="*80)
    
    # System information
    system_memory = psutil.virtual_memory()
    print(f"System Memory: {system_memory.total / 1024**3:.2f} GB total, "
          f"{system_memory.available / 1024**3:.2f} GB available")
    print(f"Python: {sys.version}")
    
    tracker = SimpleMemoryTracker()
    print(f"Process PID: {tracker.pid}")
    
    # Initial system state
    initial_system_memory = tracker.get_memory_mb()
    print(f"Initial process memory: {initial_system_memory:.2f} MB")
    
    # Test with different sample sizes
    sample_sizes = [1_000_000, 500_000, 100_000, 10_000]
    all_results = []
    
    for sample_size in sample_sizes:
        try:
            print(f"\nStarting test with {sample_size:,} samples...")
            results = test_sample_size(tracker, sample_size)
            all_results.append(results)
            
            # Brief pause between tests
            print("Waiting 3 seconds before next test...")
            time.sleep(3)
            
        except Exception as e:
            print(f"ERROR during {sample_size:,} sample test: {e}")
            # Force cleanup on error
            tracker.force_cleanup()
    
    # Final system cleanup
    print("\n" + "="*80)
    print("PERFORMING FINAL SYSTEM CLEANUP")
    print("="*80)
    
    for i in range(5):
        collected = gc.collect()
        print(f"Final GC round {i+1}: collected {collected} objects")
        time.sleep(3)
    
    final_system_memory = tracker.get_memory_mb()
    total_memory_growth = final_system_memory - initial_system_memory
    
    # Generate summary report
    print("\n" + "="*80)
    print("MEMORY LEAK DETECTION SUMMARY")
    print("="*80)
    
    print(f"Initial Process Memory: {initial_system_memory:.2f} MB")
    print(f"Final Process Memory: {final_system_memory:.2f} MB")
    print(f"Total Memory Growth: {total_memory_growth:+.2f} MB")

    # Determine if there's a memory leak
    leak_threshold = 100  # MB
    has_leak = total_memory_growth > leak_threshold
    
    print(f"Memory Leak Status: {'🚨 DETECTED' if has_leak else '✅ ACCEPTABLE'}")
    print(f"Leak Threshold: {leak_threshold} MB")
    
    # Performance summary
    if all_results:
        print(f"\n{'='*60}")
        print("PERFORMANCE SUMMARY BY SAMPLE SIZE")
        print(f"{'='*60}")
        
        for result in all_results:
            print(f"\n📊 Sample Size: {result['sample_size']:,}")
            print(f"   Creation: {result['creation_time']:.2f}s")
            print(f"   Memory Growth: {result['memory_growth']:+.2f} MB")
            print(f"   Memory Efficient: {'✅' if result['memory_efficient'] else '❌'}")
            
            # Show function performance if available
            for func_name in ['extreme_clean', 'strict_clean', 'relaxed_clean']:
                if func_name in result:
                    func_result = result[func_name]
                    print(f"   {func_name}: {func_result['duration']:.2f}s, "
                          f"{func_result['rate']:,.0f} items/sec")
    
    # Add explanation of memory patterns
    print(f"\n{'='*80}")
    print("UNDERSTANDING MEMORY PATTERNS")
    print(f"{'='*80}")
    
    print("""
💡 Memory Growth Patterns Explained:

Large Sample Sizes (1M, 500K):
- Higher initial memory growth due to data creation
- ProcessPool: Lower measured growth (worker memory isolated)
- ThreadPool: Higher measured growth (shared memory space)

Small Sample Sizes (100K, 10K):  
- Lower data creation overhead
- Better memory reuse from previous allocations
- ThreadPool benefits from shared memory efficiency

Memory Efficiency Factors:
✅ Good: Growth < 50MB per test (reusing allocated memory)
❌ Poor: Growth > 50MB per test (potential memory fragmentation)

Performance vs Memory Trade-offs:
- ThreadPool: Faster for small datasets, higher memory visibility
- ProcessPool: More stable memory patterns, process isolation overhead
- Sequential: Baseline performance, most predictable memory usage
""")

    print(f"\n{'='*80}")
    print(f"FINAL VERDICT: {'MEMORY LEAK DETECTED' if has_leak else 'NO SIGNIFICANT MEMORY LEAK'}")
    print(f"{'='*80}")
    
    return not has_leak


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
