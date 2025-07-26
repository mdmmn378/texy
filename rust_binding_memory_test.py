#!/usr/bin/env python3
"""
Memory leak test for direct Rust bindings in texy.

This test directly calls the Rust functions (without Python pipelines/threading)
to check if the Rust bindings themselves leak memory.
"""

import gc
import psutil
import time
from typing import List, Dict, Any
import os

# Import direct Rust functions
from texy import texy
rust_extreme_clean = texy.extreme_clean
rust_strict_clean = texy.strict_clean
rust_relaxed_clean = texy.relaxed_clean


class RustBindingMemoryTracker:
    """Track memory usage for direct Rust binding calls."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.baseline_memory = 0.0
        
    def get_memory_mb(self) -> float:
        """Get current RSS memory in MB."""
        return self.process.memory_info().rss / 1024 / 1024
    
    def set_baseline(self):
        """Set baseline memory after initial cleanup."""
        # Force aggressive garbage collection
        for _ in range(5):
            gc.collect()
        time.sleep(0.1)
        self.baseline_memory = self.get_memory_mb()
        print(f"🔧 Baseline memory set to: {self.baseline_memory:.1f} MB")
    
    def test_function_memory_leak(
        self, 
        func_name: str,
        rust_func,
        test_data: List[str],
        iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Test if a Rust function leaks memory over multiple calls.
        
        Args:
            func_name: Name of the function being tested
            rust_func: The Rust function to test
            test_data: Test data to process
            iterations: Number of iterations to run
            
        Returns:
            Dictionary with test results
        """
        print(f"\n🧪 Testing {func_name} with {len(test_data)} samples, {iterations} iterations")
        
        memory_readings = []
        start_memory = self.get_memory_mb()
        memory_readings.append(start_memory)
        
        start_time = time.time()
        
        for i in range(iterations):
            # Call the Rust function directly
            result = rust_func(test_data.copy())
            
            # Immediate cleanup of result
            del result
            
            # Force garbage collection after each call
            for _ in range(3):
                gc.collect()
            
            # Record memory after cleanup
            current_memory = self.get_memory_mb()
            memory_readings.append(current_memory)
            
            if i % 5 == 0:
                memory_growth = current_memory - start_memory
                print(f"  Iteration {i+1:2d}: {current_memory:5.1f} MB (+{memory_growth:+5.1f} MB)")
        
        end_time = time.time()
        end_memory = self.get_memory_mb()
        
        # Calculate statistics
        total_growth = end_memory - start_memory
        peak_memory = max(memory_readings)
        average_memory = sum(memory_readings) / len(memory_readings)
        
        results = {
            'function': func_name,
            'iterations': iterations,
            'data_size': len(test_data),
            'start_memory': start_memory,
            'end_memory': end_memory,
            'peak_memory': peak_memory,
            'average_memory': average_memory,
            'total_growth': total_growth,
            'memory_readings': memory_readings,
            'execution_time': end_time - start_time,
            'calls_per_second': iterations / (end_time - start_time)
        }
        
        # Determine if there's a leak
        leak_threshold = 5.0  # MB
        has_leak = total_growth > leak_threshold
        
        print("  📊 Results:")
        print(f"     Start: {start_memory:.1f} MB")
        print(f"     End:   {end_memory:.1f} MB")
        print(f"     Peak:  {peak_memory:.1f} MB")
        print(f"     Growth: {total_growth:+.1f} MB")
        print(f"     Time: {results['execution_time']:.2f}s ({results['calls_per_second']:.1f} calls/s)")
        
        if has_leak:
            print(f"  ⚠️  POTENTIAL LEAK: {total_growth:.1f} MB growth detected!")
        else:
            print("  ✅ CLEAN: Memory growth within acceptable limits")
            
        return results


def create_test_data(size: int) -> List[str]:
    """Create test data for memory leak testing."""
    base_samples = [
        "Hello, this is a sample text with\nnewlines.",
        "Visit https://example.com for more info!",
        "Send your feedback to feedback@example.com",
        "<p>This is an HTML paragraph.</p>",
        "<xml>This is some XML content.</xml>",
        "😃 Removing emoticons and emojis 😊 🚀",
        "This text has infrequent punctuations: !?#$%&*",
        "Multiple      spaces     between   words.",
        "Some Bengali text: কুকুর একটি পোষা প্রাণী।",
        "Mixed content with 123 numbers and symbols @#$%",
    ]
    
    # Duplicate to reach desired size
    repeats = (size // len(base_samples)) + 1
    samples = (base_samples * repeats)[:size]
    
    return samples


def run_rust_binding_memory_tests():
    """Run comprehensive memory leak tests for Rust bindings."""
    print("🔬 Rust Binding Memory Leak Test")
    print("=" * 50)
    print("Testing direct Rust function calls for memory leaks")
    print("(No Python threading/multiprocessing involved)")
    
    tracker = RustBindingMemoryTracker()
    
    # Set baseline memory
    tracker.set_baseline()
    
    # Test different data sizes
    test_sizes = [1000, 10000, 50000]
    
    # Test configurations: (function_name, rust_function)
    rust_functions = [
        ("rust_extreme_clean", rust_extreme_clean),
        ("rust_strict_clean", rust_strict_clean),
        ("rust_relaxed_clean", rust_relaxed_clean),
    ]
    
    all_results = []
    
    for data_size in test_sizes:
        print(f"\n📋 Testing with {data_size:,} samples")
        print("-" * 30)
        
        # Create test data
        test_data = create_test_data(data_size)
        
        for func_name, rust_func in rust_functions:
            # Force cleanup before each test
            for _ in range(5):
                gc.collect()
            time.sleep(0.1)
            
            try:
                results = tracker.test_function_memory_leak(
                    func_name=func_name,
                    rust_func=rust_func,
                    test_data=test_data,
                    iterations=10
                )
                all_results.append(results)
                
            except Exception as e:
                print(f"❌ Error testing {func_name}: {e}")
                continue
        
        # Cleanup between test sizes
        del test_data
        for _ in range(5):
            gc.collect()
        time.sleep(0.2)
    
    # Final summary
    print("\n📈 SUMMARY REPORT")
    print("=" * 50)
    
    leak_detected = False
    for result in all_results:
        status = "⚠️ LEAK" if result['total_growth'] > 5.0 else "✅ CLEAN"
        print(f"{status} {result['function']:20} ({result['data_size']:5,} samples): "
              f"{result['total_growth']:+6.1f} MB growth")
        
        if result['total_growth'] > 5.0:
            leak_detected = True
    
    print("\n🔍 CONCLUSION:")
    if leak_detected:
        print("⚠️  MEMORY LEAKS DETECTED in Rust bindings!")
        print("   The Rust functions appear to be retaining memory across calls.")
        print("   This suggests potential issues in the Rust/PyO3 memory management.")
    else:
        print("✅ NO MEMORY LEAKS detected in Rust bindings!")
        print("   The Rust functions properly clean up memory after each call.")
        print("   Memory growth is within acceptable limits.")
    
    return all_results


def run_single_large_test():
    """Run a single test with a large dataset to stress-test memory."""
    print("\n🎯 STRESS TEST: Single large dataset")
    print("=" * 50)
    
    tracker = RustBindingMemoryTracker()
    tracker.set_baseline()
    
    # Create large test dataset (100K samples)
    large_data = create_test_data(100000)
    print(f"Created test data: {len(large_data):,} samples")
    
    # Test each function once with large data
    functions = [
        ("rust_extreme_clean", rust_extreme_clean),
        ("rust_strict_clean", rust_strict_clean), 
        ("rust_relaxed_clean", rust_relaxed_clean),
    ]
    
    for func_name, rust_func in functions:
        print(f"\n🔧 Testing {func_name} with {len(large_data):,} samples...")
        
        start_memory = tracker.get_memory_mb()
        start_time = time.time()
        
        # Single call with large dataset
        result = rust_func(large_data.copy())
        
        end_time = time.time()
        end_memory_before_cleanup = tracker.get_memory_mb()
        
        # Cleanup
        del result
        for _ in range(5):
            gc.collect()
        time.sleep(0.1)
        
        final_memory = tracker.get_memory_mb()
        
        # Report results
        peak_growth = end_memory_before_cleanup - start_memory
        final_growth = final_memory - start_memory
        execution_time = end_time - start_time
        
        print(f"  ⏱️  Execution time: {execution_time:.2f}s")
        print(f"  📊 Memory before cleanup: {end_memory_before_cleanup:.1f} MB (+{peak_growth:+.1f} MB)")
        print(f"  🧹 Memory after cleanup:  {final_memory:.1f} MB (+{final_growth:+.1f} MB)")
        
        if final_growth > 10.0:
            print(f"  ⚠️  Potential leak: {final_growth:.1f} MB retained")
        else:
            print(f"  ✅ Clean: Only {final_growth:.1f} MB retained")


if __name__ == "__main__":
    print("🚀 Starting Rust Binding Memory Leak Tests")
    print(f"Python PID: {os.getpid()}")
    print(f"Initial memory: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB")
    
    try:
        # Run the comprehensive tests
        results = run_rust_binding_memory_tests()
        
        # Run stress test
        run_single_large_test()
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🏁 Test completed. Final memory: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB")
