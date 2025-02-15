"""
This file instantiates a web page using Solara.
This makes it possible to interact with the model and display some cool visualizations.

To initialize the app:
    solara run app.py
"""

import math
from mesa.visualization import Slider, SolaraViz, make_plot_component, make_space_component
import solara

from model import State, VirusOnNetwork, number_infected

# Define how the agents are portrayed.
def agent_portrayal(agent):
    node_color_dict = {
        State.INFECTED: "tab:red",
        State.SUSCEPTIBLE: "tab:green",
        State.RESISTANT: "tab:purple"
    }
    return {"color": node_color_dict[agent.state], "size": 100}

def get_resistant_susceptible_ratio(model):
    """
    Function to retrieve resistant to susceptible ratio.
    This function also displays the ratio amount and number of infected remaining.
    """
    ratio = model.resistant_susceptible_ratio()
    ratio_text = r"$infty$" if ratio is math.inf else f"{ratio:.2f}"
    infected_text = str(number_infected(model))

    return solara.Markdown(
        f"Resistant/Susceptible Ratio: {ratio_text}<br>Infected Remaining: {infected_text}"

    )

# Define how the model parameters will be displayed.
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed"
    },
    "num_nodes": Slider(
        label="Number of Agents",
        value=10,
        min=10,
        max=50,
        step=1
    ),
    "avg_node_degree": Slider(
        label="Avg Node Degree",
        value=3,
        min=3,
        max=8,
        step=1
    ),
    "initial_outbreak_size": Slider(
        label="Initial Outbreak Size",
        value=1,
        min=1,
        max=10,
        step=1
    ),
    "virus_spread_chance": Slider(
        label="Infection Rate",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "virus_check_frequency": Slider(
        label="Virus Check Frequency",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "recovery_chance": Slider(
        label="Chance of Recovery",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "gain_resistance_chance": Slider(
        label="Chance of Gaining Resistance",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
}

# Setup for the model process visualization.
def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_ylabel("Number of Agents")
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

SpacePlot = make_space_component(agent_portrayal)
StatePlot = make_plot_component(
    {"Infected": "tab:red", "Susceptible": "tab:green", "Resistant": "tab:purple"},
    post_process=post_process_lineplot
)

model1 = VirusOnNetwork()

# Setting up the web page
page = SolaraViz(
    model1,
    components=[
        SpacePlot,
        StatePlot,
        get_resistant_susceptible_ratio
    ],
    model_params=model_params,
    name="SIR Virus Model"
)

# Initializing an instance of the web page
page 
