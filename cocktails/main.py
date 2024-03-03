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
import glob
from importlib import metadata
import logging
import os.path

import click
from rich import print
from yaml import safe_load

from cocktails.notecard.generate import notecard
from cocktails.model import Recipe
from cocktails.show import show
from cocktails.validate import validate




# ======================================================================================================================
# Main Function
# ----------------------------------------------------------------------------------------------------------------------
@click.group()
@click.option('-v', '--verbose', count=True, help='increase verbosity of output')
@click.version_option(metadata.version('cocktails'))
def cli(verbose):
    """The cocktail tool - for managing cocktail recipes and ingredients."""
    # Setup logging output.
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(2, verbose)]
    logging.basicConfig(level=level)




# ======================================================================================================================
# Ingredient List Command
# ----------------------------------------------------------------------------------------------------------------------
@cli.command()
@click.argument('recipes', nargs=-1, type=click.File())
def ingredients(recipes):
    """Aggregate, dedupe, and list all of the ingredients needed to make the provided cocktail RECIPES."""
    ingredients = {}
    print('Aggregating a list of ingredients for the following drinks:')
    for yaml in recipes:
        recipe = safe_load(yaml)
        print(f"- [green]{recipe['title']}[/]")

        for ingredient in recipe['ingredients']:
            name = ingredient['ingredient']
            if name not in ingredients:
                ingredients[name] = []
            ingredients[name].append(recipe['title'])

    print()
    print('The following ingredients are needed to be able to make the drinks listed above:')
    for ingredient in sorted(ingredients.keys()):
        recipes = ingredients[ingredient]
        print(f"- [bold yellow]{ingredient.title()}[/]: \[[i cyan]{', '.join(recipes)}[/]]")




# ======================================================================================================================
# Search Command
# ----------------------------------------------------------------------------------------------------------------------
@cli.command()
@click.option('-c', '--contains', multiple=True, help='specify an ingredient the recipe must contain')
def search(contains):
    """Search for recipes that contain specific ingredients."""
    # Start by loading all available recipes from the recipe directory.
    recipes = []
    for filename in glob.glob(os.path.join('recipes', '*.yaml')):
        with open(filename, 'r') as handle:
            yaml = safe_load(handle)
            recipe = Recipe.from_dict(yaml)
        recipes.append(recipe)

    for contain in contains:
        filtered = []
        for recipe in recipes:
            for ingredient in recipe.ingredients:
                if contain.lower() in ingredient.ingredient.lower():
                    filtered.append(recipe)
                    break
        recipes = filtered

    print(f"Found {len(recipes)} recipes that contain {' AND '.join(contains)}")
    for recipe in recipes:
        print(f'- [cyan]{recipe.title}[/]')




# ======================================================================================================================
# External Commands
# ----------------------------------------------------------------------------------------------------------------------
cli.add_command(notecard)
cli.add_command(validate)
cli.add_command(show)




# End of File
