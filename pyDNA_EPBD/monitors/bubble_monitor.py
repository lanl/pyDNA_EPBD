from monitors.monitor import Monitor


class BubbleMonitor(Monitor):
    """The bubble monitor collects DNA bubbles for each bp at different thresholds.
    For a threshold, if a bps distance is more than the threshold, it computes the
    bubble length starting from that bp until the next bps distance is less
    than the threshold. In this implementation, the minimum and maximum bubble length are
    considered in between 3 and 20, inclusive. The number of thresholds are set to 20 by
    default from 0.5 Angstrom to 10.5 Angstrom with step size 0.5 Angstrom.
    """

    TRESHOLDS = [i / 10 for i in range(5, 105, 5)]  # start=.5, end=10.5, step.5
    TRESHOLD_SIZE = len(TRESHOLDS)
    MIN_BUB_ELEM, MAX_BUB_ELEM = 3, 20

    def __init__(self, dna) -> None:
        """Initialize BubbleMonitor object.

        Args:
            dna (DNA): A DNA object.
        """
        super(BubbleMonitor, self).__init__(dna)
        self.bubbles = [
            [[0] * self.TRESHOLD_SIZE for _ in range(self.MAX_BUB_ELEM)]
            for _ in range(self.dna.n_nt_bases)
        ]  # shape=(n_nt_bases, MAX_BUB_ELEM, TRESHOLD_SIZE)

    def collect_at_step(self, step_no):
        """Collects bubbles at every post-preheating steps.

        Args:
            step_no (int): Step number.
        """
        # bubbles are collected at every temperature
        for base_idx in range(self.dna.n_nt_bases):  # for each base
            for tr_idx in range(self.TRESHOLD_SIZE):  # for each threshold
                R = 0
                p = base_idx
                tr = self.TRESHOLDS[tr_idx]
                while self.dna.coords_dist[p] >= tr and R + 1 < self.dna.n_nt_bases:
                    R += 1
                    p = base_idx + R
                    if p >= self.dna.n_nt_bases:
                        p = p - self.dna.n_nt_bases  # - 1
                    if R >= self.MIN_BUB_ELEM:
                        length = min(R, self.MAX_BUB_ELEM - 1)
                        self.bubbles[base_idx][length][tr_idx] += 1
                if R == 0:
                    break
