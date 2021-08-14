__all__ = [
    'Worker',
    'SyncWorker',
    'AsyncWorker',
]

import time
from multiprocessing import Pool, TimeoutError
from abc import ABC, abstractmethod


class Worker:
  @abstractmethod
  def request_process(self, f, *args, **kwargs):
    pass

  @abstractmethod
  def get_results(self):
    pass

  def close(self):
    pass

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()


class SyncWorker(Worker):
  def __init__(self, early_return: bool = True):
    self.early_return = early_return
    if self.early_return:
      self.result = None
    else:
      self.results = []

  def request_process(self, f, *args, **kwargs):
    if self.early_return and self.result is not None:
      return
    result = f(*args, **kwargs)
    if result is not None:
      if self.early_return:
        self.result = result
      else:
        self.results.append(result)

  def get_results(self):
    if self.early_return:
      return self.result
    else:
      return self.results


class AsyncWorker(Worker):
  def __init__(self, num_workers=None, timeout=None, early_return: bool = True):
    self.pool = Pool(num_workers)
    self.timeout = timeout
    self.results = []
    self.early_return = early_return

  def request_process(self, f, *args, **kwargs):
    self.results.append(self.pool.apply_async(f, args, kwargs))

  def get_results(self):
    begin_time = time.time()
    unpacked_results = []
    for result in self.results:
      try:
        if self.timeout is None:
          unpacked_result = result.get()
        else:
          rem = max(0, self.timeout - (time.time() - begin_time))
          unpacked_result = result.get(rem)
        if unpacked_result is not None:
          if self.early_return:
            return unpacked_result
          unpacked_results.append(unpacked_result)
      except TimeoutError:
        pass
    return None if self.early_return else unpacked_result

  def close(self):
    self.pool.terminate()
    self.pool.join()
