"""
Direct interface to Rust functions that minimizes Python memory overhead.
This module provides direct access to the optimized Rust functions without 
Python multiprocessing overhead for minimal memory footprint.
"""
import gc
from typing import List

from .texy import extreme_clean as _extreme_clean_direct
from .texy import relaxed_clean as _relaxed_clean_direct  
from .texy import strict_clean as _strict_clean_direct


def extreme_clean_direct(data: List[str]) -> List[str]:
    """
    Direct extreme cleaning that bypasses Python multiprocessing.
    Provides minimal memory overhead for maximum memory efficiency.
    """
    try:
        # Call Rust function directly
        result = _extreme_clean_direct(data)
        return result
    finally:
        # Force immediate garbage collection
        for _ in range(3):
            gc.collect()


def strict_clean_direct(data: List[str]) -> List[str]:
    """
    Direct strict cleaning that bypasses Python multiprocessing.
    Provides minimal memory overhead for maximum memory efficiency.
    """
    try:
        # Call Rust function directly
        result = _strict_clean_direct(data)
        return result
    finally:
        # Force immediate garbage collection
        for _ in range(3):
            gc.collect()


def relaxed_clean_direct(data: List[str]) -> List[str]:
    """
    Direct relaxed cleaning that bypasses Python multiprocessing.
    Provides minimal memory overhead for maximum memory efficiency.
    """
    try:
        # Call Rust function directly
        result = _relaxed_clean_direct(data)
        return result
    finally:
        # Force immediate garbage collection
        for _ in range(3):
            gc.collect()


# For backward compatibility, also provide the direct functions with shorter names
extreme_clean = extreme_clean_direct
strict_clean = strict_clean_direct
relaxed_clean = relaxed_clean_direct
