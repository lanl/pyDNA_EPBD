from monitors.monitor import Monitor


class CoordMonitor(Monitor):
    """The coordinate monitor collects each bps distance and squared-distance at every post-preheating step."""

    def __init__(self, dna) -> None:
        """Initialize CoordMonitor object.

        Args:
            dna (DNA): A DNA object.
        """
        super(CoordMonitor, self).__init__(dna)
        self.coord = [0.0] * self.dna.n_nt_bases
        self.coord_square = [0.0] * self.dna.n_nt_bases

    def collect_at_step(self, step_no):
        """Collect bps distance and squared-distance at every post-preheating step.

        Args:
            step_no (int): Step number.
        """
        for i in range(self.dna.n_nt_bases):
            self.coord[i] += self.dna.coords_dist[i]
            self.coord_square[i] += self.dna.coords_dist[i] ** 2
