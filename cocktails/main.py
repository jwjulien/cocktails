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
import dataclasses
import glob
from importlib import metadata
import logging
import os.path
import sys

import click
from rich import print

from cocktails.notecard.generate import notecard
from cocktails.model import load_recipe
from cocktails.search import search
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
@click.argument('recipes', nargs=-1, type=click.Path(exists=True, dir_okay=False))
@click.option('-m', '--minimal', is_flag=True, help='limit output to one ingredient per line (great for piping!)')
def ingredients(recipes, minimal):
    """Aggregate, dedupe, and list all of the ingredients needed to make the provided cocktail RECIPES."""
    ingredients = {}
    if not minimal:
        print('Aggregating a list of ingredients for the following drinks:')
    for recipe in recipes:
        recipe = load_recipe(recipe)
        if not minimal:
            print(f"- [green]{recipe.title}[/]")

        for ingredient in recipe.ingredients:
            name = ingredient.ingredient
            if name not in ingredients:
                ingredients[name] = []
            ingredients[name].append(recipe.title)

    if not minimal:
        print()
        print('The following ingredients are needed to be able to make the drinks listed above:')
    for ingredient in sorted(ingredients.keys()):
        recipes = ingredients[ingredient]
        if minimal:
            print(ingredient)
        else:
            print(f"- [bold yellow]{ingredient.title()}[/]: \[[i cyan]{', '.join(recipes)}[/]]")




# ======================================================================================================================
# External Commands
# ----------------------------------------------------------------------------------------------------------------------
cli.add_command(notecard)
cli.add_command(validate)
cli.add_command(show)
cli.add_command(search)




# End of File
