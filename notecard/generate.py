# ======================================================================================================================
#      File:  /notecard/generate.py
#   Project:  Recipes
#    Author:  Jared Julien <jaredjulien@exsystems.net>
# Copyright:  (c) 2023 Jared Julien, eX Systems
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
"""Notecard generator main function."""

# ======================================================================================================================
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import logging
import json
import glob
from importlib import metadata
from argparse import ArgumentParser
from fractions import Fraction
from io import BytesIO

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'true'
import pygame
import yaml
from PIL import Image
import img2pdf

from notecard import colors
from notecard.textbox import TextBox
from notecard.geometry import Point




# ======================================================================================================================
# Helper Functions
# ----------------------------------------------------------------------------------------------------------------------
def draw_title(screen, title: str, font: pygame.font, x: int, y: int) -> int:
    text = font.render(title, True, colors.BLACK)
    screen.blit(text, (x, y))
    return y + text.get_size()[1]


# ----------------------------------------------------------------------------------------------------------------------
def fraction(value: float) -> str:
    integer = int(value)
    decimal = value - integer
    text = ''
    if integer > 0:
        text += f'{integer} '
    if decimal > 0:
        text += str(Fraction(decimal).limit_denominator(32))
    return text




# ======================================================================================================================
# Main Function
# ----------------------------------------------------------------------------------------------------------------------
def main() -> int:
    description = 'Recipe index card generator for cocktail recipes.'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        'recipe',
        nargs='+',
        help='a JSON format cocktail recipe to format into an index card.'
    )
    parser.add_argument(
        '-o',
        '--output',
        nargs='?',
        const=False,
        help='the path to the PDF to be written'
    )
    parser.add_argument(
        '-s',
        '--silent',
        action='store_true',
        default=False,
        help='don\'t show the rendering - best used with -o option to just write the PDF'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='increase verbosity of output'
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=metadata.version('cocktails'),
        help='print version number and exit'
    )
    args = parser.parse_args()

    # Setup logging
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(2, args.verbose)]
    logging.basicConfig(level=level)

    for recipe_arg in args.recipe:
        for recipe_filename in glob.glob(recipe_arg):
            # Load recipe from file.
            with open(recipe_filename, 'r', encoding='utf-8') as handle:
                if recipe_filename.endswith('.json'):
                    recipe = json.load(handle)
                elif recipe_filename.endswith('.yaml'):
                    recipe = yaml.safe_load(handle)
                else:
                    logging.critical('Unsupported recipe format: %s', os.path.splitext(recipe_filename)[1])
                    return 1

            scale = 0.5

            # Load the boarder image and let it dictate the width and height.
            image_path = os.path.join(os.path.dirname(__file__), 'templates', 'drinks_4x6.png')
            frame = pygame.image.load(image_path)
            width, height = frame.get_size()
            width *= scale
            height *= scale

            # Build a window for our card.
            pygame.init()
            pygame.font.init()
            screen = pygame.display.set_mode((width, height))

            # Add the background image/border.
            screen.fill(colors.WHITE)
            border = 100 * scale
            frame = pygame.transform.scale(frame, (width - (border * 2), height - (border * 2)))
            screen.blit(frame, (border, border))

            # Define fonts.
            fonts = os.path.join(os.path.dirname(__file__), 'fonts')
            h1 = pygame.font.Font(os.path.join(fonts, 'Lobster-Regular.ttf'), int(150 * scale))
            body = pygame.font.SysFont(os.path.join(fonts, 'Roboto-Regular.ttf'), int(75 * scale))
            small = pygame.font.SysFont(os.path.join(fonts, 'Roboto-Regular.ttf'), int(50 * scale))

            # Initialize parameters.
            margin = (200 * scale) + border
            spacing = 60 * scale
            y = margin

            # If there's an author, give them credit.
            if 'author' in recipe:
                author = TextBox(width - (margin * 2), font=body)
                author.add(recipe['author'] + "'s", color=colors.GRAY, italic=True)
                y = author.render(screen, Point(margin, y)).y

            # Then a version.
            version = TextBox(width / 4, font=small)
            version.add(f"Version: {recipe['version']}", italic=True, color=colors.GRAY)
            # TODO: This magic 200 offset is not the ideal way to right-align the version number.
            version.render(screen, Point(width - margin - (200 * scale), y))

            # Next, a title.
            title = TextBox(width - (margin * 2), font=h1)
            title.add(recipe['title'], underline=True)
            y = title.render(screen, Point(margin, y)).y
            y += spacing

            # Add the description.
            if 'description' in recipe:
                description = TextBox(width - margin * 2, font=body)
                description.add(recipe['description'])
                y = description.render(screen, Point(margin, y)).y
                y += spacing

            # Add ingredients to the left.
            ingredients = TextBox(width / 2, font=body, line_height=1.2, indent=20)
            for ingredient in recipe['ingredients']:
                text = '• '
                quantity = 1
                if 'quantity' in ingredient:
                    quantity = ingredient['quantity']
                    text += fraction(quantity) + ' '
                if 'unit' in ingredient:
                    text += ingredient['unit']
                    if quantity > 1:
                        text += 's'
                    text += ' '
                ingredients.add(text)
                ingredients.add(ingredient['ingredient'], bold=True)
                if 'suggested' in ingredient:
                    ingredients.add(f" ({ingredient['suggested']})", italic=True)
                if 'examples' in ingredient:
                    examples = ', '.join(ex for ex in ingredient['examples'] if ex != ingredient.get('suggested'))
                    ingredients.add(f' [e.g. {examples}]', italic=True)
                if 'notes' in ingredient:
                    ingredients.add(f", {ingredient['notes']}", italic=True, color=colors.GRAY)
                ingredients.add('\n')
            y1 = ingredients.render(screen, Point(margin, y)).y

            # Add details (preparation, yield, glass, style, etc.) to the right.
            details = TextBox((width / 2) - (margin * 2), font=body, line_height=1.2, indent=20)
            if 'yield' in recipe:
                details.add(f"Yield: {recipe['yield']} ")
                details.add('shot' if recipe.get('glass') == 'shot' else 'drink')
                if recipe['yield'] > 1:
                    details.add('s')
                details.add('\n')
            if 'preparation' in recipe:
                details.add(f"Preparation: {recipe['preparation'].title()}\n")
            if 'served' in recipe:
                details.add(f"Served: {recipe['served'].title()}\n")
            if 'glass' in recipe:
                details.add(f"In a: {recipe['glass'].title()} Glass\n")
            if details:
                y2 = details.render(screen, Point(width / 2 + margin * 2, y)).y
            else:
                y2 = y

            # Move Y down to be below whichever section was larger.
            y = max(y1, y2) + spacing

            # Add instructions.
            instructions = TextBox(width - margin *2, font=body, line_height=1.2, indent=20)
            for idx, instruction in enumerate(recipe['instructions']):
                instructions.add(f'{idx + 1}. {instruction}\n')
            y = instructions.render(screen, Point(margin, y)).y
            y += spacing

            # Add notes section.
            if 'notes' in recipe:
                notes = TextBox(width - margin * 2, font=body)
                notes.add(recipe['notes'], italic=True)
                y = notes.render(screen, Point(margin, y)).y

            # Show source, if provided.
            if 'source' in recipe:
                source = TextBox(width - margin * 2, font=small)
                source.add(f"Source: {recipe['source']}", italic=True, color=colors.GRAY)
                source.render(screen, Point(margin, height - margin))

            # Show the results
            pygame.display.flip()

            # Determine where to write the output PDF - when specified
            if args.output is not None:
                filename = args.output
                if not filename:
                    filename = os.path.splitext(os.path.basename(recipe_filename))[0]
                if not filename.endswith('.pdf'):
                    filename += '.pdf'

                # Write the rendered result to PDF.
                data = pygame.image.tobytes(screen, 'RGB')
                image = Image.frombytes('RGB', (int(width), int(height)), data)
                file = BytesIO()
                image.save(file, 'png')
                file.seek(0)
                notecard_dimensions = (img2pdf.in_to_pt(6), img2pdf.in_to_pt(4))
                layout_fun = img2pdf.get_layout_fun(notecard_dimensions)
                with open(filename, "wb") as handle:
                    handle.write(img2pdf.convert(file, layout_fun=layout_fun))

            # Show until the user requests to exit.
            showing = not args.silent
            while showing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 0
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            return 0
                        elif event.key == pygame.K_n:
                            showing = False






# End of File
