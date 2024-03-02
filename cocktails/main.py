# ======================================================================================================================
#      File:  /cocktails/main.py
#   Project:  Cocktail Recipes
#    Author:  Jared Julien <jaredjulien@exsystems.net>
# Copyright:  (c) 2024 Jared Julien, eX Systems
# ---------------------------------------------------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------------------------------------------------------------------------------------------------------------------
"""Packing list generator."""

# ======================================================================================================================
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import logging

import click
from rich import print
from yaml import safe_load




# ======================================================================================================================
# Main Function
# ----------------------------------------------------------------------------------------------------------------------
@click.command
@click.argument('recipes', nargs=-1, type=click.File())
@click.option('-v', '--verbose', count=True, help='increase verbosity of output')
def main(recipes, verbose):
    # Setup logging output.
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(2, verbose)]
    logging.basicConfig(level=level)

    ingredients = {}
    for yaml in recipes:
        recipe = safe_load(yaml)

        for ingredient in recipe['ingredients']:
            name = ingredient['ingredient']
            if name not in ingredients:
                ingredients[name] = []
            ingredients[name].append(recipe['title'])

    for ingredient in sorted(ingredients.keys()):
        recipes = ingredients[ingredient]
        print(f"- [bold green]{ingredient.title()}[/]: [i]{', '.join(recipes)}")





# End of File