"""wraps a function (usually a logging function) in a rate-limiter"""
import time
from typing import Callable, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


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
            logging.debug(f"rate limited function call with args: {self.arg}")
            return self._force_call()
        else:
            return None, False

    def force_call(self):
        logging.debug("forced rate limited function call.")
        return self._force_call()
        

    def _force_call(self):

        result = self.fn(self.arg)

        self.arg = {}
        self.last_called_time = time.time()

        return result, True

    def aggregate(self, x):
        if self.aggregation == "last":
            self.arg = self.arg | x
        elif self.aggregation == "first":
            self.arg = x | self.arg
