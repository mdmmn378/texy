#!/usr/bin/env python3
"""
Advanced Memory Leak Detection Script with Executor Comparison

This script compares memory usage patterns between ProcessPoolExecutor and ThreadPoolExecutor
to understand the memory behavior differences you observed.
"""

import gc
import os
import psutil
import time
import sys
from typing import Dict, List
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing


class AdvancedMemoryTracker:
    """Advanced memory tracking with detailed process monitoring."""
    
    def __init__(self):
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)
        self.memory_snapshots = []
        
    def get_detailed_memory_info(self) -> Dict[str, float]:
        """Get comprehensive memory information."""
        memory_info = self.process.memory_info()
        memory_percent = self.process.memory_percent()
        
        # Get system memory info
        system_memory = psutil.virtual_memory()
        
        # Get process-specific details
        try:
            memory_maps = self.process.memory_maps()
            total_mapped = sum(m.rss for m in memory_maps) / 1024 / 1024
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            total_mapped = 0
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'percent': memory_percent,
            'shared_mb': getattr(memory_info, 'shared', 0) / 1024 / 1024,
            'text_mb': getattr(memory_info, 'text', 0) / 1024 / 1024,
            'data_mb': getattr(memory_info, 'data', 0) / 1024 / 1024,
            'lib_mb': getattr(memory_info, 'lib', 0) / 1024 / 1024,
            'dirty_mb': getattr(memory_info, 'dirty', 0) / 1024 / 1024,
            'mapped_mb': total_mapped,
            'available_system_mb': system_memory.available / 1024 / 1024,
            'timestamp': time.time()
        }
    
    def take_snapshot(self, label: str) -> Dict[str, float]:
        """Take a detailed memory snapshot."""
        snapshot = self.get_detailed_memory_info()
        snapshot['label'] = label
        self.memory_snapshots.append(snapshot)
        
        print(f"[{label}] PID: {self.pid}")
        print(f"  RSS: {snapshot['rss_mb']:.2f} MB, VMS: {snapshot['vms_mb']:.2f} MB")
        print(f"  Shared: {snapshot['shared_mb']:.2f} MB, Mapped: {snapshot['mapped_mb']:.2f} MB")
        print(f"  Memory %: {snapshot['percent']:.2f}%, Available: {snapshot['available_system_mb']:.2f} MB")
        
        return snapshot
    
    def force_aggressive_cleanup(self):
        """Perform aggressive cleanup and measure effectiveness."""
        initial_memory = self.get_detailed_memory_info()['rss_mb']
        
        for i in range(5):
            collected = gc.collect()
            print(f"    GC round {i+1}: collected {collected} objects")
            time.sleep(0.2)
        
        # Try to force memory release
        try:
            import ctypes
            libc = ctypes.CDLL("libc.so.6")
            libc.malloc_trim(0)
        except Exception:
            pass  # Not available on all systems
        
        final_memory = self.get_detailed_memory_info()['rss_mb']
        released = initial_memory - final_memory
        print(f"    Memory released: {released:.2f} MB")
        
        return released


def create_complex_test_data() -> str:
    """Create complex text for memory stress testing."""
    return """
    🔥 MEMORY STRESS TEST DATA 🔥
    
    Complex content with multiple challenging patterns:
    
    📧 Contact Info:
    - Email: complex.email+test123@very-long-domain-name.co.uk
    - Phone: +1-555-123-4567 ext. 9999
    - Website: https://subdomain.example-site.com/very/long/path?param1=value1&param2=value2#anchor
    
    🌍 International Text:
    - English: The quick brown fox jumps over the lazy dog
    - Spanish: El rápido zorro marrón salta sobre el perro perezoso
    - French: Le renard brun rapide saute par-dessus le chien paresseux
    - German: Der schnelle braune Fuchs springt über den faulen Hund
    - Russian: Быстрая коричневая лиса прыгает через ленивую собаку
    - Chinese: 敏捷的棕色狐狸跳过懒惰的狗
    - Japanese: 素早い茶色のキツネが怠け者の犬を飛び越える
    - Arabic: الثعلب البني السريع يقفز فوق الكلب الكسول
    
    🎨 Rich Content:
    <html>
    <head>
        <title>Memory Test Page</title>
        <style>
            .container { margin: 20px; padding: 15px; }
            .highlight { background-color: #ffff00; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Test Content</h1>
            <p class="highlight">This is <em>emphasized</em> text with <strong>strong</strong> formatting.</p>
            <ul>
                <li>Item 1 with <a href="https://example.com">link</a></li>
                <li>Item 2 with <code>inline code</code></li>
                <li>Item 3 with <img src="image.jpg" alt="description" /></li>
            </ul>
        </div>
    </body>
    </html>
    
    📊 Data Structures:
    JSON: {"users": [{"id": 1, "name": "John Doe", "email": "john@example.com", "active": true}]}
    XML: <users><user id="1"><name>John Doe</name><email>john@example.com</email></user></users>
    CSV: id,name,email,active\n1,"John Doe","john@example.com",true
    
    🔢 Numbers and Patterns:
    - Large numbers: 1,234,567,890.123456789
    - Scientific notation: 1.23e-45, 9.87E+123
    - Currencies: $1,234.56, €999.99, £500.00, ¥10,000, ₹5,000.50
    - Percentages: 99.99%, 0.001%, 150.5%
    - Dates: 2024-01-01, 01/31/2024, Jan 1st, 2024
    
    🎭 Special Characters & Symbols:
    Math: ∑∏∫∂∆∇±×÷≤≥≠≈∞√∛∜
    Currency: $€£¥₹₽₩₪₨₦₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿
    Arrows: ←→↑↓↔↕↖↗↘↙⇐⇒⇑⇓⇔⇕
    Symbols: ©®™℗℠℡№℞℟♀♂⚠⚡⚽⚾⛄⛅⛈⛎⛏⛐⛑⛒⛓⛔⛕⛖⛗⛘⛙⛚⛛⛜⛝⛞⛟⛠⛡⛢⛣⛤⛥⛦⛧⛨⛩⛪⛫⛬⛭⛮⛯⛰⛱⛲⛳⛴⛵⛶⛷⛸⛹⛺⛻⛼⛽⛾⛿
    
    🔤 Text Patterns:
    - Repeated: aaaaaaaaaa bbbbbbbbbb cccccccccc
    - Alternating: abababababab cdcdcdcdcdcd
    - Progressive: a ab abc abcd abcde abcdef
    - Palindromes: racecar, madam, level, radar, civic
    - Very long words: pneumonoultramicroscopicsilicovolcanoconiosisantidisestablishmentarianism
    
    This text is specifically designed to stress test memory allocation and deallocation
    patterns in text processing systems, with varied content that exercises different
    code paths and memory usage patterns.
    """


def test_with_process_pool(test_data: List[str], sample_size: int) -> Dict:
    """Test memory usage with ProcessPoolExecutor."""
    print(f"\n🔄 TESTING WITH PROCESS POOL ({sample_size:,} samples)")
    print("-" * 60)
    
    tracker = AdvancedMemoryTracker()
    
    # Import here to avoid issues with multiprocessing
    from texy.pipelines import extreme_clean
    
    # Take baseline
    baseline = tracker.take_snapshot("ProcessPool - Baseline")
    
    results = {}
    
    # Test with ProcessPoolExecutor
    max_workers = min(4, multiprocessing.cpu_count())
    print(f"Using {max_workers} worker processes")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        process_start = tracker.take_snapshot("ProcessPool - Started")
        
        start_time = time.time()
        
        # Split data into chunks for parallel processing
        chunk_size = len(test_data) // max_workers
        chunks = [test_data[i:i + chunk_size] for i in range(0, len(test_data), chunk_size)]
        
        # Submit jobs
        futures = [executor.submit(extreme_clean, chunk) for chunk in chunks]
        
        # Collect results
        processed_results = []
        for i, future in enumerate(futures):
            result = future.result()
            processed_results.extend(result)
            snapshot = tracker.take_snapshot(f"ProcessPool - Chunk {i+1} completed")
        
        end_time = time.time()
        
        process_end = tracker.take_snapshot("ProcessPool - All completed")
    
    # Cleanup
    del processed_results
    del chunks
    tracker.force_aggressive_cleanup()
    
    final = tracker.take_snapshot("ProcessPool - After cleanup")
    
    duration = end_time - start_time
    rate = sample_size / duration if duration > 0 else 0
    memory_growth = final['rss_mb'] - baseline['rss_mb']
    
    results = {
        'executor_type': 'ProcessPool',
        'duration': duration,
        'rate': rate,
        'memory_growth': memory_growth,
        'baseline_memory': baseline['rss_mb'],
        'final_memory': final['rss_mb'],
        'peak_memory': max(s['rss_mb'] for s in tracker.memory_snapshots),
        'memory_efficient': abs(memory_growth) < 50
    }
    
    print(f"Results: {duration:.2f}s, {rate:,.0f} items/sec, {memory_growth:+.2f} MB growth")
    
    return results


def test_with_thread_pool(test_data: List[str], sample_size: int) -> Dict:
    """Test memory usage with ThreadPoolExecutor."""
    print(f"\n🧵 TESTING WITH THREAD POOL ({sample_size:,} samples)")
    print("-" * 60)
    
    tracker = AdvancedMemoryTracker()
    
    from texy.pipelines import extreme_clean
    
    # Take baseline
    baseline = tracker.take_snapshot("ThreadPool - Baseline")
    
    results = {}
    
    # Test with ThreadPoolExecutor
    max_workers = min(8, (os.cpu_count() or 1) * 2)  # More threads than cores for I/O bound
    print(f"Using {max_workers} worker threads")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        thread_start = tracker.take_snapshot("ThreadPool - Started")
        
        start_time = time.time()
        
        # Split data into chunks for parallel processing
        chunk_size = len(test_data) // max_workers
        chunks = [test_data[i:i + chunk_size] for i in range(0, len(test_data), chunk_size)]
        
        # Submit jobs
        futures = [executor.submit(extreme_clean, chunk) for chunk in chunks]
        
        # Collect results
        processed_results = []
        for i, future in enumerate(futures):
            result = future.result()
            processed_results.extend(result)
            snapshot = tracker.take_snapshot(f"ThreadPool - Chunk {i+1} completed")
        
        end_time = time.time()
        
        thread_end = tracker.take_snapshot("ThreadPool - All completed")
    
    # Cleanup
    del processed_results
    del chunks
    tracker.force_aggressive_cleanup()
    
    final = tracker.take_snapshot("ThreadPool - After cleanup")
    
    duration = end_time - start_time
    rate = sample_size / duration if duration > 0 else 0
    memory_growth = final['rss_mb'] - baseline['rss_mb']
    
    results = {
        'executor_type': 'ThreadPool',
        'duration': duration,
        'rate': rate,
        'memory_growth': memory_growth,
        'baseline_memory': baseline['rss_mb'],
        'final_memory': final['rss_mb'],
        'peak_memory': max(s['rss_mb'] for s in tracker.memory_snapshots),
        'memory_efficient': abs(memory_growth) < 50
    }
    
    print(f"Results: {duration:.2f}s, {rate:,.0f} items/sec, {memory_growth:+.2f} MB growth")
    
    return results


def compare_executors_for_sample_size(sample_size: int) -> Dict:
    """Compare ProcessPool vs ThreadPool for a specific sample size."""
    print(f"\n{'='*80}")
    print(f"EXECUTOR COMPARISON FOR {sample_size:,} SAMPLES")
    print(f"{'='*80}")
    
    # Create test data
    base_text = create_complex_test_data()
    test_data = [base_text] * sample_size
    
    print(f"Created {len(test_data):,} test samples")
    
    results = {}
    
    try:
        # Test ProcessPool
        results['process_pool'] = test_with_process_pool(test_data, sample_size)
        
        # Wait between tests
        time.sleep(2)
        
        # Test ThreadPool
        results['thread_pool'] = test_with_thread_pool(test_data, sample_size)
        
    except Exception as e:
        print(f"ERROR during executor comparison: {e}")
        return {}
    
    finally:
        # Cleanup test data
        del test_data
        del base_text
        gc.collect()
    
    # Analysis
    if 'process_pool' in results and 'thread_pool' in results:
        pp = results['process_pool']
        tp = results['thread_pool']
        
        print(f"\n📊 COMPARISON SUMMARY:")
        print(f"ProcessPool: {pp['duration']:.2f}s, {pp['rate']:,.0f} items/sec, {pp['memory_growth']:+.2f} MB")
        print(f"ThreadPool:  {tp['duration']:.2f}s, {tp['rate']:,.0f} items/sec, {tp['memory_growth']:+.2f} MB")
        
        performance_diff = ((tp['rate'] - pp['rate']) / pp['rate']) * 100 if pp['rate'] > 0 else 0
        memory_diff = tp['memory_growth'] - pp['memory_growth']
        
        print(f"\nThreadPool vs ProcessPool:")
        print(f"  Performance: {performance_diff:+.1f}% {'faster' if performance_diff > 0 else 'slower'}")
        print(f"  Memory difference: {memory_diff:+.2f} MB {'more' if memory_diff > 0 else 'less'}")
        
        results['comparison'] = {
            'performance_diff_percent': performance_diff,
            'memory_diff_mb': memory_diff,
            'threadpool_faster': performance_diff > 0,
            'threadpool_more_memory': memory_diff > 0
        }
    
    return results


def main():
    """Run comprehensive executor comparison."""
    print("="*80)
    print("PROCESSPOOL VS THREADPOOL MEMORY ANALYSIS")
    print("="*80)
    
    # System info
    system_memory = psutil.virtual_memory()
    print(f"System: {system_memory.total / 1024**3:.2f} GB total, "
          f"{system_memory.available / 1024**3:.2f} GB available")
    print(f"CPUs: {multiprocessing.cpu_count()}")
    print(f"Python: {sys.version}")
    
    # Test different sample sizes
    sample_sizes = [1_000_000, 500_000, 100_000, 10_000]
    all_results = {}
    
    for sample_size in sample_sizes:
        try:
            results = compare_executors_for_sample_size(sample_size)
            all_results[sample_size] = results
            
            print(f"\nWaiting 5 seconds before next test...")
            time.sleep(5)
            
        except Exception as e:
            print(f"ERROR during {sample_size:,} sample test: {e}")
            continue
    
    # Final analysis
    print(f"\n{'='*80}")
    print("FINAL ANALYSIS")
    print(f"{'='*80}")
    
    print("\nKey Findings:")
    
    for sample_size, results in all_results.items():
        if not results or 'comparison' not in results:
            continue
            
        comp = results['comparison']
        pp = results['process_pool']
        tp = results['thread_pool']
        
        print(f"\n📊 {sample_size:,} samples:")
        print(f"  ThreadPool: {comp['performance_diff_percent']:+.1f}% performance, {comp['memory_diff_mb']:+.1f} MB memory")
        print(f"  ProcessPool peak: {pp['peak_memory']:.1f} MB, ThreadPool peak: {tp['peak_memory']:.1f} MB")
        
        if abs(comp['memory_diff_mb']) > 100:
            print(f"  ⚠️  Significant memory difference detected!")
        
        if comp['performance_diff_percent'] > 20:
            print(f"  🚀 ThreadPool significantly faster")
        elif comp['performance_diff_percent'] < -20:
            print(f"  🚀 ProcessPool significantly faster")
    
    print(f"\n{'='*60}")
    print("EXPLANATION OF DIFFERENCES")
    print(f"{'='*60}")
    
    print("""
🔄 ProcessPoolExecutor:
- Each worker runs in a separate process with isolated memory
- Memory allocations in workers don't affect main process measurements
- Overhead from inter-process communication and serialization
- Better for CPU-bound tasks, memory isolation
- More stable memory usage in main process

🧵 ThreadPoolExecutor:
- All threads share the same memory space as main process
- Memory allocations directly visible in main process memory
- Python's GIL can cause memory retention between threads
- Better for I/O-bound tasks, shared memory efficiency
- Can show higher memory usage spikes in large workloads

💡 Why Large Samples Show Different Patterns:
- ProcessPool: Worker memory is isolated, main process sees communication overhead
- ThreadPool: All memory allocations accumulate in main process space
- GIL contention in ThreadPool can delay garbage collection
- Serialization overhead in ProcessPool affects performance
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
