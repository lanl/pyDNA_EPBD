"""The switches activate the monitors to record the observations throughout the MCMC simulation.
"""
import os

os.environ["BUBBLE_MONITOR"] = "True"
os.environ["ENERGY_MONITOR"] = "False"
os.environ["COORD_MONITOR"] = "True"
os.environ["FLIPPING_MONITOR"] = "False"
os.environ["FLIPPING_MONITOR_VERBOSE"] = "True"
os.environ["MELTING_AND_FRACTION_MONITOR"] = "False"
os.environ["MELTING_AND_FRACTION_MANY_MONITOR"] = "False"
