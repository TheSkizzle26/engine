import inspect
from enum import Enum


class EventBus:
    def __init__(self):
        self._listeners = {}
        self._wildcard_listeners = {}

    def _call_callback(self, callback, *args):
        sig = inspect.signature(callback)
        param_count = len(sig.parameters)

        if param_count == 0:
            callback()
        else:
            callback(*args[:param_count])

    def subscribe(self, event_or_group, callback):
        if isinstance(event_or_group, Enum):
            self._listeners.setdefault(event_or_group, []).append(callback)
        else:
            self._wildcard_listeners.setdefault(event_or_group, []).append(callback)

    def emit(self, event_or_group, data=None):
        for callback in self._listeners.get(event_or_group, []):
            self._call_callback(callback, data)

        for group, callbacks in self._wildcard_listeners.items():
            if isinstance(event_or_group, group):
                for callback in callbacks:
                    self._call_callback(callback, data, event_or_group)


event = EventBus()