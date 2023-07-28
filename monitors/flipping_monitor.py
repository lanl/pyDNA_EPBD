import sys

sys.path.append("../pyDNA_EPBD")

from monitors.monitor import Monitor


class FlippingMonitor(Monitor):
    """The flipping monitor collects flipping characteristics for each bp at every post preheating steps
    at a predefined threshold.
    """

    FLIP_CUTOFF = 0.707106781186548  # correspond to 0.5A and 1.5A

    def __init__(self, dna) -> None:
        """initialize FlippingMonitor object.

        Args:
            dna (DNA): A DNA object.
        """
        super(FlippingMonitor, self).__init__(dna)
        self.flip = [0.0] * self.dna.n_nt_bases  # shape=(n_nt_bases, FLIP_SIZE)

    def collect_at_step(self, step_no):
        """Collects flipping characteristics.

        Args:
            step_no (int): Step number.
        """
        for i in range(self.dna.n_nt_bases):
            if self.dna.coords_dist[i] >= self.FLIP_CUTOFF:
                self.flip[i] += 1

