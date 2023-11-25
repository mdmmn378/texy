# Texy: A conservative text processing library

---

[![Python](https://github.com/mdmmn378/texy/actions/workflows/build-publish.yaml/badge.svg)](https://github.com/mdmmn378/texy/actions/workflows/build-publish.yaml)

> A utility library for quickly cleaning texts

## Installation

Python version in the dev environment: `3.11.5`

> `pip install -U texy`

## Usage

Pipelines with parallelization in Rust:

```python
>>> from texy.pipelines import extreme_clean, strict_clean, relaxed_clean
>>> data = ["hello ;/ from the other side 😊 \t "]
print(extreme_clean(data))
>>> ['hello from the other side']
print(strict_clean(data))
>>> ['hello ;/ from the other side']
print(relaxed_clean(data))
>>> ['hello ;/ from the other side 😊']
```

Parallelize custom functions with Python Multiprocessing:

```python
from texy.pipelines import parallelize

def dummy(x):
    return [i[0] for i in x]

data = ["a ", "b ", "c ", "d ", "e ", "f ", "g ", "h ?."] * 100
print(parallelize(dummy, data, 2))
```

## Actions

| Pipeline        | Actions                                                                                                                                                               |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `relaxed_clean` | `remove_newlines`, `remove_html`, `remove_xml`, `merge_spaces`                                                                                                        |
| `strict_clean`  | `remove_newlines`, `remove_urls`, `remove_emails`, `remove_html`, `remove_xml`, `remove_emoticons`, `remove_emojis`, `remove_infrequent_punctuations`, `merge_spaces` |
| `extreme_clean` | `remove_newlines`, `remove_urls`, `remove_emails`, `remove_html`, `remove_xml`, `remove_emoticons`, `remove_emojis`, `remove_all_punctuations`, `merge_spaces`        |
