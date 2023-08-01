from monitors.monitor import Monitor


class MeltingAndFractionManyMonitor(Monitor):
    """This collects whether the DNA is melted and the fraction of DNA base-pairs melted,
    as in melting and fraction monitor, at many different time steps and thresholds.
    By default, it collects melting and fraction observations 100 time steps throughout
    the post preheating steps in an evenly separated manner. And twenty thresholds are chosen
    in between [0.5, 2.5) Angstrom with step size 0.1.
    """

    MELT_FRACTION_TRESHOLDS = [
        i / 10 for i in range(5, 25)
    ]  # start=0.5, end=2.5, step=0.1
    MELT_FRACTION_SIZES = len(MELT_FRACTION_TRESHOLDS)

    # MELT_FRACTION_TIME_STEP = 800
    # MELT_FRACTION_MAX_STEPS = 80000
    MELT_FRACTION_TIME_STEPS = (
        100  # int(MELT_FRACTION_MAX_STEPS/MELT_FRACTION_TIME_STEP) # 100
    )

    def __init__(self, dna, n_preheating_steps) -> None:
        """Initialize MeltingAndFractionManyMonitor object.

        Args:
            dna (DNA): A DNA object.
            n_steps_after_preheating (int): Number of post-preheating steps.
        """
        super(MeltingAndFractionManyMonitor, self).__init__(dna)

        self.n_preheating_steps = n_preheating_steps

        self.melting_fraction_many = [0.0] * self.dna.n_nt_bases
        self.melting_many = [
            [0.0] * self.MELT_FRACTION_SIZES
            for i in range(self.MELT_FRACTION_TIME_STEPS)
        ]  # shape=(MELT_FRACTION_TIME_STEPS, MELT_FRACTION_SIZES)
        self.fraction_many = [
            [0.0] * self.MELT_FRACTION_SIZES
            for i in range(self.MELT_FRACTION_TIME_STEPS)
        ]  # shape=(MELT_FRACTION_TIME_STEPS, MELT_FRACTION_SIZES)

    def collect_at_step(self, step_no):
        """Melting and fraction characteristics are collected at various time steps thoughout the post preheating steps.

        Args:
            step_no (int): Step number.
        """
        for i in range(self.dna.n_nt_bases):
            self.melting_fraction_many[i] += self.dna.coords_dist[i]

        step = step_no - self.n_preheating_steps
        if step % self.MELT_FRACTION_TIME_STEPS == 0:
            time_step = int(step / self.MELT_FRACTION_TIME_STEPS)

            self.__check_melting_and_fraction_many(step, time_step)

    def __check_melting_and_fraction_many(self, step, time_step):
        for thresh_idx in range(self.MELT_FRACTION_SIZES):
            melting, fraction = 1.0, 0.0

            for base_idx in range(self.dna.n_nt_bases):
                if (
                    melting == 1.0
                    and self.melting_fraction_many[base_idx] / (step + 1)
                    < self.MELT_FRACTION_TRESHOLDS[thresh_idx]
                ):
                    melting = 0.0
                    break

                if (
                    self.melting_fraction_many[base_idx] / (step + 1)
                    > self.MELT_FRACTION_TRESHOLDS[thresh_idx]
                ):
                    fraction += 1  # computing total fraction length for this threshold

            self.melting_many[time_step][thresh_idx] += melting
            self.fraction_many[time_step][thresh_idx] += fraction / self.dna.n_nt_bases
