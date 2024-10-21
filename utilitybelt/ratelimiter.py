"""wraps a function (usually a logging function) in a rate-limiter"""
import time
from typing import Callable, Dict, Any, Tuple



class RateLimitedFn:
    def __init__(
        self,
        fn: Callable[Dict, Any] = lambda x: None,
        call_period_sec=1.0,
        aggregation="last",
    ):
        self.fn = fn
        self.last_called_time = time.time()

        assert aggregation in ["last", "first"]
        self.aggregation = aggregation

        self.call_period_sec = call_period_sec

        self.arg = {}

    def __call__(self, x: Dict) -> Tuple[Any, bool]:
        curtime = time.time()

        self.aggregate(x)

        if curtime > self.last_called_time + self.call_period_sec:
            return self.force_call(), True
        else:
            return None, False

    def force_call(self):

        result = self.fn(self.arg)

        self.arg = {}
        self.counts = {}
        self.last_called_time = time.time()

        return result

    def __del__(self):
        self.force_call()


    def aggregate(self, x):
        if self.aggregation == "last":
            self.arg = self.arg | x
        elif self.aggregation == "first":
            self.arg = x | self.arg
