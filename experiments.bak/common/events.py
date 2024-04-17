from multiprocessing import Event as EventFactory
from multiprocessing.synchronize import Event
from enum import Enum


class EventName(Enum):
    # Worker events
    STARTED_EXPERIMENT = "STARTED_EXPERIMENT"
    LOADED_DATASET = "LOADED_DATASET"
    EXECUTED_ATTRIBUTE = "EXECUTED_ATTRIBUTE"
    FINISHED_EXPERIMENT = "FINISHED_EXPERIMENT"
    EXITED = "EXITED"

    # Memory usage watcher events
    STARTED_MEMORY_USAGE_WATCHER = "STARTED_MEMORY_USAGE_WATCHER"
    MEASURED_MEMORY_USAGE = "MEASURED_MEMORY_USAGE"

    # Execution time watcher events
    STARTED_EXECUTION_TIME_WATCHER = "STARTED_EXECUTION_TIME_WATCHER"
    MEASURED_EXECUTION_TIME = "MEASURED_EXECUTION_TIME"


class EventDispatcher:
    events = {
        EventName.STARTED_EXPERIMENT: EventFactory(),
        EventName.LOADED_DATASET: EventFactory(),
        EventName.EXECUTED_ATTRIBUTE: EventFactory(),
        EventName.FINISHED_EXPERIMENT: EventFactory(),
        EventName.STARTED_MEMORY_USAGE_WATCHER: EventFactory(),
        EventName.MEASURED_MEMORY_USAGE: EventFactory(),
        EventName.STARTED_EXECUTION_TIME_WATCHER: EventFactory(),
        EventName.MEASURED_EXECUTION_TIME: EventFactory(),
        EventName.EXITED: EventFactory(),
    }

    barrier_events: list[Event]

    def __init__(self, barrier_event_names: list[EventName] = []) -> None:
        self.barrier_events = self.__get_events(barrier_event_names)

    def dispatch(
        self,
        event_name: EventName,
        sync: bool = False,
    ) -> None:
        event = self.events[event_name]
        event.set()

        if sync:
            self.sync()

    def sync(self) -> None:
        for event in self.barrier_events:
            event.wait()

        for event in self.barrier_events:
            event.clear()

    def wait(self, event_name: EventName, timeout: float | None = None) -> bool:
        return self.events[event_name].wait(timeout=timeout)

    def wait_watchers_start(self) -> None:
        watcher_start_events = self.__get_events(
            [
                EventName.STARTED_MEMORY_USAGE_WATCHER,
                EventName.STARTED_EXECUTION_TIME_WATCHER,
            ]
        )

        for event in watcher_start_events:
            event.wait()

    def is_event_set(self, event_name: EventName) -> bool:
        return self.events[event_name].is_set()

    def get_next(self, event_name_list: list[EventName]) -> EventName:
        for event_name in event_name_list:
            if not self.events[event_name].is_set():
                return event_name

    def reset(self) -> None:
        for event in self.events.values():
            event.clear()

    def worker_exited(self) -> bool:
        return self.is_event_set(EventName.EXITED)

    def __get_events(self, event_names: list[EventName]) -> list[Event]:
        return [self.events[event_name] for event_name in event_names]
