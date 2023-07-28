import sys

sys.path.append("../pyDNA_EPBD")

from simulation.constants import *


class DNA:
    """The DNA object for MCMC simulation."""

    def __init__(self, seq) -> None:
        """Initialize a DNA object from an input DNA sequence.

        Args:
            seq (str): A DNA sequence. The characters are supposed to be in {A,C,G,T} (upper case).
        """
        super(DNA, self).__init__()

        self.seq = seq
        self.n_nt_bases = len(seq)  # nt: nucleotide
        self.reset()

    def reset(self):
        """A DNA object is initialized with coordinates (left and right bases),
        the distances among them, bp energies, total energy, stacking terms,
        hydrogen bond types and other constants.
        """
        self.coords_state = self.__init_coords()  # DNA, u and v
        self.coords_dist = self.__init_coords_dist()  # y

        self.bp_energies = self.__init_energy()  # energies for each base-pairs
        self.total_energy = 0.0

        self.DA, self.kn = self.__init_stacking_terms()
        self.kn_div_four = [i * 0.25 for i in self.kn]
        self.DA_div_sqrt_two = [
            [j * one_div_sqrt2 for j in self.DA[i]] for i in range(self.n_nt_bases)
        ]

    def __init_coords(self):
        """Private method for initializing coordinates (u (left) and v (right) bases).

        Returns:
            list: Bp coordinates.
        """
        # 0, 1: u, v
        return [[0.0] * 2 for _ in range(self.n_nt_bases)]

    def __init_coords_dist(self):
        """Private method for initializing bp distances (y_n).

        Returns:
            list: Bp distances.
        """
        # y = (u-v)/sqrt(2)
        return [0.0] * self.n_nt_bases

    def __init_energy(self):
        """Private method for initializing bp energies.

        Returns:
            list: Bp energies
        """
        # 0, 1: Umors, Wstack
        return [[0.0] * 2 for _ in range(self.n_nt_bases)]

    def __str__(self):
        return f"{self.coords_state}"

    def __init_stacking_terms(self):
        """Private method for initializing bp stacking constants.

        Returns:
            list, list: Bp nature (DA), coupling constants between the left and right two neighboring bases.
        """
        seq = self.seq
        # D and A values for computing Morse-potentials for each base-pair

        DA = [[0.0] * 2 for _ in range(self.n_nt_bases)]  # 0 -> D_n, 1 -> a_n
        kn = [0.0] * self.n_nt_bases

        for i in range(self.n_nt_bases):
            # next base index
            if i + 1 >= self.n_nt_bases:  # circular stacking
                k1 = 0
            else:
                k1 = i + 1

            if seq[i] == "G":
                DA[i][0] = DGC
                DA[i][1] = aGC

                if seq[k1] == "G":
                    kn[k1] = GG
                elif seq[k1] == "T":
                    kn[k1] = GT
                elif seq[k1] == "A":
                    kn[k1] = GA
                elif seq[k1] == "C":
                    kn[k1] = GC
                else:
                    print("G Wrong DNA input structure!", i)

            elif seq[i] == "C":
                DA[i][0] = DGC
                DA[i][1] = aGC

                if seq[k1] == "G":
                    kn[k1] = CG
                elif seq[k1] == "T":
                    kn[k1] = CT
                elif seq[k1] == "A":
                    kn[k1] = CA
                elif seq[k1] == "C":
                    kn[k1] = CC
                else:
                    print("C Wrong DNA input structure!", i)

            elif seq[i] == "T":
                DA[i][0] = DAT
                DA[i][1] = aAT

                if seq[k1] == "G":
                    kn[k1] = TG
                elif seq[k1] == "T":
                    kn[k1] = TT
                elif seq[k1] == "A":
                    kn[k1] = TA
                elif seq[k1] == "C":
                    kn[k1] = TC
                else:
                    print("T Wrong DNA input structure!", i)

            elif seq[i] == "A":
                DA[i][0] = DAT
                DA[i][1] = aAT

                if seq[k1] == "G":
                    kn[k1] = AG
                elif seq[k1] == "T":
                    kn[k1] = AT
                elif seq[k1] == "A":
                    kn[k1] = AA
                elif seq[k1] == "C":
                    kn[k1] = AC
                else:
                    print("T Wrong DNA input structure!", i)

        return DA, kn


#