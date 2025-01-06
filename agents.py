"""The file contains all the agent classes needed for the SIR model."""

from enum import Enum
from mesa import Agent

class State(Enum):
    """Defining the initial state (number) of susceptible, infected, and resistant agents."""
    SUSCEPTIBLE = 0
    INFECTED = 1
    RESISTANT = 2

class VirusAgent(Agent):
    """Individual virus agent definition, properties, and interaction methods."""

    def __init__(
            self,
            model,
            initial_state,

            virus_spread_chance, # The probability of a SUSCEPTIBLE agent becoming INFECTED
            virus_check_frequency, # A function to check if SUSCEPTIBLE agents have become INFECTED
            recovery_chance, # The probability of an INFECTED agent recovering. Note that this does not guarantee becoming RESISTANT 
            gain_resistance_chance, # The probability of an INFECTED agent becoming RESISTANT
    ):
        super().__init__(model)

        # Define the initial state of agents
        self.state = initial_state

        # Define the properties of the agents
        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.recover_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance

    """Define how SUSCEPTIBLE agents become INFECTED"""
    def try_to_infect_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighborhood(
            self.pos, include_center=False
        )
        # Find the SUSCEPTIBLE neighbors
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]
        for a in susceptible_neighbors:
            # If the chance of getting infected for a SUSCEPTIBLE agent is 
            # less than the virus_spread_chance metric, 
            # then the SUSCPTIBLE agent becomes an INFECTED agent
            if self.random.random() < self.virus_spread_chance:
                a.state = State.INFECTED
    
    """Define how INFECTED agents become RESISTANT"""
    def try_gain_resistance(self):
        # If the gain_resistance_chance of the INFECTED agent is 
        # less than the gain_resistance_chance metric
        if self.random.random() < self.gain_resistance_chance:
            # Then the agent is RESISTANT
            self.state = State.RESISTANT
    
    """Define whether an agent is SUSCEPTIBLE or INFECTED based on recovery_chance metric"""
    def try_remove_infection(self):
        # If the recovery_chance of the agent is less than the recovery_chance metric:
        if self.random.random(self) < self.recovery_chance:
            # Then the agent is SUSCEPTIBLE to infection
            self.state = State.SUSCEPTIBLE
            self.try_gain_resistance()
        else:
            # Otherwise, the agent is INFECTED
            self.state = State.INFECTED

    """Check to see if an INFECTED agent can become RESISTANT"""
    def try_check_situation(self):
        if (self.random.random() < self.virus_check_frequency) and (
            self.state is State.INFECTED
        ):
            self.try_remove_infection()
    
    """Define the steps for agents within the model"""
    def step(self):
        # If the agent is INFECTED, they will try to infect their neighbors
        if self.state is State.INFECTED:
            self.try_to_infect_neighbors()
        # If the agent is INFECTED, check the situation to see if the infection
        # can be removed
        self.try_check_situation()
