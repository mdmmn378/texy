#!/usr/bin/env python3
"""
Comprehensive Memory Leak Detection Script for Texy Library
Tests different sized arrays and monitors memory behavior across multiple runs.
"""
import gc
import time
import ctypes
import sys
from typing import List, Dict, Any, Tuple

def get_memory_mb() -> float:
    """Get current memory usage in MB using /proc/self/status."""
    try:
        with open('/proc/self/status', 'r') as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    mem_kb = int(line.split()[1])
                    return mem_kb / 1024
    except Exception:
        return 0.0

def aggressive_cleanup() -> None:
    """Perform aggressive memory cleanup."""
    # Multiple rounds of garbage collection
    for _ in range(8):
        gc.collect()
    
    # Force memory return to OS
    try:
        libc = ctypes.CDLL("libc.so.6")
        for _ in range(3):
            libc.malloc_trim(0)
    except Exception:
        pass
    
    # Brief pause to allow system cleanup
    time.sleep(0.1)

def generate_test_data(size: int, complexity: str = "medium") -> List[str]:
    """Generate test data of specified size and complexity."""
    
    if complexity == "simple":
        base_texts = [
            "Hello world",
            "Simple text",
            "Test data",
        ]
    elif complexity == "medium":
        base_texts = [
            "Hello world with https://example.com and test@email.com 😊",
            "<p>HTML content with <b>bold</b> and <i>italic</i> tags</p>",
            "Text with :) :( :D emoticons and 🚀 🌟 ✨ emojis",
            "Multiple    spaces    and\nnewlines\there\tand\teverywhere",
            "Punctuation!@#$%^&*()_+-={}[]|\\:;\"'<>?,./ removal test",
        ]
    else:  # complex
        base_texts = [
            "Complex text with https://very-long-url.example.com/path/to/resource?param=value&other=data and multiple@email-addresses.domain.com 😊🎉🚀",
            "<div class='container'><p>Nested <b>HTML</b> with <a href='#'>links</a> and <span style='color: red;'>styles</span></p></div>",
            "Emoticons galore :) :( :D :P :O :| >:( :') ;) and emojis 🌟✨🎊🎉🚀💫⭐🌈🦄💖",
            "    Excessive     whitespace     with\n\n\nmultiple\n\nlines\t\tand\t\ttabs\t\teverywhere    ",
            "Special chars üñíçødé and punctuation!!!@@@###$$$%%%^^^&&&***((())) test---___+++===",
            "Mixed content: Visit https://example.com or email user@domain.org for more 🌟 info!!! :)",
        ]
    
    # Replicate base texts to reach desired size
    result = []
    while len(result) < size:
        result.extend(base_texts)
    
    return result[:size]

def run_single_test(pipeline_func, data: List[str], test_name: str) -> Dict[str, Any]:
    """Run a single test and return detailed memory statistics."""
    
    # Pre-test cleanup and baseline
    aggressive_cleanup()
    pre_memory = get_memory_mb()
    
    # Process the data
    start_time = time.perf_counter()
    try:
        result = pipeline_func(data.copy())
        success = True
        error_msg = None
    except Exception as e:
        result = []
        success = False
        error_msg = str(e)
    
    end_time = time.perf_counter()
    peak_memory = get_memory_mb()
    
    # Immediate cleanup
    del result
    del data
    aggressive_cleanup()
    
    # Post-cleanup memory
    post_memory = get_memory_mb()
    
    # Calculate metrics
    processing_time = end_time - start_time
    peak_increase = peak_memory - pre_memory
    net_increase = post_memory - pre_memory
    
    return {
        'test_name': test_name,
        'success': success,
        'error': error_msg,
        'pre_memory': pre_memory,
        'peak_memory': peak_memory,
        'post_memory': post_memory,
        'peak_increase': peak_increase,
        'net_increase': net_increase,
        'processing_time': processing_time,
    }

def analyze_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze test results for memory leak patterns."""
    
    successful_results = [r for r in results if r['success']]
    
    if not successful_results:
        return {'status': 'ALL_FAILED', 'message': 'All tests failed'}
    
    # Calculate statistics
    net_increases = [r['net_increase'] for r in successful_results]
    peak_increases = [r['peak_increase'] for r in successful_results]
    
    avg_net = sum(net_increases) / len(net_increases)
    max_net = max(net_increases)
    min_net = min(net_increases)
    
    avg_peak = sum(peak_increases) / len(peak_increases)
    max_peak = max(peak_increases)
    
    # Detect patterns
    leak_detected = False
    leak_severity = "NONE"
    
    if avg_net > 1.0:
        leak_detected = True
        if avg_net > 5.0:
            leak_severity = "SEVERE"
        elif avg_net > 2.0:
            leak_severity = "MODERATE"
        else:
            leak_severity = "MINOR"
    
    # Check for accumulation pattern
    accumulation_detected = False
    if len(net_increases) >= 3:
        # Check if memory keeps increasing
        increasing_count = 0
        for i in range(1, len(net_increases)):
            if net_increases[i] > net_increases[i-1]:
                increasing_count += 1
        
        if increasing_count >= len(net_increases) * 0.6:
            accumulation_detected = True
    
    return {
        'status': 'ANALYZED',
        'total_tests': len(results),
        'successful_tests': len(successful_results),
        'failed_tests': len(results) - len(successful_results),
        'avg_net_increase': avg_net,
        'max_net_increase': max_net,
        'min_net_increase': min_net,
        'avg_peak_increase': avg_peak,
        'max_peak_increase': max_peak,
        'leak_detected': leak_detected,
        'leak_severity': leak_severity,
        'accumulation_detected': accumulation_detected,
        'net_increases': net_increases,
    }

def print_test_report(results: List[Dict[str, Any]], analysis: Dict[str, Any], pipeline_name: str) -> None:
    """Print detailed test report."""
    
    print(f"\n{'='*70}")
    print(f"TEST REPORT: {pipeline_name.upper()}")
    print(f"{'='*70}")
    
    print(f"Tests Run: {analysis['total_tests']}")
    print(f"Successful: {analysis['successful_tests']}")
    print(f"Failed: {analysis['failed_tests']}")
    
    if analysis['successful_tests'] > 0:
        print(f"\nMEMORY STATISTICS:")
        print(f"Average net increase: {analysis['avg_net_increase']:+.3f} MB")
        print(f"Maximum net increase: {analysis['max_net_increase']:+.3f} MB")
        print(f"Minimum net increase: {analysis['min_net_increase']:+.3f} MB")
        print(f"Average peak increase: {analysis['avg_peak_increase']:+.3f} MB")
        print(f"Maximum peak increase: {analysis['max_peak_increase']:+.3f} MB")
        
        print(f"\nDETAILED RESULTS:")
        print(f"{'Size':<8} {'Time(s)':<8} {'Peak(MB)':<10} {'Net(MB)':<10} {'Status':<10}")
        print("-" * 50)
        
        for result in results:
            if result['success']:
                size = result['test_name'].split(' ')[0] if ' ' in result['test_name'] else 'N/A'
                status = "✅ OK"
            else:
                size = result['test_name'].split(' ')[0] if ' ' in result['test_name'] else 'N/A'
                status = "❌ FAIL"
            
            print(f"{size:<8} {result['processing_time']:<8.3f} "
                  f"{result['peak_increase']:<10.3f} {result['net_increase']:<10.3f} {status:<10}")
    
    print(f"\nMEMORY LEAK ASSESSMENT:")
    
    if not analysis['leak_detected']:
        print("🏆 NO MEMORY LEAKS DETECTED!")
        print("✨ Excellent memory management!")
    else:
        severity_emoji = {
            'MINOR': '🟡',
            'MODERATE': '⚠️',
            'SEVERE': '❌'
        }
        emoji = severity_emoji.get(analysis['leak_severity'], '❓')
        print(f"{emoji} MEMORY LEAK DETECTED: {analysis['leak_severity']}")
        
        if analysis['leak_severity'] == 'MINOR':
            print("📊 Minor memory retention - acceptable for most use cases")
        elif analysis['leak_severity'] == 'MODERATE':
            print("⚠️ Moderate memory leaks - monitor in production")
        else:
            print("❌ Severe memory leaks - optimization required")
    
    if analysis['accumulation_detected']:
        print("📈 ACCUMULATION PATTERN DETECTED: Memory increases over time")
    else:
        print("✅ NO ACCUMULATION: Memory usage is stable")

def comprehensive_memory_test():
    """Run comprehensive memory leak tests across all pipelines and sizes."""
    
    print("🔬 TEXY COMPREHENSIVE MEMORY LEAK DETECTION")
    print("="*70)
    print("Testing memory behavior across different array sizes and complexities")
    print()
    
    # Import pipeline functions
    try:
        from texy.texy import extreme_clean, relaxed_clean, strict_clean
        print("✅ Successfully imported Rust pipeline functions")
    except ImportError as e:
        print(f"❌ Failed to import Rust functions: {e}")
        return False
    
    try:
        from texy.pipelines import extreme_clean as py_extreme_clean
        from texy.pipelines import relaxed_clean as py_relaxed_clean
        from texy.pipelines import strict_clean as py_strict_clean
        print("✅ Successfully imported Python pipeline functions")
        python_pipelines_available = True
    except ImportError as e:
        print(f"⚠️ Python pipelines not available: {e}")
        python_pipelines_available = False
    
    # Initialize memory baseline
    aggressive_cleanup()
    initial_memory = get_memory_mb()
    print(f"📊 Initial memory baseline: {initial_memory:.2f} MB")
    
    # Initialize pipelines
    print("\n🔧 Initializing pipelines...")
    _ = extreme_clean(["init"])
    aggressive_cleanup()
    post_init_memory = get_memory_mb()
    init_cost = post_init_memory - initial_memory
    print(f"📊 Initialization cost: {init_cost:.2f} MB")
    
    # Test configurations
    test_sizes = [50, 100, 500, 1000, 2500, 5000]
    complexities = ["simple", "medium", "complex"]
    
    # Pipeline configurations
    rust_pipelines = [
        ("extreme_clean", extreme_clean),
        ("relaxed_clean", relaxed_clean),
        ("strict_clean", strict_clean),
    ]
    
    if python_pipelines_available:
        python_pipelines = [
            ("py_extreme_clean", py_extreme_clean),
            ("py_relaxed_clean", py_relaxed_clean),
            ("py_strict_clean", py_strict_clean),
        ]
    else:
        python_pipelines = []
    
    all_results = {}
    
    # Test Rust pipelines
    print(f"\n🦀 TESTING RUST PIPELINES")
    print("-" * 40)
    
    for pipeline_name, pipeline_func in rust_pipelines:
        print(f"\n📋 Testing {pipeline_name}...")
        results = []
        
        for size in test_sizes:
            for complexity in complexities:
                test_data = generate_test_data(size, complexity)
                test_name = f"{size} {complexity}"
                
                print(f"  Running {test_name}...", end=" ")
                result = run_single_test(pipeline_func, test_data, test_name)
                results.append(result)
                
                if result['success']:
                    print(f"✅ {result['net_increase']:+.3f}MB")
                else:
                    print(f"❌ Failed: {result['error']}")
        
        # Analyze results for this pipeline
        analysis = analyze_results(results)
        all_results[f"rust_{pipeline_name}"] = {
            'results': results,
            'analysis': analysis
        }
        
        # Print report
        print_test_report(results, analysis, f"Rust {pipeline_name}")
    
    # Test Python pipelines if available
    if python_pipelines:
        print(f"\n🐍 TESTING PYTHON PIPELINES")
        print("-" * 40)
        
        for pipeline_name, pipeline_func in python_pipelines:
            print(f"\n📋 Testing {pipeline_name}...")
            results = []
            
            # Use smaller sizes for Python pipelines to avoid hanging
            python_test_sizes = [50, 100, 500, 1000]
            
            for size in python_test_sizes:
                test_data = generate_test_data(size, "medium")  # Use medium complexity only
                test_name = f"{size} medium"
                
                print(f"  Running {test_name}...", end=" ")
                result = run_single_test(pipeline_func, test_data, test_name)
                results.append(result)
                
                if result['success']:
                    print(f"✅ {result['net_increase']:+.3f}MB")
                else:
                    print(f"❌ Failed: {result['error']}")
            
            # Analyze results for this pipeline
            analysis = analyze_results(results)
            all_results[f"python_{pipeline_name}"] = {
                'results': results,
                'analysis': analysis
            }
            
            # Print report
            print_test_report(results, analysis, f"Python {pipeline_name}")
    
    # Final comprehensive analysis
    print(f"\n🎯 COMPREHENSIVE ANALYSIS")
    print("="*70)
    
    rust_leak_count = sum(1 for k, v in all_results.items() 
                         if k.startswith('rust_') and v['analysis']['leak_detected'])
    
    python_leak_count = sum(1 for k, v in all_results.items() 
                           if k.startswith('python_') and v['analysis']['leak_detected'])
    
    total_rust_pipelines = len(rust_pipelines)
    total_python_pipelines = len(python_pipelines)
    
    print(f"📊 RUST PIPELINES:")
    print(f"   Total tested: {total_rust_pipelines}")
    print(f"   Memory leaks detected: {rust_leak_count}")
    print(f"   Success rate: {((total_rust_pipelines - rust_leak_count) / total_rust_pipelines * 100):.1f}%")
    
    if python_pipelines:
        print(f"📊 PYTHON PIPELINES:")
        print(f"   Total tested: {total_python_pipelines}")
        print(f"   Memory leaks detected: {python_leak_count}")
        print(f"   Success rate: {((total_python_pipelines - python_leak_count) / total_python_pipelines * 100):.1f}%")
    
    # Overall assessment
    total_leaks = rust_leak_count + python_leak_count
    total_pipelines = total_rust_pipelines + total_python_pipelines
    
    print(f"\n🏆 OVERALL ASSESSMENT:")
    
    if total_leaks == 0:
        print("🎉 EXCELLENT: No memory leaks detected in any pipeline!")
        print("✨ The Texy library shows outstanding memory management!")
        final_grade = "A+"
    elif total_leaks <= total_pipelines * 0.2:
        print("✅ GOOD: Minimal memory leaks detected")
        print("📊 Overall memory management is solid")
        final_grade = "B+"
    elif total_leaks <= total_pipelines * 0.5:
        print("⚠️ ACCEPTABLE: Some memory leaks detected")
        print("🔧 Consider further optimization")
        final_grade = "C+"
    else:
        print("❌ POOR: Significant memory leaks detected")
        print("⚠️ Major optimization required")
        final_grade = "D"
    
    # Final memory check
    aggressive_cleanup()
    final_memory = get_memory_mb()
    total_memory_increase = final_memory - post_init_memory
    
    print(f"\n📈 FINAL MEMORY STATUS:")
    print(f"Memory after all tests: {final_memory:.2f} MB")
    print(f"Total increase from baseline: {total_memory_increase:+.2f} MB")
    print(f"Final Grade: {final_grade}")
    
    return total_leaks == 0

if __name__ == "__main__":
    print("🚀 Starting comprehensive memory leak detection...")
    success = comprehensive_memory_test()
    
    print(f"\n{'='*70}")
    if success:
        print("🎯 MEMORY LEAK DETECTION: PASSED")
        print("🏆 No memory leaks detected! Production ready!")
        sys.exit(0)
    else:
        print("⚠️ MEMORY LEAK DETECTION: ISSUES FOUND")
        print("🔧 Optimization recommended before production use")
        sys.exit(1)
