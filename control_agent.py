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
    def handle_query(self, query: str) -> str:
        model_state = self.get_model_snapshot()
        prompt = (
            "You are an AI control assistant for an agent-based SIR model of disease spread.\n"
            "Your job is to interpret the model state and answer user questions.\n"
            f"Model State (JSON):\n{json.dumps(model_state, indent=2)}\n"
            f"User Question: {query}\n"
            "Provide a concise and helpful answer."
        )
        try:
            return self.llm_fn(prompt)
        except Exception as e:
            return f"Error querying LLM: {e}"
