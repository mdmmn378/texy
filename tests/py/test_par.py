from texy.pipelines import extreme_clean, parallelize


def dummy(x):
    return [i[0] for i in x]


def test_parallelize():
    """Test parallelize function."""
    data = ["a ", "b ", "c ", "d ", "e ", "f ", "g ", "h ?."]
    expected_data = ["a", "b", "c", "d", "e", "f", "g", "h"]
    data *= 1_000
    expected_data *= 1_000
    assert parallelize(extreme_clean, data, 2) == expected_data


def test_parallelize_with_native():
    """Test parallelize function."""
    data = ["a ", "b ", "c ", "d ", "e ", "f ", "g ", "h ?."]
    expected_data = ["a", "b", "c", "d", "e", "f", "g", "h"]
    data *= 10_000
    expected_data *= 10_000

    assert parallelize(dummy, data, 2) == expected_data
