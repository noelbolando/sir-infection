"""
This file instantiates a web page using Solara.
This makes it possible to interact with the model and display some cool visualizations.

*** How to Run: ***
1. initialize mistral model with: 
    ollama run mistral
2. initialize solara app with:
    solara run app.py
"""

import logging
import math
from mesa.visualization import Slider, SolaraViz, make_plot_component, make_space_component
import requests
import solara

from model import State, VirusOnNetwork, number_infected
from control_agent import ControlAgent

# Logger function for tracking Ollama response rate
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Function to interact with Ollama LLM interaction logic
def call_ollama(messages: list[dict]) -> str:
    """HTTP call request funtion for interacting with Ollama LLM"""
    
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "mistral", # using mistral model
            "messages": messages,
            "stream": False
        }
    )
    return response.json()["message"]["content"]

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

# Setting up ControlAgent
control_agent = ControlAgent(model1, llm_fn=call_ollama)
user_query = solara.reactive("")
agent_response = solara.reactive("")

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

# Add ControlAgent interface to Solara app
@solara.component
def ControlPanel():
    query = solara.use_reactive("")
    response = solara.use_reactive("")
    loading = solara.use_reactive(False)

    solara.InputText(label="Ask something about the simulation:", value=query)

    if solara.Button("Submit") and query.value.strip():
        loading.set(True)

        def run_llm():
            new_response = control_agent.handle_query(query.value)
            response.set(new_response)
            query.set("")
            loading.set(False)

        import threading
        threading.Thread(target=run_llm).start()

    if loading.value:
        solara.Markdown("Thinking...")
        solara.ProgressLinear(value=None)
    else:
        for message in control_agent.get_conversation():
            role = message["role"].capitalize()
            content = message["content"]
            if role == "User":
                solara.Markdown(f"**You:** {content}")
            elif role == "Assistant":
                solara.Markdown(f"**LLM:** {content}")


# Initializing an instance of the web page
@solara.component
def Page():
    solara.Title("SIR Model with LLM Control Agent")
    with solara.ColumnsResponsive(12, large=[8,4]):
        with solara.Column(style={"padding": "1em"}):
            solara.Markdown("## 🧫 SIR Virus Simulation")
            SolaraViz(
                model1,
                components=[
                    SpacePlot,
                    StatePlot,
                    get_resistant_susceptible_ratio
                ],
                model_params=model_params,
                name="SIR Virus Model"
            )
        with solara.Column(style={"padding": "1em"}):
            solara.Markdown("## 🤖 Control Agent Panel")
            ControlPanel()
