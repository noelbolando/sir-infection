# Infectious Virus - SIR Model with LLM Compatability #
This project explores how a virus spreads on a network.

Originally, I undertook this project as a way to understand:
1. How a virus, or infection, spreads across a network
2. How the mechanics of infectious diseaes can be modeled
3. How to model such behavior following the SIR model, a common model used in epidemiology

Note that this model does not explicitly look at any specific infectious disease spread although analogous parallels may be drawn between the two (patterns, amiright?)

NEW: This model now contains an LLM "Control Agent" for querying the model, allowing users to "talk to the simulation."

## Project Details ##
There are four files in this repo:
1. 'agents.py': this file defines the properties of agents. In the case of this project, this defines SUSCEPTIBLE, INFECTED, and RESISTANT agents. Agents have properties related to how the virus spreads, the chance of recovery, and the chance to gain resistance to the virus.
2. 'app.py': using Solara, this file defines an interactive visualization tool so that users can toggle different agent properties to see how quickly infection spreads and if/how recovery occurs accross the population. It also enables users to interact with a control agent to query the model for insights.
3. 'control_agent.py': this file definse the ControlAgent class, allowing us to pass LLM interactive logic within our simulation. 
4. 'model.py': this file defines the model itself and sets initial values for the properties of agents. SUSCEPTIBLE agents are created in this file, infection spreads to some of these agents, and the ratio of SUSCEPTIBLE to RESISTANT agents is determined.

## How to Use ##
This is pretty simple for those new to Python:
1. Clone the project directory.
2. Make sure all your packages are installed. Especially:
```` $ pip install enum ````
```` $ pip install mesa ````
```` $ pip install networkx ````
```` $ pip install solara ````
3. To run the app, key in the following command to your terminal:
```` $ solara run app.py````
and have fun playing with the webpage tool.
ENJOY! =D

## The Nerd Corner ##
Honestly, this was a really fun model to work on. I ran into a lot of issues debugging and had to delve into the mechanics of ABS modeling more than I thought but all the tangles just resulted in a deeper appreciation for this model. I hope you enjoy the tool as much as I enjoyed developing it.

During this project, I learned more about SIR and some of the theory behind this model. Why, SIR you might be wondering? Well...

## Why the SIR Model? ##
The SIR model is a stochastic compartmental model with 3 basic compartments:
1. S - the number of susceptible agents.
    When a susceptible agent and infectious agent have "infectious content," the susceptible agent contracts the disease and transitions to the infectious compartment. 
2. I - the number of infectious agents.
    These are agents who have been infected and are capable of infecting susceptible agents.
3. R - the number of removed/recovered/resistant (immune, dead, etc.) agents.
    These are agents who have either been infected and recovered from the disease and entered into the removed compartment.

SIR models evaluate the behavior between three agent types and their ability to infect, contract, and recover from infections. This isn't to say that this model covers it all, in fact, far from it. This model is a basic introduction to infectious disease models; there are loads of other variations of the SIR model that you can find with a quick google search =D

## References ##
[This](https://mesa.readthedocs.io/stable/examples/basic/virus_on_network.html) tutorial was really helpful for code development and guidance, although the project I built here expands on what this tutorial encompasses.  This is a great place to start for those who may want to expand their knowledge in this realm.

[This](http://ccl.northwestern.edu/netlogo/models/VirusonaNetwork) webpage contained loads of info that helped me grow my contextual understanding of this model, understanding the variables in greater depth, and learning to appreciate the probablities that go into this sort of modeling.

Read [this](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology) to learn more about SIR modeling.
