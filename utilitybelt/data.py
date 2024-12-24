import abc.collections
from typing import Optional, Sequence, Callable, Union, Tuple
import math


class SequenceMixer(abc.collections.Sequence):

    def __init__(self, seqs: Sequence, schedule: Optional[Tuple[int]] = None):
        """
        seqs is a list of sequence types.
        The i^th element of this class instance is

        j, k = schedule_fn(i)
        seqs[j][k % len(seqs[j])]


        if schedule is None, schedule_fn(i) = i % len(seqs), i//len(seqs)
        if schedule is a tuple, then schedule_fn(i) is schedule[i % len(schedule)],  number  of times schedule[p % len(schedule)] = schedule[i % len(schedule)] for p < i
        """

        if schedule is None:
            schedule = list(range(len(seqs)))

        totals = [0 for i in range(len(seqs))]
        intermediates = []
        for i in schedule:
            intermediates.append(totals[i])
            totals[i] += 1

        def schedule_fn(i):
            z = i % len(schedule)
            c = i // len(schedule)

            j = schedule[z]

            k = totals[j] * c + intermediates[z]

            return j, k

        self.schedule = schedule
        self.schedule_fn = schedule_fn
        self.seqs = seqs

        # compute total length
        # first find how many times through the schedule we  need to go  to  exhaust every sequence
        max_epochs = 0
        for i in range(len(seqs)):
            max_epochs = max(max_epochs, math.ceil(len(seqs[i]) / totals[i]))
        self._len = max_epochs * len(schedule)

    def __len__(self):
        return self._len

    def __getitem__(self, idx):
        if idx >= self._len or idx <= -self._len:
            raise IndexError

        if idx < 0:
            idx = self._len + idx

        j, k = self.schedule_fn(idx)
        return self.seqs[j][k % len(self.seqs[j])]
