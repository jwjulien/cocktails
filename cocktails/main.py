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
# Validate Command
# ----------------------------------------------------------------------------------------------------------------------
@cli.command()
@click.argument('path', type=click.Path(exists=True))
def validate(path):
    """Validate the YAML schema for the provided recipe PATH and report any issues with content.

    If PATH is a single file, only that file will be validated.  If path is a directory, all .yaml files in that
    directory will be validated as Recipes.
    """
    if os.path.isfile(path):
        filenames = [path]
    else:
        filenames = glob.glob(os.path.join(path, '*.yaml'))

    for filename in filenames:
        print(f'Processing {filename}...')
        counts = {
            'error': 0,
            'warning': 0
        }

        def error(msg):
            print(f'[red][bold]ERROR:[/bold] {msg}[/]')
            counts['error'] += 1
        def warning(msg):
            print(f'[yellow][bold]WARNING:[/bold] {msg}[/]')
            counts['warning'] += 1

        try:
            with open(filename, 'r') as handle:
                yaml = safe_load(handle)
        except:
            error('The following error occurred while loading the YAML file:')
            raise

        try:
            recipe = Recipe.from_dict(yaml)
        except:
            error('The following error occurred while attempting to parse the recipe:')
            raise

        if not recipe.title:
            error('Title is a required attribute.')
        else:
            if not isinstance(recipe.title, str):
                error('Title should be a plain text string.')
            else:
                if len(recipe.title) < 4:
                    warning('Title is a little short.')
                elif len(recipe.title) > 30:
                    warning('Title is a little long.')

        if not recipe.version:
            error('A version number is required.  When in doubt, start at 1.')
        else:
            try:
                value = int(recipe.version)
            except TypeError:
                error('Version number should be an integer')
            else:
                if value < 1:
                    error('The version number should be a non-zero, positive integer')

        if not recipe.ingredients:
            error('Ingredients is a required attribute')
        else:
            if not isinstance(recipe.ingredients, list):
                error('Ingredients should be a list.')
            else:
                for ingredient in recipe.ingredients:
                    if not ingredient.ingredient:
                        error('One or more ingredients are missing an "ingredient" attribute.')
                    else:
                        if ingredient.quantity:
                            try:
                                value = float(ingredient.quantity)
                            except TypeError:
                                error(f'Ingredient {ingredient.ingredient} quantity is not a valid float.')
                            else:
                                if value <= 0:
                                    error('Ingredient quantity must be greater than zero.')

                        if ingredient.notes:
                            if not isinstance(ingredient.notes, str):
                                error(f'Ingredient {ingredient.ingredient} notes should be a string.')

                        if ingredient.suggested:
                            if not isinstance(ingredient.suggested, str):
                                error(f'Ingredient {ingredient.ingredient} suggested should be a string.')

                        if ingredient.examples:
                            if not isinstance(ingredient.examples, list):
                                error(f'Ingredient {ingredient.ingredient} examples should be a list.')
                            else:
                                for example in ingredient.examples:
                                    if not isinstance(example, str):
                                        error(f'Example ingredient {example} is not a string.')

        if not recipe.instructions:
            error('Instructions are a required attribute')
        else:
            if not isinstance(recipe.instructions, list):
                error(f'Recipe instructions must be a list.')
            else:
                for idx, instruction in enumerate(recipe.instructions):
                    if not isinstance(instruction, str):
                        error(f'Instruction #{idx + 1} "{instruction}" is not a string.')

        if recipe.description:
            if not isinstance(recipe.description, str):
                error('Description must be a string.')
            else:
                if len(recipe.description) < 40:
                    warning('Description is short.')

        if recipe.yield_:
            try:
                value = int(recipe.yield_)
            except TypeError:
                error('Failed to parse yield as an integer.')
            else:
                if value < 1:
                    error('Yield should be a positive, non-zero integer.')

        if recipe.author:
            if not isinstance(recipe.author, str):
                error('Author must be a string.')
            else:
                if len(recipe.author) < 8:
                    warning('Author is short.')
                elif len(recipe.author) > 100:
                    warning('Author is long.')

        if recipe.source:
            if not isinstance(recipe.source, str):
                error('Source must be a string.')
            else:
                if len(recipe.source) < 10:
                    warning('Source is short.')
                elif len(recipe.source) > 120:
                    warning('Source is long.')

        if recipe.notes:
            if not isinstance(recipe.notes, str):
                error('Notes must be a string.')
            else:
                if len(recipe.notes) < 10:
                    warning('Notes is short.')

        if sum(counts.values()) == 0:
            print('[green]No errors or warnings found.[/]')
        if counts['warning']:
            print(f"A total of [yellow bold]{counts['warning']} warnings[/] were found.")
        if counts['error']:
            print(f"A total of [red bold]{counts['error']} errors[/] were found.")
        print()




# ======================================================================================================================
# Show Command
# ----------------------------------------------------------------------------------------------------------------------
@cli.command()
@click.argument('recipe', type=click.File())
def show(recipe):
    """Show the specified recipe in the terminal."""
    recipe = Recipe.from_dict(safe_load(recipe))




# ======================================================================================================================
# External Commands
# ----------------------------------------------------------------------------------------------------------------------
cli.add_command(notecard)




# End of File
