"""wraps a function (usually a logging function) in a rate-limiter"""
import time
import eqx
from typing import Callable, Dict, Any, Tuple, Boolean


class RateLimitedFn:
    def __init__(
        self,
        fn: Callable[Dict, Any] = lambda x: None,
        call_period_sec=1.0,
        aggregation="last",
        non_numerical_aggregation="last",
    ):
        self.fn = fn
        self.last_called_time = time.time()

        assert aggregation in ["mean", "sum", "last", "first"]
        assert non_numerical_aggregation in ["last", "first"]
        self.aggregation = aggregation
        self.non_numerical_aggregation = non_numerical_aggregation

        self.call_period_sec = call_period_sec

        self.arg = {}
        self.counts = {}

    def __call__(self, x: Dict) -> Tuple[Any, Boolean]:
        curtime = time.time()

        self.aggregate(x)

        if curtime > self.last_called_time + self.call_period_sec:
            return self.force_call(), True
        else:
            return None, False

    def force_call(self):
        # compute averages if necessary
        finalized_arg = self.finalize_arg()

        result = self.fn(finalized_arg)

        self.arg = {}
        self.counts = {}
        self.last_called_time = time.time()

        return result

    def __del__(self):
        self.force_call()

    def finalize_arg(self):
        finalized_arg = dict(self.arg)
        if self.aggregation == "mean":
            for k in finalized_arg:
                if k in self.counts:
                    finalized_arg[k] = finalized_arg[k] / self.counts[k]

        return finalized_arg

    def aggregate(self, x):
        if self.aggregation == "last":
            self.arg = self.arg | x
        elif self.aggregation == "first":
            self.arg = x | self.arg
        elif self.aggregation == "sum":
            for k in self.arg:
                if eqx.is_array_like(self.arg[k]) and eqx.is_array_like(x[k]):
                    self.arg[k] = self.arg[k] + x[k]
                    if k not in self.counts:
                        self.counts[k] = 0
                    self.counts[k] += 1
                else:
                    if self.fallback_aggregation == "last":
                        self.arg[k] = x[k]
