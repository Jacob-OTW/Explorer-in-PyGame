# Explorer-in-PyGame
This is my attempt to recreate a game I created in SNAP! awhile ago. (https://snap.berkeley.edu/project?user=jacob-otw&project=Explorer)
Im planing to recreate all aspects in PyGame.

# Docs
-Adding a usable item:
    Add the name of the item to "shop_ui.usable_items" array 
    and create a match case in the "shop_ui.use" function under the inventory section below the "use" statement.

-Making an item part of a shop: Add an entry to the 
planet that's meant to sell it to you or buy it from 
you by adding "buying={'{item_name}': {price: int}}" 
or "selling={'{item_name}': {price: int}}" as an argument.
for this to work, the planet needs to have "Shop" in its status array.
