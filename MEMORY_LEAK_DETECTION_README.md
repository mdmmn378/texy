# Memory Leak Detection Scripts for Texy Library

This repository contains comprehensive memory leak detection scripts designed to test the Texy library with varying sample sizes and monitor memory usage patterns.

## Scripts Overview

### 1. Comprehensive Memory Leak Detector

**File:** `comprehensive_memory_leak_detector.py`

This is the most detailed memory leak detection script that provides:

- Advanced memory tracking with PID monitoring
- Context managers for precise memory measurement
- Detailed snapshots at each test phase
- Memory trend analysis
- Performance metrics for each cleaning function

### 2. Simple Memory Leak Detector

**File:** `simple_memory_leak_detector.py`

A streamlined version that provides:

- Basic memory tracking
- Clear performance summaries
- Easy-to-read output format
- Essential memory leak detection

## Prerequisites

The scripts require the following dependencies:

- `psutil` - For system and process memory monitoring
- `memory-profiler` - For detailed memory profiling

## Installation with UV

This project uses [UV](https://github.com/astral-sh/uv) for fast and reliable Python package management.

```bash
# Install dependencies
uv add psutil memory-profiler

# The texy library should already be included in the project
```

## Usage

### Running the Comprehensive Detector

```bash
# Run with uv (recommended)
uv run python comprehensive_memory_leak_detector.py

# Or run directly (if environment is activated)
python comprehensive_memory_leak_detector.py
```

### Running the Simple Detector

```bash
# Run with uv (recommended)
uv run python simple_memory_leak_detector.py

# Or run directly (if environment is activated)
python simple_memory_leak_detector.py
```

## Test Methodology

Both scripts test memory usage with the following sample sizes:

- **1,000,000 samples** - Large-scale stress test
- **500,000 samples** - Medium-scale test
- **100,000 samples** - Moderate-scale test
- **10,000 samples** - Small-scale test

### Test Process

1. **Data Creation**: Creates a list of complex text samples (same text duplicated N times)
2. **Memory Baseline**: Records initial memory usage
3. **Function Testing**: Tests each Texy cleaning function:
   - `extreme_clean()` - Most aggressive cleaning
   - `strict_clean()` - Balanced cleaning
   - `relaxed_clean()` - Minimal cleaning
4. **Memory Tracking**: Monitors RSS, VMS memory, and percentage usage
5. **Cleanup Verification**: Forces garbage collection and verifies memory release
6. **Analysis**: Compares final vs initial memory usage

### Hard-to-Clean Text Sample

The test uses a comprehensive text sample containing:

- URLs and email addresses
- Emojis and emoticons
- HTML and XML markup
- Special characters and Unicode
- Multiple whitespace patterns
- Numbers and currencies
- Code blocks and markdown
- Mixed languages
- Long words and repeated patterns

## Memory Leak Detection Criteria

### Acceptable Memory Growth

- **Threshold**: Less than 100 MB total growth
- **Status**: ✅ MEMORY LEAK FREE

### Potential Memory Leak

- **Threshold**: More than 100 MB total growth
- **Status**: 🚨 POTENTIAL MEMORY LEAK DETECTED

## Output Analysis

### Key Metrics

1. **RSS Memory**: Resident Set Size (physical memory usage)
2. **VMS Memory**: Virtual Memory Size (total virtual memory)
3. **Processing Rate**: Items processed per second
4. **Memory Efficiency**: Whether memory returns to baseline after cleanup

### Performance Indicators

- **High processing rates** (50,000+ items/sec) indicate good performance
- **Stable memory usage** between tests indicates proper cleanup
- **Memory return to baseline** indicates no memory leaks

## Example Output

```
================================================================================
MEMORY LEAK DETECTION SUMMARY
================================================================================
Initial Memory (RSS): 20.95 MB
Final Memory (RSS): 83.58 MB
Net Memory Growth: +62.63 MB
Memory Leak Status: ACCEPTABLE

============================================================
PERFORMANCE SUMMARY
============================================================

Sample Size: 1,000,000
----------------------------------------
  extreme_clean:
    Duration: 13.76s
    Rate: 72,682 items/sec
    Output Size: 1,000,000
  Memory Analysis:
    Peak RSS: 43.78 MB
    Final RSS: 36.14 MB
    Memory Efficient: True
```

## Troubleshooting

### Import Errors

If you encounter import errors for the texy module:

1. Ensure the texy library is built: `uv run maturin develop`
2. Check that you're in the correct project directory
3. Verify the virtual environment is activated

### Memory Issues

If tests fail due to insufficient memory:

1. Reduce sample sizes in the script
2. Close other memory-intensive applications
3. Monitor system memory usage during tests

### Performance Issues

If tests run very slowly:

1. Check system CPU usage
2. Ensure no other intensive processes are running
3. Consider running smaller sample sizes first

## Exit Codes

- **0**: No memory leaks detected
- **1**: Potential memory leak detected
- **130**: User interrupted (Ctrl+C)
- **1**: Fatal error occurred

## Customization

You can modify the scripts to:

- Change sample sizes by editing the `sample_sizes` list
- Adjust memory leak threshold by changing the threshold value
- Add custom text samples by modifying the test data creation function
- Include additional cleaning functions for testing

## System Requirements

- **Python**: 3.8 or higher
- **Memory**: At least 8 GB RAM recommended for large sample tests
- **Storage**: Minimal disk space required
- **OS**: Linux, macOS, or Windows

## Contributing

When adding new memory leak detection features:

1. Maintain compatibility with both scripts
2. Add appropriate error handling
3. Include clear documentation
4. Test with various sample sizes
5. Verify memory measurements are accurate
