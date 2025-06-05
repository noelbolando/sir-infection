"""
The file contains the class and call functions for the ControlAgent.
For this model, we are using an Ollama LLM agent
"""

import json
from mesa import Model

from agents import State

class ControlAgent(Model):
    """
    Control Agents to monitor the status of the simulation.
    Allows users to interact with and prompt the simulation.
    """

    def __init__(
            self, 
            model, 
            llm_fn=None
    ):
        self.model = model
        self.llm_fn = llm_fn
        self.history = [
            {
                "role": "system",
                "content": "You are a helpful assistant for understanding and controlling an agent-based SIR virus model simulation."
            }
        ]

    # Function to gain model snapshot and agent states
    def get_model_snapshot(self):
        return {
            "num_nodes": self.model.num_nodes,
            "virus_spread_chance": self.model.virus_spread_chance,
            "virus_check_frequency": self.model.virus_check_frequency,
            "recovery_chance": self.model.recovery_chance,
            "gain_resistance_chance": self.model.gain_resistance_chance,
            "initial_outbreak_size": self.model.initial_outbreak_size,
            "infected": sum(1 for a in self.model.grid.get_all_cell_contents() if a.state is State.INFECTED),
            "susceptible": sum(1 for a in self.model.grid.get_all_cell_contents() if a.state is State.SUSCEPTIBLE ),
            "resistant": sum(1 for a in self.model.grid.get_all_cell_contents() if a.state is State.RESISTANT),
            "r_to_s_ratio": self.model.resistant_susceptible_ratio(),
        }
    
    # Function to handle user queries 
    def handle_query(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})
        response = self.llm_fn(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response
    
    def get_conversation(self):
        return self.history[1:]
