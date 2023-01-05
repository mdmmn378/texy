import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

from ._internal import process_schema_101  # pyright: ignore


def set_seq(batch, idx):
    return idx, process_schema_101(batch)


def run_101(data, multiprocess=True):
    if multiprocess:
        cpus = multiprocessing.cpu_count()
    else:
        cpus = 1
    batch_size = max(len(data) // cpus, 1)
    if len(data) < cpus * (2**4):
        cpus = 1
    futures = []
    store = []
    with ProcessPoolExecutor(max_workers=cpus) as executor:
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            futures.append(executor.submit(set_seq, batch, i))
        for future in as_completed(futures):
            try:
                store.append(future.result())
            except:
                raise "Failed to process data!"
    store = sorted(store, key=lambda x: x[0])
    result = []
    for i in store:
        result.extend(i[1])
    return result
