from ..events import EventDispatcher
from .constants import MEMORY_USAGE_RESULTS_NAME, EXECUTION_TIME_RESULTS_NAME


def reset_watcher_results(
    watcher_results: dict, event_dispatcher: EventDispatcher
) -> None:
    event_dispatcher.reset()
    watcher_results[MEMORY_USAGE_RESULTS_NAME] = []
    watcher_results[EXECUTION_TIME_RESULTS_NAME] = []
