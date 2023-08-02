from pydna_epbd.monitors.flipping_monitor import Monitor


class FlippingMonitorVerbose(Monitor):
    """The flipping verbose monitor collects flipping characteristics for different thresholds."""

    FLIP_CUTOFF = [
        0.707106781186548 * i for i in range(1, 6)
    ]  # [0.707106781186548, 1.414213562373096, 2.121320343559644, 2.828427124746192, 3.53553390593274]
    FLIP_SIZES = len(FLIP_CUTOFF)

    def __init__(self, dna) -> None:
        """initialize FlippingMonitor object.

        Args:
            dna (DNA): A DNA object.
        """
        super(FlippingMonitorVerbose, self).__init__(dna)
        self.flip = [
            [0.0] * self.FLIP_SIZES for i in range(self.dna.n_nt_bases)
        ]  # shape=(n_nt_bases, FLIP_SIZE)

    def collect_at_step(self, step_no):
        """Collects flipping characteristics considering different thresholds.

        Args:
            step_no (int): Step number.
        """
        for i in range(self.dna.n_nt_bases):
            for j in range(self.FLIP_SIZES):
                if self.dna.coords_dist[i] >= self.FLIP_CUTOFF[j]:
                    self.flip[i][j] += 1
