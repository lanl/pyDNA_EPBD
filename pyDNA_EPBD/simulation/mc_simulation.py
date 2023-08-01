from math import log, exp
from random import random, normalvariate

from simulation.dna import DNA
from monitors.all_monitors import Monitors
from simulation.constants import ro, beta1_div_sqrt_two, one_div_sqrt2


class Simulation:
    def __init__(self, dna: DNA) -> None:
        """Init Simulation object.

        Args:
            dna (DNA): A DNA object to run simulation on it.
        """
        super(Simulation, self).__init__()
        self.dna = dna
        self.coords_state_saved = [[0.0] * 2 for _ in range(self.dna.n_nt_bases)]

        # https://en.wikipedia.org/wiki/Boltzmann_constant in eV/K
        self.KB = 0.0000861733034
        self.ACCEPT_CUTOFF = 25.00

    def init_temp(self, temperature):
        """Init simulation temperature.

        Args:
            temperature (float): Temperature in Kelvin.
        """
        self.beta_div_one = self.KB * temperature

    def execute(self, monitors: Monitors, total_steps, preheating_steps):
        """Execute the simulation for total_steps (preheating+post_preheating).

        Args:
            monitors (Monitors): Record different aspects of MCMC simulation of pyDNA-EPBD model.
            total_steps (int): Preheating steps + Post preheating steps.
            preheating_steps (int): Number of preheating steps, when mostly monitors do not collect anything.
        """
        for step_no in range(total_steps):
            # self.__one_move()
            for i in range(self.dna.n_nt_bases):  # a major drawback
                self.__move_bp()

            if step_no < preheating_steps:
                monitors.collect_at_step_preheat(step_no)
            else:
                monitors.collect_at_step(step_no)

    def __move_bp(self):
        """Moves a randomly selected bp and updates new DNA state and corresponding energy."""
        n = int(
            self.dna.n_nt_bases * random()
        )  # selecting random n-th base-pair, get_random_displacement()

        # n_next = (n + 1) % self.dna.n_nt_bases
        # n_previous = (n - 1 + self.dna.n_nt_bases) % self.dna.n_nt_bases
        n_next = n + 1
        if n_next >= self.dna.n_nt_bases:
            n_next = 0
        n_previous = n - 1
        if n_previous < 0:
            n_previous = self.dna.n_nt_bases - 1

        # changing the n-th base pair's coordinate to the direction
        self.__do_random_displacement(n)

        # recalculating the energy
        etotal = (
            self.dna.total_energy
            - self.dna.bp_energies[n][0]
            - self.dna.bp_energies[n][1]
            - self.dna.bp_energies[n_next][1]
        )
        u2 = self.__Umors(n)
        w1, w3 = self.__Wstack(n_previous, n, n_next)
        etotal += u2 + w1 + w3

        # checking energy and Metropolis criteria
        if self.dna.total_energy == etotal:
            # equal energy exit the function
            return
        if etotal < self.dna.total_energy:
            # we are reducing the energy of the system
            self.__assign_new_state(n, n_next, u2, w1, w3, etotal)
        else:
            # kind of exploration
            DELTA_E = self.dna.total_energy - etotal
            # diff of previous energy and current energy
            if DELTA_E > self.beta_div_one * log(random()):
                # if Metropolis criteria is OK
                self.__assign_new_state(n, n_next, u2, w1, w3, etotal)
            else:
                self.__revert_old_state(n)

    def __assign_new_state(self, n, n_next, u2, w1, w3, etotal):
        """Assign new DNA state by updating coordinates, coordinate distance and
        bps Morse and stacking potentials.

        Args:
            n (int): n-th bp.
            n_next (int): Next of n-th bp. Can be circular.
            u2 (float): Morse potential of n-th bp.
            w1 (float): Stacking potential between n and n_previous bps.
            w3 (float): Stacking potential between n and n_next bps.
            etotal (float): New energy due to the bp movement.
        """
        # coordinates
        self.coords_state_saved[n][0] = self.dna.coords_state[n][0]
        self.coords_state_saved[n][1] = self.dna.coords_state[n][1]

        # energy
        self.dna.total_energy = etotal
        self.dna.bp_energies[n][0] = u2
        self.dna.bp_energies[n][1] = w1
        self.dna.bp_energies[n_next][1] = w3

        # y_n
        self.dna.coords_dist[n] = (
            self.dna.coords_state[n][0] - self.dna.coords_state[n][1]
        ) * one_div_sqrt2

    def __revert_old_state(self, n):
        """Revert to old state.

        Args:
            n (int): n-th bp.
        """
        self.dna.coords_state[n][0] = self.coords_state_saved[n][0]
        self.dna.coords_state[n][1] = self.coords_state_saved[n][1]
        # bp_energies and total_energy are calculated but not updated, so do not need to revert

    def __Umors(self, n):
        """Computes Morse potentials at n-th bp.

        Args:
            n (int): n-th bp.

        Returns:
            float: Computed Morse potential.
        """
        y_n = self.dna.coords_state[n][0] - self.dna.coords_state[n][1]
        Dn = self.dna.DA[n][0]
        An_div_sqrt_two = self.dna.DA_div_sqrt_two[n][1]

        return Dn * (exp(-An_div_sqrt_two * y_n) - 1) ** 2

    def __Wstack(self, n_previous, n, n_next):
        """Computes stacking potentials. The relation between n_previous and n_next with n-th bp can be circular.

        Args:
            n_previous (int): Previous bp of n-th bp.
            n (int): n-th bp.
            n_next (int): Next bp of n-th bp.

        Returns:
            float, float: Stacking potentials between n- and n-previous bps, and n- and n-next bps.
        """
        y_n_previous = (
            self.dna.coords_state[n_previous][0] - self.dna.coords_state[n_previous][1]
        )
        y_n = self.dna.coords_state[n][0] - self.dna.coords_state[n][1]
        y_n_next = self.dna.coords_state[n_next][0] - self.dna.coords_state[n_next][1]

        Kn_div_four = self.dna.kn_div_four[n]
        w1 = (
            Kn_div_four
            * (1 + ro * exp(-beta1_div_sqrt_two * (y_n_previous + y_n)))
            * (y_n_previous - y_n) ** 2
        )

        Kn_div_four = self.dna.kn_div_four[n_next]
        w3 = (
            Kn_div_four
            * (1 + ro * exp(-beta1_div_sqrt_two * (y_n_next + y_n)))
            * (y_n_next - y_n) ** 2
        )
        return w1, w3

    def __do_random_displacement(self, n):
        """This changes the new coordinate state and keep intact of the coorditate state.

        Args:
            n (int): n-th bp.
        """

        dx = normalvariate(mu=0.0, sigma=1.0)  # get_gasdev()
        if random() > 0.5:  # LEFT, get_l_or_r()
            self.dna.coords_state[n][0] += dx
            if (
                abs(self.dna.coords_state[n][0] - self.coords_state_saved[n][1])
                > self.ACCEPT_CUTOFF
            ):
                self.dna.coords_state[n][0] -= dx  # reverting the change

        else:  # RIGHT
            self.dna.coords_state[n][1] += dx
            if (
                abs(self.dna.coords_state[n][1] - self.coords_state_saved[n][0])
                > self.ACCEPT_CUTOFF
            ):
                self.dna.coords_state[n][1] -= dx  # reverting the change
