#!/usr/bin/env python3
"""
Final validation test for memory leak fixes.
Tests the optimized Rust code without lazy_static.
"""

import gc
import time
import psutil
from concurrent.futures import ThreadPoolExecutor

# Import the available texy functions
from texy import pipelines
from texy.direct import extreme_clean_direct, strict_clean_direct, relaxed_clean_direct

# Test data
HARD_TEXT = """
🚀 Check out this amazing project at https://github.com/user/repo! 
📧 Contact us at: support@example.com or admin@test.org
🎉 Visit our website: http://www.awesome-site.com/path?param=value
👨‍💻 Developer email: dev@company.co.uk and backup@domain.net
🌟 Don't forget: www.simple-site.org and https://secure.banking.com/login
📱 Mobile: https://m.mobile-site.com/app and ftp://files.example.com/data
💡 Ideas: ideas@startup.io plus feedback@service.com
🤔 Think about this: 😀😢😍🤔😂 with some more :) :( ;) :D emoticons here!
"""

SAMPLE_TEXTS = [HARD_TEXT + f" Sample {i}" for i in range(1000)]

class MemoryTracker:
    def __init__(self, name: str):
        self.name = name
        self.process = psutil.Process()
        self.initial_memory = None
        
    def start(self):
        gc.collect()
        time.sleep(0.1)
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        print(f"🧮 {self.name} - Initial memory: {self.initial_memory:.1f} MB")
        
    def checkpoint(self, label: str):
        gc.collect()
        time.sleep(0.1)
        current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        change = current_memory - self.initial_memory
        print(f"📊 {self.name} - {label}: {current_memory:.1f} MB ({change:+.1f} MB)")
        return current_memory
        
    def end(self):
        gc.collect()
        time.sleep(0.2)
        final_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        total_change = final_memory - self.initial_memory
        print(f"🏁 {self.name} - Final memory: {final_memory:.1f} MB ({total_change:+.1f} MB total)")
        return total_change

def test_direct_rust_functions():
    """Test direct Rust function calls for memory leaks."""
    tracker = MemoryTracker("Direct Rust Functions")
    tracker.start()
    
    # Test extreme_clean_direct
    for i in range(0, 500, 50):
        batch = SAMPLE_TEXTS[i:i+50]
        _ = extreme_clean_direct(batch)
        if i % 100 == 0:
            tracker.checkpoint(f"extreme_clean x{i+50}")
    
    # Test strict_clean_direct
    for i in range(0, 500, 50):
        batch = SAMPLE_TEXTS[i:i+50]
        _ = strict_clean_direct(batch)
        if i % 100 == 0:
            tracker.checkpoint(f"strict_clean x{i+50}")
    
    # Test relaxed_clean_direct
    for i in range(0, 500, 50):
        batch = SAMPLE_TEXTS[i:i+50]
        _ = relaxed_clean_direct(batch)
        if i % 100 == 0:
            tracker.checkpoint(f"relaxed_clean x{i+50}")
    
    return tracker.end()

def test_pipeline_functions():
    """Test pipeline functions for memory leaks."""
    tracker = MemoryTracker("Pipeline Functions")
    tracker.start()
    
    # Test the three main pipeline functions
    for i in range(0, 400, 50):
        batch = SAMPLE_TEXTS[i:i+50]
        _ = pipelines.extreme_clean(batch)
        _ = pipelines.strict_clean(batch)
        _ = pipelines.relaxed_clean(batch)
        if i % 100 == 0:
            tracker.checkpoint(f"Pipeline processing x{i+50}")
    
    return tracker.end()

def test_threading_memory():
    """Test threading with memory tracking."""
    tracker = MemoryTracker("Threading Test")
    tracker.start()
    
    def worker_task(text_batch):
        # Use direct functions for threading test
        r1 = extreme_clean_direct(text_batch)
        r2 = strict_clean_direct(text_batch)
        return len(r1) + len(r2)
    
    # Split texts into batches for threading
    batch_size = 25
    batches = [SAMPLE_TEXTS[i:i+batch_size] for i in range(0, 400, batch_size)]
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i, batch in enumerate(batches):
            future = executor.submit(worker_task, batch)
            futures.append(future)
            if i % 4 == 0:
                tracker.checkpoint(f"Submitted {i+1} thread tasks")
        
        # Collect results
        for i, future in enumerate(futures):
            _ = future.result()
            if i % 4 == 0:
                tracker.checkpoint(f"Completed {i+1} thread tasks")
    
    return tracker.end()

def test_intensive_processing():
    """Test intensive processing to stress-test memory management."""
    tracker = MemoryTracker("Intensive Processing")
    tracker.start()
    
    # Process larger batches intensively
    for i in range(0, 1000, 100):
        batch = SAMPLE_TEXTS[i:i+100] if i+100 <= len(SAMPLE_TEXTS) else SAMPLE_TEXTS[i:]
        
        # Multiple rounds of processing with both direct and pipeline functions
        _ = extreme_clean_direct(batch)
        _ = strict_clean_direct(batch)
        _ = relaxed_clean_direct(batch)
        
        _ = pipelines.extreme_clean(batch)
        _ = pipelines.strict_clean(batch)
        _ = pipelines.relaxed_clean(batch)
        
        tracker.checkpoint(f"Intensive batch {i//100 + 1}")
    
    return tracker.end()

def test_repeated_processing():
    """Test repeated processing with the same data to check for cumulative leaks."""
    tracker = MemoryTracker("Repeated Processing")
    tracker.start()
    
    # Use the same batch repeatedly to test for cumulative memory growth
    test_batch = SAMPLE_TEXTS[:100]
    
    for round_num in range(1, 21):
        _ = extreme_clean_direct(test_batch)
        _ = strict_clean_direct(test_batch)
        _ = relaxed_clean_direct(test_batch)
        _ = pipelines.extreme_clean(test_batch)
        _ = pipelines.strict_clean(test_batch)
        _ = pipelines.relaxed_clean(test_batch)
        
        if round_num % 5 == 0:
            tracker.checkpoint(f"Round {round_num}")
    
    return tracker.end()

def main():
    print("🔬 Starting Final Validation Test (Post lazy_static Removal)")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Direct Rust functions
    print("\n🧪 Test 1: Direct Rust Functions")
    print("-" * 40)
    results["direct"] = test_direct_rust_functions()
    
    # Test 2: Pipeline functions
    print("\n🧪 Test 2: Pipeline Functions") 
    print("-" * 40)
    results["pipeline"] = test_pipeline_functions()
    
    # Test 3: Threading
    print("\n🧪 Test 3: Threading Memory")
    print("-" * 40)
    results["threading"] = test_threading_memory()
    
    # Test 4: Intensive processing
    print("\n🧪 Test 4: Intensive Processing")
    print("-" * 40)
    results["intensive"] = test_intensive_processing()
    
    # Test 5: Repeated processing
    print("\n🧪 Test 5: Repeated Processing")
    print("-" * 40)
    results["repeated"] = test_repeated_processing()
    
    # Summary
    print("\n📋 FINAL SUMMARY")
    print("=" * 50)
    
    total_change = 0
    all_passed = True
    
    for test_name, memory_change in results.items():
        status = "✅ PASSED" if memory_change <= 2.0 else "❌ FAILED"
        if memory_change > 2.0:
            all_passed = False
        print(f"{test_name.upper():15} : {memory_change:+6.1f} MB - {status}")
        total_change += memory_change
    
    print("-" * 50)
    print(f"{'TOTAL':15} : {total_change:+6.1f} MB")
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Memory leaks have been eliminated!")
        print("🚀 The lazy_static removal successfully fixed the memory retention issues.")
        print("💡 Final status: Rust bindings are now memory-efficient.")
    else:
        print("\n⚠️  Some tests still show memory growth > 2MB. Investigating...")
        
        if total_change <= 5.0:
            print("🔍 Total memory change is reasonable (≤5MB) - likely acceptable overhead.")
        else:
            print("⚠️  Total memory change is high - may need further optimization.")
        
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
