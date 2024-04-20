from typing import Callable, Any
from multiprocessing import Process, Queue, Manager


def run_in_process(function: Callable, *args, **kwargs) -> Any:
    def target(queue: Queue) -> None:
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            queue.put(e)
        else:
            queue.put(result)

        return

    manager = Manager()
    queue = manager.Queue()
    process = Process(target=target, args=(queue,))
    process.start()
    process.join()

    result = queue.get()
    if isinstance(result, Exception):
        raise result

    return result


__all__ = ["run_in_process"]
