#!/usr/bin/env python3
"""
Quick performance test to verify OnceLock optimization works correctly.
"""

import time
import gc
from texy.direct import extreme_clean_direct

# Test data with URLs, emails, emojis
test_texts = [
    "Check out https://github.com/user/repo and email us at test@example.com 😀😢",
    "Visit http://example.com or contact admin@test.org for more info 🎉",
    "Website: https://secure.site.com/login?user=test@domain.com 🚀",
] * 1000000  # 300 total texts

def performance_test():
    print("🚀 Testing OnceLock Performance Optimization")
    print("=" * 50)
    
    # Warm up (first call compiles regexes)
    print("🔥 Warming up (compiling regexes)...")
    start = time.time()
    _ = extreme_clean_direct(test_texts[:10])
    warmup_time = time.time() - start
    print(f"   Warmup time: {warmup_time:.4f}s")
    
    # Performance test (should reuse compiled regexes)
    print("\n⚡ Performance test (reusing regexes)...")
    start = time.time()
    for i in range(5):
        _ = extreme_clean_direct(test_texts)
        lap_time = time.time() - start
        print(f"   Iteration {i+1}: {lap_time:.4f}s total")
    
    total_time = time.time() - start
    avg_time = total_time / 5
    texts_per_second = (len(test_texts) * 5) / total_time
    
    print(f"\n📊 Results:")
    print(f"   Total processing time: {total_time:.4f}s")
    print(f"   Average per iteration: {avg_time:.4f}s")
    print(f"   Texts processed per second: {texts_per_second:.1f}")
    print(f"   Processing {len(test_texts)} texts took: {avg_time:.4f}s avg")
    
    if avg_time < 0.1:
        print("✅ EXCELLENT: Very fast processing!")
    elif avg_time < 0.2:
        print("✅ GOOD: Fast processing")
    else:
        print("⚠️ SLOW: May need further optimization")

if __name__ == "__main__":
    performance_test()
