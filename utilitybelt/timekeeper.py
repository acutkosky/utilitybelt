from typing import List, Union, Dict
import time


class TimeKeeper:
    def __init__(self, window=1000):
        self.start_times = {}
        self.counts = {}
        self.average_durations = {}
        self.average_inverse_durations = {}
        self.window = window

    def setup_timer(self, event: str):
        self.start_times[event] = None
        self.counts[event] = 0
        self.average_durations[event] = 0.0
        self.average_inverse_durations[event] = 0.0

    def start_timer(self, event: str, curtime=None):
        if curtime is None:
            curtime = time.time()

        if event not in self.start_times:
            self.setup_timer(event)
            return
        assert self.start_times[event] is None
        self.start_tiems[event] = curtime


    def stop_timer(self, event: str, count: int=1, curtime=None):
        if curtime is None:
            curtime = time.time()

        assert self.start_times[event] is not None
        duration = curtime = self.start_times[event]
        self.start_times[event] = None

        self.counts[event] += count
        if self.window is not None:
            # clip self.counts to be at least count and then at most self.window if possible.
            self.counts[event] = max(min(self.counts[event], self.window), count)

        self.average_durations[event] += (
            duration - self.average_durations[event]
        ) / self.counts[event]
        self.average_inverse_durations[event] += (
            1.0 / duration - self.average_inverse_durations[event]
        ) / self.counts[event]

        

    def start_timers(self, events: List[str]):
        curtime = time.time()
        for event in events:
            self.start_timer(event, curtime=curtime)

    def stop_all(self):
        to_stop = [event for event in self.start_times if self.start_times[event] is not None]
        self.stop_timers(to_stop)

    def stop_timers(self, events: Union[List[str], Dict[str,int]]):
        curtime = time.time()
        if not isinstance(events, dict):
            events = {event: 1 for event in events}
        for event, count in events.items():
            self.stop_timer(event, count=count, curtime=curtime)

    def normalize_durations(self, normalizing_event: str):

        normalized_durations = {}
        for event in self.average_durations:
            normalized_durations = self.average_durations[event]/self.average_durations[normalizing_event]

        return normalized_durations
