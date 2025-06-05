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
            model, 
            llm_fn=None
    ):
        self.model = model
        self.llm_fn = llm_fn
        self.history = [
             {
                "role": "system", 
                "content": "You are a simulation assistant that knows how to interpret model state."
            }
        ]
 
    # Function to retrieve model information
    def get_model_snapshot(self):
        infected = sum(1 for a in self.model.grid.get_all_cell_contents()
                       if a.state is State.INFECTED)
        susceptible = sum(1 for a in self.model.grid.get_all_cell_contents() 
                        if a.state is State.SUSCEPTIBLE)
        resistant = sum(1 for a in self.model.grid.get_all_cell_contents() 
                        if a.state is State.RESISTANT)
        ratio = self.model.resistant_susceptible_ratio()

        return (
            f"The model has {self.model.num_nodes} agents. "
            f"Currently, there are {infected} infected, {susceptible} susceptible, " 
            f"and {resistant} resistant agents. "
            f"The infection rate is {self.model.virus_spread_chance}, "
            f"and the recovery chance is {self.model.recovery_chance}. "
            f"The resistant-to-susceptible ratio is {'∞' if ratio == math.inf else round(ratio, 2)}. "
        )

    # Function to handle user queries 
    def handle_query(self, query: str) -> str:
        model_snapshot = self.get_model_snapshot()
        prompt = (
            "You are an AI simulation control agent observing an agent-based SIR disease model. "
            "Answer the user's questions based on the current state of the simulation. "
            "Here is the model status:\n"
            f"{model_snapshot}\n\n"
            f"User Question: {query}\n"
            "Answer in clear, concise language. If the user asks something not directly answerable, explain why."
        )
        try:
            return self.llm_fn(prompt)
        except Exception as e:
            return f"Error querying LLM: {e}"
    
    def get_conversation(self):
        return self.history[1:]
