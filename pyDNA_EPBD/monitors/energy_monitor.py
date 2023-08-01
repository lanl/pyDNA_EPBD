from monitors.monitor import Monitor


class EnergyMonitor(Monitor):
    """The energy monitor collects total energy (in Kelvin) at every preheating and post preheating step."""

    KB = 0.0000861733034

    def __init__(self, dna, total_steps) -> None:
        """Initialize EnergyMonitor object.

        Args:
            dna (DNA): A DNA object.
            total_steps (int): Total number of steps.
        """
        super(EnergyMonitor, self).__init__(dna)
        self.energy = [0.0] * total_steps

    def collect_at_step(self, step_no):
        """Collect energies at post-preheating steps.

        Args:
            step_no (int): Step number.
        """
        temp = self.dna.total_energy / (
            self.KB * self.dna.n_nt_bases
        )  # computing temperature from energy
        self.energy[step_no] += temp

    def collect_at_step_preheat(self, step_no):
        """Collect energies at preheating steps.

        Args:
            step_no (int): Step number.
        """
        self.collect_at_step(step_no)
