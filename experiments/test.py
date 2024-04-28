import multiprocessing
import sys
import time
import os


def trace_calls(frame, event, arg):
    if event == "call":
        code = frame.f_code
        func_name = code.co_name
        lineno = frame.f_lineno
        module_name = frame.f_globals["__name__"]
        print(f"Trace: {func_name} called at line {lineno} in module {module_name}")
    return trace_calls


def test_function():
    print("Test function is running")
    for _ in range(3):
        time.sleep(1)


def new_fn():
    print("New FN is running")


def worker():
    print("Worker process started")
    test_function()
    new_fn()


if __name__ == "__main__":
    sys.settrace(trace_calls)
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
    sys.settrace(None)
