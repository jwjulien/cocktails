# ======================================================================================================================
#      File:  /cocktails/search.py
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
"""Search command implementation."""

# ======================================================================================================================
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import dataclasses
import glob
import os.path
import sys
from typing import Iterator, List

import click
from rich import print

from cocktails.model import load_recipe, Ingredient, Recipe




# ======================================================================================================================
# Classes
# ----------------------------------------------------------------------------------------------------------------------
class RecipeScore:

    def __init__(self, recipe: Recipe, possibilities: List[str]):
        self.recipe: Recipe = recipe
        self.missing: List[Ingredient] = []
        for ingredient in recipe.ingredients:
            for test in possibilities:
                if test.lower().strip() == ingredient.ingredient.lower().strip():
                    break
            else:
                self.missing.append(ingredient)

    @property
    def score(self) -> int:
        return len(self.recipe.ingredients) - len(self.missing)




# ======================================================================================================================
# Search Command
# ----------------------------------------------------------------------------------------------------------------------
@click.command()
@click.argument('recipes', type=click.Path(exists=True, file_okay=False))
@click.argument('ingredients', nargs=-1)
@click.option('-a', '--all', 'all_ingredients', is_flag=True, help='recipe MUST contain all listed ingredients')
@click.option('-m', '--missing', default=0, help='how many ingredients can be missing')
@click.option('-s', '--stdin', is_flag=True, help='take ingredient list input from stdin')
def search(recipes, ingredients, all_ingredients, missing, stdin):
    """Search for recipes that contain specific ingredients."""
    # Start by loading all available recipes from the provided recipe directory.
    recipes = [load_recipe(filename) for filename in glob.glob(os.path.join(recipes, '*.yaml'))]

    # If the stdin argument is specified, then load the list from stdin.
    if stdin:
        ingredients = sys.stdin.read().split('\n')

    if all_ingredients:
        for contains in ingredients:
            filtered = []
            for recipe in recipes:
                for ingredient in recipe.ingredients:
                    if contains.lower() in ingredient.ingredient.lower():
                        filtered.append(recipe)
                        break
            recipes = filtered

        print(f"Found {len(recipes)} recipes that contain {' AND '.join(contains)}")
        for recipe in recipes:
            print(f'- [cyan]{recipe.title}[/]')

    else:
        # Create a list of RecipeScore objects to help with ranking.
        scores = [RecipeScore(recipe, ingredients) for recipe in recipes]

        # Remove recipes that have more missing items than the provided threshold.
        scores = [score for score in scores if len(score.missing) <= missing]

        # Sort what's left by the number of matches.
        scores.sort(key=lambda score: (score.score, score.recipe.title))

        # Print the results.
        for score in scores:
            if score.missing:
                missing = f'[yellow]Missing [bold]{len(score.missing)}[/bold] ingredients[/yellow]'
                missing += f" [gray]\[{', '.join(ingredient.ingredient for ingredient in score.missing)}][/gray]"
            else:
                missing = '[green]No missing ingredients[/green]'
            print(f'{score.recipe.title}: {missing}')




# End of File
