import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

from .texy import extreme_clean, relaxed_clean, strict_clean  # noqa: F401


def _apply_strategy(strategy, batch, idx):
    return idx, strategy(batch)


def parallelize(strategy, data, max_workers=None):
    if not max_workers:
        max_workers = multiprocessing.cpu_count()
    batch_size = max(len(data) // max_workers, 1)
    if len(data) < max_workers * (2**4):
        max_workers = 1
    futures = []
    store = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            futures.append(executor.submit(_apply_strategy, strategy, batch, i))
        for future in as_completed(futures):
            try:
                store.append(future.result())
            except Exception as e:
                print(e)
                raise "Failed to process data!"
    store = sorted(store, key=lambda x: x[0])
    result = []
    for i in store:
        result.extend(i[1])
    return result
