"""
This is a smple menu that our code can use.
"""


from menu import *

tomato = AddOnChoice("tomato", ["tomato, tomate"], 0.5)
lettuce = AddOnChoice("lettuce", ["lettuce, letuce"], 0.0)

onion = AddOnChoice("onion", ["onion"], 1.0)

pepperoni = AddOnChoice("pepperoni", ["pepperoni"], 2.0)
mushroom = AddOnChoice("muchroom", ["mushroom, mushrom"], 1.0)

small = AddOnChoice("small", ["small"], 0)
medium = AddOnChoice("medium", ["medium, regular"], 2)
large = AddOnChoice("large", ["large"], 4)

burger_toppings = AddOnList("burger toppings", 0, 100, [tomato, lettuce, onion], "Which toppings would you like on your burger?")
pizza_toppings = AddOnList("pizza toppings", 0, 100, [pepperoni, mushroom, onion], "Which toppings would you like on your pizza?")
pizza_sizes = AddOnList("pizza sizes", 1, 1, [small, medium, large], "What size pizza would you like?")

burger = MainItem("burger", ["burger", "hamberder"], [burger_toppings], 10.0)
pizza = MainItem("pizza", ["pizza", "pie"], [pizza_toppings, pizza_sizes], 8.0)

intro_message = "Welcome to Cheesy Does It! Here is our menu. What can I get for you?"
closed_message = "Welcome to Cheesy Does It! Here is our menu. We are currently closed but will open soon! Our hours are: [hours]"

menu = Menu("Cheesy Does It", [burger, pizza], intro_message, closed_message, True, 60, 30, True)
