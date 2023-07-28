import os
import sys

sys.path.append("../pyDNA_EPBD")

from monitors.bubble_monitor import BubbleMonitor
from monitors.coord_monitor import CoordMonitor
from monitors.energy_monitor import EnergyMonitor
from monitors.flipping_monitor import FlippingMonitor
from monitors.flipping_monitor_verbose import FlippingMonitorVerbose
from monitors.melting_and_fraction_monitor import MeltingAndFractionMonitor
from monitors.melting_and_fraction_many_monitor import MeltingAndFractionManyMonitor


class Monitors:
    """All monitors to apply for the same DNA object."""

    def __init__(self, dna, n_preheating_steps, n_steps_after_preheating) -> None:
        """Initialize all the monitors if the corresponding switches are on/off.

        Args:
            dna (DNA): A DNA object.
            n_preheating_steps (int): Number of preheating steps.
            n_steps_after_preheating (int): Number of post-preheating steps.
        """
        super(Monitors, self).__init__()
        total_steps = n_preheating_steps, n_steps_after_preheating
        self.monitors = []

        if os.environ["BUBBLE_MONITOR"] == "True":
            self.bubble_monitor = BubbleMonitor(dna)
            self.monitors.append(self.bubble_monitor)

        if os.environ["COORD_MONITOR"] == "True":
            self.coord_monitor = CoordMonitor(dna)
            self.monitors.append(self.coord_monitor)

        if os.environ["FLIPPING_MONITOR"] == "True":
            self.flipping_monitor = FlippingMonitor(dna)
            self.monitors.append(self.flipping_monitor)

        if os.environ["FLIPPING_MONITOR_VERBOSE"] == "True":
            self.flipping_monitor_verbose = FlippingMonitorVerbose(dna)
            self.monitors.append(self.flipping_monitor_verbose)

        if os.environ["ENERGY_MONITOR"] == "True":
            self.energy_monitor = EnergyMonitor(dna, total_steps)
            self.monitors.append(self.energy_monitor)

        if os.environ["MELTING_AND_FRACTION_MONITOR"] == "True":
            self.melting_and_fraction_monitor = MeltingAndFractionMonitor(
                dna, n_steps_after_preheating
            )
            self.monitors.append(self.melting_and_fraction_monitor)

        if os.environ["MELTING_AND_FRACTION_MANY_MONITOR"] == "True":
            self.melting_and_fraction_many_monitor = MeltingAndFractionManyMonitor(
                dna, n_preheating_steps
            )
            self.monitors.append(self.melting_and_fraction_many_monitor)

        # if os.environ['COORD_VERBOSE_MONITOR'] == 'True':
        #     self.monitors.append(CoordMonitorVerbose(dna, input_configs))

    def update_state(self, seq_id, temp, iter_no):
        """Update state for all monitors.

        Args:
            seq_id (str): Sequence id.
            temp (float): Simulation temperature.
            iter_no (int): Iteration number.
        """
        for monitor in self.monitors:
            monitor.update_state(seq_id, temp, iter_no)

    def collect_at_step(self, step_no):
        """Call monitors to record at post-preheating steps.

        Args:
            step_no (int): Step number.
        """
        for monitor in self.monitors:
            monitor.collect_at_step(step_no)

    def collect_at_step_preheat(self, step_no):
        """Call monitors to record at preheating steps.

        Args:
            step_no (int): Step number.
        """
        for monitor in self.monitors:
            monitor.collect_at_step_preheat(step_no)

    def collect_at_iter(self):
        """Call monitors to record at the end of iterations."""
        for monitor in self.monitors:
            monitor.collect_at_iter()

