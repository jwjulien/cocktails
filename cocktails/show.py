# ======================================================================================================================
#      File:  /cocktails/show.py
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
"""A command to print a recipe card to the terminal."""

# ======================================================================================================================
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import click
from rich import box, print
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from yaml import safe_load

from cocktails.model import Recipe, Glass
from cocktails.notecard.generate import fraction




# ======================================================================================================================
# Show Command
# ----------------------------------------------------------------------------------------------------------------------
@click.command()
@click.argument('recipe', type=click.File())
def show(recipe):
    """Show the specified RECIPE in the terminal."""
    recipe = Recipe.from_dict(safe_load(recipe))

    top = recipe.description + '\n'

    left = ''
    for ingredient in recipe.ingredients:
        left += '- '
        if ingredient.quantity:
            left += fraction(ingredient.quantity) + ' '
        if ingredient.unit:
            left += ingredient.unit.value.title()
            if ingredient.quantity > 1:
                left += 's'
            left += ' '
        left += f'[bold]{ingredient.ingredient}[/bold][italic]'
        if ingredient.suggested:
            left += f" ({ingredient.suggested})"
        if ingredient.examples:
            examples = ', '.join(ex for ex in ingredient.examples if ex != ingredient.suggested)
            left += f' \[e.g. {examples}]'
        if ingredient.notes:
            left += f"[gray], {ingredient.notes}[/gray]"
        left += '[/]\n'

    center = '\n'.join(f'{idx + 1}. {instruction}' for idx, instruction in enumerate(recipe.instructions))

    right = f'Version: {recipe.version}\n'
    if recipe.yield_:
        unit = 'shot' if recipe.glass == Glass.Shot else 'drink'
        plural = 's' if recipe.yield_ != 1 else ''
        right += f"Yield: {recipe.yield_} {unit}{plural}\n"
    if recipe.preparation:
        right += f"Preparation: {recipe.preparation.value.title()}\n"
    if recipe.served:
        right += f"Served: {recipe.served.value.title()}\n"
    if recipe.glass:
        right += f"In a: {recipe.glass.value.title()}\n"

    columns = Columns([left, center, right], expand=True)

    title = ''
    if recipe.author:
        title = f"[i]{recipe.author}'s[/] "
    title += f'[bold magenta]{recipe.title}[/]'

    if recipe.notes:
        content = Group(top, columns, recipe.notes)
    else:
        content = Group(top, columns)

    panel = Panel(content, box=box.ROUNDED, title=title, subtitle=recipe.source or '', subtitle_align='left')

    print(panel)




# End of File
