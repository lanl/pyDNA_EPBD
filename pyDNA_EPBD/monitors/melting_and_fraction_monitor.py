from monitors.monitor import Monitor


class MeltingAndFractionMonitor(Monitor):
    """Melting and fraction characteristics recording monitor at predefined threhold.
    At the end of each iteration, this monitor decides whether the DNA is melted or not at every bp by checking
    that any of the bp's average coordinate distance is less than a predefined melting threshold (here 0.5 Angstrom).
    In another word, if all bps average coordinate distance is more or equal to the threshold, then it is melted.
    In addition, the fraction computes the fraction of bps that have melted. Therefore, if the DNA melted, the fraction is 1.0.
    """

    MELT_FRACTION_TRESHOLD = 0.5

    def __init__(self, dna, n_steps_after_preheating) -> None:
        """Initialize MeltingAndFractionMonitor object.

        Args:
            dna (DNA): A DNA object.
            n_steps_after_preheating (int): Number of post-preheating steps.
        """
        super(MeltingAndFractionMonitor, self).__init__(dna)
        self.n_steps_after_preheating = n_steps_after_preheating
        self.melting, self.fraction = 0.0, 0.0
        self.melting_fraction = [0.0] * self.dna.n_nt_bases

    def collect_at_step(self, step_no):
        """Melting and fraction characteristics are collected at step_no.

        Args:
            step_no (int): Step number.
        """
        for i in range(self.dna.n_nt_bases):
            self.melting_fraction[i] += self.dna.coords_dist[i]

    def collect_at_iter(self):
        """Melting and fraction characteristics are collected at the end of the iteration."""
        melting, fraction = 1.0, 0.0
        for i in range(self.dna.n_nt_bases):
            if (
                melting == 1.0
                and (self.melting_fraction[i] / self.n_steps_after_preheating)
                < self.MELT_FRACTION_TRESHOLD
            ):
                melting = 0.0  # 0.0 means did not melt the whole DNA

            if (
                self.melting_fraction[i] / self.n_steps_after_preheating
            ) > self.MELT_FRACTION_TRESHOLD:
                fraction += 1  # total number of base pairs whose distance is >MELT_FRACTION_TRESHOLD

        self.melting = melting  # if melting is 1.0, then the fraction should be 1.0, because the whole DNA melted.
        self.fraction = (
            fraction / self.dna.n_nt_bases
        )  # fraction of the bps got melted.
