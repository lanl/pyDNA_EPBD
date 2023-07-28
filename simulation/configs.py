import sys

sys.path.append("../pyDNA_EPBD")


# from dataclasses import dataclass
# @dataclass(frozen=True)
class InputLimits:  # immutable, not using decorator which makes codes slower
    MAX_SEEDS = 4000
    MAX_SEQUENCES = 25000
    MAX_TEMPERATURES = 150

    MAX_BASES = 20000
    MAX_STRING_LENGTH = 256


class InputConfigs:
    """Input configuration object to use throughout the simulation."""

    def __init__(
        self,
        temperature: float,
        sequences: list,
        outputs_dir: str,
        n_iterations: int,
        n_preheating_steps: int,
        n_steps_after_preheating: int,
        n_nodes: int,
        save_full=False,
        save_runtime=False,
    ) -> None:
        """Initializes input configuration object.

        Args:
            temperature (float): In Kelvin scale.
            sequences (list): List of tuples of sequences in [("output_dir", "seq_id", "seq")] format
            outputs_dir (str): The directory path to save the simulation outputs.
            n_iterations (int): The number of independent iterations with different initial conditions.
            n_preheating_steps (int): The number of preheating steps.
            n_steps_after_preheating (int): The number of post preheating steps.
            n_nodes (int): The computing nodes where the input sequences are divided equally for faster execution of bulk sequences.
            save_full (bool, optional): Whether or not save the full outputs of the simulation. If True, first axis denotes n_iterations. Defaults to False.
            save_runtime (bool, optional): Whether or not save the runtime for each sequence. Defaults to False.
        """
        self.n_iterations = n_iterations

        self.n_preheating_steps = n_preheating_steps
        self.n_steps_after_preheating = n_steps_after_preheating
        self.total_steps = n_preheating_steps + n_steps_after_preheating

        self.outputs_dir = outputs_dir

        self.n_nodes = n_nodes

        self.sequences = sequences
        self.n_sequences = len(sequences)

        self.temperature = temperature

        self.save_full = save_full
        self.save_runtime = save_runtime

        print("An example input seq: ", self.sequences[0])

    def __str__(self) -> str:
        return (
            f"\t#-Iterations: {self.n_iterations}\n\t#-PreheatingSteps: {self.n_preheating_steps}\n\t#-PostPreheatingSteps: {self.n_steps_after_preheating}\n\t"
            f"#-TotalSteps: {self.total_steps}\n\t#-Sequences: {self.n_sequences}\n\tTemperature: {self.temperature}K\n\t"
            f"#-Nodes: {self.n_nodes}\n\tOutputsDir: {self.outputs_dir}\n\tIsSavingFull: {self.save_full}\n\tIsSavingRuntime: {self.save_runtime}"
        )
