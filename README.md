# Infectious Virus - SIR Model #

This project explores how a virus spreads on a network.
An example of such a virus is one that can spread through emails.

I undertook this project as a way to understand:
1. How infection virus spread across a network
2. How the mechanics of infectious diseaes can be modeled
3. How to model such behavior following the SIR model, a common model used in epidemiology

Note that this model does not explicitly look at infectious disease spread although analogous parallels may be drawn between the two (patterns, amiright?)

## Why the SIR Model? ##

The SIR model is a compartmental model with 3 basic compartments:
1. S - the number of susceptible agents.
    When a susceptible agent and infectious agent have "infectious content," the susceptible agent contracts the disease and transitions to the infectious compartment. 
2. I - the number of infectious agents.
    These are agents who have been infected and are capable of infecting susceptible agents.
3. R - the number of removed/recovered/resistant (immune, dead, etc.) agents.
    These are agents who have either been infected and recovered from the disease and entered into the removed compartment.

## References ##

[This](https://mesa.readthedocs.io/stable/examples/basic/virus_on_network.html) tutorial was really helpful for code development and guidance, although the project I built here expands on what this tutorial encompasses. I had other ideas I wanted to explore but this is a great place to start for those who may want to expand their knowledge in this realm.

[This](http://ccl.northwestern.edu/netlogo/models/VirusonaNetwork) webpage contained loads of info that helped me grow my contextual understanding of this model, understanding the variables in greater depth, and learning to appreciate the probablities that go into this sort of modeling.

Read [this](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology) to learn more about SIR modeling.
