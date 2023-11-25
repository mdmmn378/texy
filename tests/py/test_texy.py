from texy.pipelines import extreme_clean, relaxed_clean, strict_clean


def test_strict(sample_input, strict_output):
    for i, j in zip(strict_clean(sample_input), strict_output):
        assert i == j


def test_relaxed(sample_input, relaxed_output):
    for i, j in zip(relaxed_clean(sample_input), relaxed_output):
        assert i == j


def test_extreme(sample_input, extreme_output):
    for i, j in zip(extreme_clean(sample_input), extreme_output):
        assert i == j
