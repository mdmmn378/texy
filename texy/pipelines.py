import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Callable, List, Tuple

from .texy import extreme_clean, relaxed_clean, strict_clean  # noqa: F401


def _apply_strategy(
    strategy: Callable[[List[str]], List[str]], batch: List[str], idx: int
) -> Tuple[int, List[Any]]:
    return idx, strategy(batch)


def parallelize(
    strategy: Callable[[List[str]], List[str]], data: List[str], max_workers: int
) -> List[str]:
    """Using this function is not recommended for most of the cases."""
    if not max_workers:
        max_workers = multiprocessing.cpu_count()
    batch_size: int = max(len(data) // max_workers, 1)
    if len(data) < max_workers * (2**4):
        max_workers = 1
    futures: List[Any] = []
    store: List[Any] = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            futures.append(executor.submit(_apply_strategy, strategy, batch, i))
        for future in as_completed(futures):
            try:
                store.append(future.result())
            except Exception as e:  # TODO: specify exception
                print(e)
                raise Exception("Exception occurred")
    store = sorted(store, key=lambda x: x[0])
    result: List[str] = []
    for i in store:
        result.extend(i[1])
    return result
