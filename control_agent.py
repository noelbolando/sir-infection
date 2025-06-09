"""
The file contains the class and call functions for the ControlAgent.
For this model, we are using an Ollama LLM agent
"""

import json
import math
from mesa import Model

from agents import State

class ControlAgent(Model):
    """
    Control Agents to monitor the status of the simulation.
    Allows users to interact with and prompt the simulation.
    """

    def __init__(
            self, 
            model_getter,
            llm_fn=None
    ):
        self._get_model = model_getter
        self.llm_fn = llm_fn
        self.history = [
             {
                "role": "system", 
                "content": "You are a simulation assistant that knows how to interpret model state."
            }
        ]
 
    # Function to retrieve model information
    def get_model_snapshot(self):
        model = self._get_model()

        infected = sum(1 for a in model.grid.get_all_cell_contents()
                       if a.state is State.INFECTED)
        susceptible = sum(1 for a in model.grid.get_all_cell_contents() 
                        if a.state is State.SUSCEPTIBLE)
        resistant = sum(1 for a in model.grid.get_all_cell_contents() 
                        if a.state is State.RESISTANT)
        ratio = model.resistant_susceptible_ratio()

        return (
            f"The model has {model.num_nodes} agents. "
            f"Currently, there are {infected} infected, {susceptible} susceptible, " 
            f"and {resistant} resistant agents. "
            f"The infection rate is {model.virus_spread_chance}, "
            f"and the recovery chance is {model.recovery_chance}. "
            f"The resistant-to-susceptible ratio is {'∞' if ratio == math.inf else round(ratio, 2)}. "
        )

    # Function to handle user queries 
    def handle_query(self, user_input: str) -> str:
        context = self.get_model_snapshot()
        self.history.append(
            {
                "role": "user", 
                "content": f"{context}\n\nUser query: {user_input}"
            }
        )
        response = self.llm_fn(self.history)
        self.history.append(
            {
                "role": "assistant", 
                "content": response
            }
        )
        return response
    
    def get_conversation(self):
        return self.history[1:]
