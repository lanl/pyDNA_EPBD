from pydna_epbd.simulation.dna import DNA


class Monitor:
    """The monitor to collect various aspects of the simulation."""

    def __init__(self, dna: DNA) -> None:
        """Initialize Monitor object for the input DNA object.

        Args:
            dna (DNA): A DNA object.
        """
        super(Monitor, self).__init__()
        self.dna = dna

    def update_state(self, seq_id, temp, iter_no):
        """State of a monitor

        Args:
            seq_id (str): Sequence id.
            temp (float): Simulation temperature.
            iter_no (int): Iteration number.
        """
        self.seq_id = seq_id
        self.temp_idx = temp
        self.iter_no = iter_no

    def collect_at_step(self, step_no):
        """The characteristics to collect at post-preheating steps.
        Abstract method to be implemented by the child monitors,
        to collect specific aspects of the MCMC simulation.

        Args:
            step_no (int): Iteration number.

        Raises:
            NotImplementedError: The child monitors must implement this.
        """
        raise NotImplementedError()

    def collect_at_step_preheat(self, step_no):
        """The characteristics to collect at preheating steps.
        Optional, since not all child monitors need to record at preheating steps.

        Args:
            step_no (int): Iteration number.
        """
        pass

    def collect_at_iter(self):
        """The characteristics to collect at the end of each iteration.
        The corresponding iteration number is updated in the update_state function
        Optional, since not all child monitors need to record at iteration end.
        """
        pass

    def collect_at_temp(self):
        """The characteristics to collect specifically for each temperature.
        The corresponding temperature is updated in the update_state function
        Optional, since not all child monitors need to record at temperature end.
        """
        pass
