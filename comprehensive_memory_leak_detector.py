#!/usr/bin/env python3
"""
Comprehensive Memory Leak Detection Script for Texy Library

This script tests memory usage with varying sample sizes to detect potential memory leaks.
It tests with 1M, 500K, 100K, and 10K samples to observe if memory is properly released.
"""

import gc
import os
import psutil
import time
import sys
from typing import List, Dict, Any
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class MemorySnapshot:
    """Data class to store memory usage information."""
    timestamp: float
    rss_mb: float
    vms_mb: float
    percent: float
    available_mb: float
    pid: int


class MemoryTracker:
    """Enhanced memory tracking with PID monitoring."""
    
    def __init__(self):
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)
        self.snapshots: List[MemorySnapshot] = []
        
    def take_snapshot(self, label: str = "") -> MemorySnapshot:
        """Take a memory snapshot with current usage."""
        memory_info = self.process.memory_info()
        memory_percent = self.process.memory_percent()
        system_memory = psutil.virtual_memory()
        
        snapshot = MemorySnapshot(
            timestamp=time.time(),
            rss_mb=memory_info.rss / 1024 / 1024,
            vms_mb=memory_info.vms / 1024 / 1024,
            percent=memory_percent,
            available_mb=system_memory.available / 1024 / 1024,
            pid=self.pid
        )
        
        self.snapshots.append(snapshot)
        
        if label:
            print(f"[{label}] PID: {snapshot.pid}, RSS: {snapshot.rss_mb:.2f} MB, "
                  f"VMS: {snapshot.vms_mb:.2f} MB, Percent: {snapshot.percent:.2f}%, "
                  f"Available: {snapshot.available_mb:.2f} MB")
        
        return snapshot
    
    def get_memory_difference(self, start_snapshot: MemorySnapshot, end_snapshot: MemorySnapshot) -> Dict[str, float]:
        """Calculate memory difference between two snapshots."""
        return {
            'rss_diff_mb': end_snapshot.rss_mb - start_snapshot.rss_mb,
            'vms_diff_mb': end_snapshot.vms_mb - start_snapshot.vms_mb,
            'percent_diff': end_snapshot.percent - start_snapshot.percent,
            'time_elapsed': end_snapshot.timestamp - start_snapshot.timestamp
        }
    
    def force_cleanup(self, iterations: int = 3):
        """Force garbage collection multiple times."""
        for i in range(iterations):
            collected = gc.collect()
            print(f"  GC iteration {i+1}: collected {collected} objects")
            time.sleep(0.1)  # Small delay between collections


@contextmanager
def memory_context(tracker: MemoryTracker, label: str):
    """Context manager for memory tracking."""
    print(f"\n--- Starting {label} ---")
    start_snapshot = tracker.take_snapshot(f"{label} - START")
    
    try:
        yield start_snapshot
    finally:
        end_snapshot = tracker.take_snapshot(f"{label} - END")
        diff = tracker.get_memory_difference(start_snapshot, end_snapshot)
        
        print(f"Memory Change: RSS: {diff['rss_diff_mb']:+.2f} MB, "
              f"VMS: {diff['vms_diff_mb']:+.2f} MB, "
              f"Percent: {diff['percent_diff']:+.2f}%, "
              f"Time: {diff['time_elapsed']:.2f}s")


def create_test_data() -> str:
    """Create a single complex text sample for duplication."""
    return """
    This is a comprehensive test text with multiple challenging elements:
    
    1. URLs: https://example.com, http://test.org, ftp://files.server.com
    2. Emails: test@domain.com, user.name+tag@example.org, admin@sub.domain.co.uk
    3. Emojis: 😊 🚀 ⭐ 💫 🌟 ✨ 🎉 🎊 🔥 💯 ❤️ 💙 💚 💛 💜 🧡
    4. Emoticons: :) :( :D :P :o ;) :'( >:( :| :-) :-( :-D :-P
    5. HTML: <p>Paragraph with <b>bold</b>, <i>italic</i>, <a href="link">anchor</a></p>
    6. XML: <root><item id="1">Content</item><nested><deep>value</deep></nested></root>
    7. Special chars: !@#$%^&*()_+-={}[]|\\:";'<>?,./ ~`
    8. Unicode: café naïve résumé jalapeño piñata
    9. Whitespace: Multiple     spaces\t\ttabs\n\nnewlines\r\rcarriage returns
    10. Numbers: 123.456 -789 +999 1,000,000 $500.99 €250.50 £100.75
    11. Markdown: # Header ## Subheader **bold** *italic* `code` [link](url)
    12. Code blocks: ```python\ndef hello():\n    print("world")\n```
    13. Mixed languages: Hello Hola Bonjour Guten Tag こんにちは 你好 مرحبا
    14. Long words: pneumonoultramicroscopicsilicovolcanoconiosispneumonoultramicroscopic
    15. Repeated patterns: ababababab cdcdcdcdcd efefefefefef ghghghghgh
    
    This text is designed to stress test the text processing pipeline with various
    edge cases and challenging content that might cause memory leaks or inefficient
    processing. It contains nested structures, complex Unicode, and patterns that
    could potentially cause issues in regex processing or string manipulation.
    """


def test_memory_with_sample_size(tracker: MemoryTracker, sample_size: int) -> Dict[str, Any]:
    """Test memory usage with a specific sample size."""
    print(f"\n{'='*60}")
    print(f"TESTING WITH {sample_size:,} SAMPLES")
    print(f"{'='*60}")
    
    # Create test data
    base_text = create_test_data()
    
    with memory_context(tracker, f"Data Creation ({sample_size:,})"):
        test_data = [base_text] * sample_size
        data_creation_snapshot = tracker.take_snapshot("After data creation")
    
    results = {}
    
    # Import texy functions
    try:
        import sys
        sys.path.insert(0, '/home/mamun/projects/synced/open-source/texy')
        from texy.pipelines import extreme_clean, strict_clean, relaxed_clean
    except ImportError as e:
        print(f"ERROR: Could not import texy functions: {e}")
        print("Make sure texy is installed or the path is correct.")
        return {}
    
    # Test extreme_clean
    with memory_context(tracker, f"Extreme Clean ({sample_size:,})"):
        start_time = time.time()
        result_extreme = extreme_clean(test_data)
        end_time = time.time()
        
        results['extreme_clean'] = {
            'duration': end_time - start_time,
            'input_size': len(test_data),
            'output_size': len(result_extreme) if result_extreme else 0,
            'processing_rate': sample_size / (end_time - start_time)
        }
        
        # Clean up result
        del result_extreme
        tracker.force_cleanup()
        tracker.take_snapshot("After extreme_clean cleanup")
    
    # Test strict_clean
    with memory_context(tracker, f"Strict Clean ({sample_size:,})"):
        start_time = time.time()
        result_strict = strict_clean(test_data)
        end_time = time.time()
        
        results['strict_clean'] = {
            'duration': end_time - start_time,
            'input_size': len(test_data),
            'output_size': len(result_strict) if result_strict else 0,
            'processing_rate': sample_size / (end_time - start_time)
        }
        
        # Clean up result
        del result_strict
        tracker.force_cleanup()
        tracker.take_snapshot("After strict_clean cleanup")
    
    # Test relaxed_clean
    with memory_context(tracker, f"Relaxed Clean ({sample_size:,})"):
        start_time = time.time()
        result_relaxed = relaxed_clean(test_data)
        end_time = time.time()
        
        results['relaxed_clean'] = {
            'duration': end_time - start_time,
            'input_size': len(test_data),
            'output_size': len(result_relaxed) if result_relaxed else 0,
            'processing_rate': sample_size / (end_time - start_time)
        }
        
        # Clean up result
        del result_relaxed
        tracker.force_cleanup()
        tracker.take_snapshot("After relaxed_clean cleanup")
    
    # Final cleanup
    with memory_context(tracker, f"Final Cleanup ({sample_size:,})"):
        del test_data
        del base_text
        tracker.force_cleanup(5)  # More aggressive cleanup
        final_snapshot = tracker.take_snapshot("After final cleanup")
    
    # Calculate memory efficiency
    results['memory_analysis'] = {
        'peak_rss_mb': max(s.rss_mb for s in tracker.snapshots[-10:]),  # Last 10 snapshots
        'final_rss_mb': final_snapshot.rss_mb,
        'data_creation_rss_mb': data_creation_snapshot.rss_mb,
        'memory_efficiency': final_snapshot.rss_mb <= data_creation_snapshot.rss_mb + 50  # Allow 50MB variance
    }
    
    return results


def run_comprehensive_memory_test():
    """Run the comprehensive memory leak detection test."""
    print("="*80)
    print("COMPREHENSIVE MEMORY LEAK DETECTION FOR TEXY LIBRARY")
    print("="*80)
    
    # Display system information
    system_info = psutil.virtual_memory()
    print(f"System Memory: Total: {system_info.total / 1024**3:.2f} GB, "
          f"Available: {system_info.available / 1024**3:.2f} GB")
    print(f"Python Version: {sys.version}")
    print(f"Process PID: {os.getpid()}")
    
    tracker = MemoryTracker()
    initial_snapshot = tracker.take_snapshot("Initial State")
    
    # Test with different sample sizes
    sample_sizes = [1_000_000, 500_000, 100_000, 10_000]
    all_results = {}
    
    for sample_size in sample_sizes:
        try:
            results = test_memory_with_sample_size(tracker, sample_size)
            all_results[sample_size] = results
            
            # Wait between tests to allow system to stabilize
            print("\nWaiting 5 seconds before next test...")
            time.sleep(5)
            
        except Exception as e:
            print(f"ERROR during test with {sample_size:,} samples: {e}")
            tracker.force_cleanup(5)
            continue
    
    # Final system cleanup
    tracker.force_cleanup(10)
    final_snapshot = tracker.take_snapshot("Final State")
    
    # Generate summary report
    print(f"\n{'='*80}")
    print("MEMORY LEAK DETECTION SUMMARY")
    print(f"{'='*80}")
    
    initial_memory = initial_snapshot.rss_mb
    final_memory = final_snapshot.rss_mb
    memory_growth = final_memory - initial_memory
    
    print(f"Initial Memory (RSS): {initial_memory:.2f} MB")
    print(f"Final Memory (RSS): {final_memory:.2f} MB")
    print(f"Net Memory Growth: {memory_growth:+.2f} MB")
    print(f"Memory Leak Status: {'DETECTED' if memory_growth > 100 else 'ACCEPTABLE'}")
    
    # Performance summary
    print(f"\n{'='*60}")
    print("PERFORMANCE SUMMARY")
    print(f"{'='*60}")
    
    for sample_size, results in all_results.items():
        if not results:
            continue
            
        print(f"\nSample Size: {sample_size:,}")
        print("-" * 40)
        
        for function_name, metrics in results.items():
            if function_name == 'memory_analysis':
                continue
                
            print(f"  {function_name}:")
            print(f"    Duration: {metrics['duration']:.2f}s")
            print(f"    Rate: {metrics['processing_rate']:,.0f} items/sec")
            print(f"    Output Size: {metrics['output_size']:,}")
        
        if 'memory_analysis' in results:
            memory_analysis = results['memory_analysis']
            print("  Memory Analysis:")
            print(f"    Peak RSS: {memory_analysis['peak_rss_mb']:.2f} MB")
            print(f"    Final RSS: {memory_analysis['final_rss_mb']:.2f} MB")
            print(f"    Memory Efficient: {memory_analysis['memory_efficiency']}")
    
    # Memory trend analysis
    print(f"\n{'='*60}")
    print("MEMORY TREND ANALYSIS")
    print(f"{'='*60}")
    
    rss_values = [s.rss_mb for s in tracker.snapshots]
    if len(rss_values) > 1:
        trend = "INCREASING" if rss_values[-1] > rss_values[0] + 50 else "STABLE"
        print(f"Memory Trend: {trend}")
        print(f"Peak Memory: {max(rss_values):.2f} MB")
        print(f"Memory Range: {min(rss_values):.2f} - {max(rss_values):.2f} MB")
        print(f"Total Snapshots: {len(tracker.snapshots)}")
    
    return memory_growth < 100  # Return True if no significant leak detected


if __name__ == "__main__":
    print("Starting comprehensive memory leak detection...")
    
    try:
        leak_free = run_comprehensive_memory_test()
        exit_code = 0 if leak_free else 1
        
        print(f"\n{'='*80}")
        print(f"FINAL RESULT: {'MEMORY LEAK FREE' if leak_free else 'POTENTIAL MEMORY LEAK DETECTED'}")
        print(f"{'='*80}")
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)
