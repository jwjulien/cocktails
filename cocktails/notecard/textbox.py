# ======================================================================================================================
#      File:  /notecard/textbox.py
#   Project:  Recipes
#    Author:  Jared Julien <jaredjulien@exsystems.net>
# Copyright:  (c) 2023-2024 Jared Julien, eX Systems
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
"""Rendering tool to handle drawing multiline text within pygame."""

# ======================================================================================================================
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from typing import List, Tuple
from dataclasses import dataclass, field

import pygame

from notecard.geometry import Point, Rectangle
from cocktails.notecard import colors




# ======================================================================================================================
# Text Segment Class
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Text:
    text: str
    font: pygame.font
    color: Tuple[int, int, int] = colors.BLACK
    italic: bool = False
    bold: bool = False
    underline: bool = False

    def render(self, screen, cursor: Point, bounds: Rectangle, line_height: float, indent: int) -> Point:
        """Render this chunk of text to the screen at the provided position.

        Arguments:
            screen: The pygame surface into which this text shall be `blit`.
            cursor: The current x/y position of the vursor for flowing text.
            bounds: The bounding box within which this text must fit.

                The Y coordinate isn't really relevant here as `cursor.y` will be used for placement.

                If height is 0, it will be ignored.  Otherwise, text the exceeds `bounds.height` will be truncated.
            line_height: The scale factor for the white space between lines of text.
            indent: An optional indent to use specifically for *wrapping* new lines of text.

        Returns:
            A Point indicating the "cursor" position at the end of this text.
        """
        # Determine the size of a space using the specified font.
        space_width, space_height = self.font.size(' ')

        def newline(offset: int):
            """Wrap the cursor back to the start of a new line."""
            # Break the loop if the cursor will be outside of the available space.
            cursor.x = bounds.left + offset
            cursor.y += space_height * line_height


        lines = self.text.split('\n')
        for line_idx, line in enumerate(lines):
            words = line.split(' ')
            for word_idx, word in enumerate(words):
                # Get the amount of room that this word will need.
                width = self.font.size(word)[0]

                # Carriage return if the line exceeds the available width.
                available_width = bounds.width - (cursor.x - bounds.left)
                if width > available_width:
                    newline(indent)

                # If the text no longer fits at this new line, abort with an exception.
                if bounds.height > 0 and cursor.y + space_height >= bounds.bottom:
                    raise OverflowError

                # Render the text at the calculated position.
                self.font.set_bold(self.bold)
                self.font.set_italic(self.italic)
                self.font.set_underline(self.underline)
                surface = self.font.render(word, True, self.color)
                screen.blit(surface, (cursor.x, cursor.y))
                cursor.x += width

                # Add a space width back in for every space except the end of the line.
                if word_idx + 1 < len(words):
                    surface = self.font.render(' ', False, self.color)
                    screen.blit(surface, (cursor.x, cursor.y))
                    cursor.x += space_width

            # Newline for every line except the end.
            if line_idx + 1 < len(lines):
                newline(0)

        return cursor




# ======================================================================================================================
# Text Box Class
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class TextBox:
    """Provide a bounding box for multiline text to be rendered by pygame.

    Attributes:
        font: pygame font to use to render the text
    """
    width: int
    height: int = 0
    line_height: float = 1.0
    indent: int = 0
    texts: List[Text] = field(default_factory=list)
    font: pygame.font = field(default_factory=lambda: pygame.font.SysFont('Calibri', 12))


    def __bool__(self) -> bool:
        return bool(self.texts)


    def add(self, text: str, **args) -> None:
        """This is a convenience method for add Text's to this TextBox.  Equivalent to:

            box = TextBox()
            font = pygame.font.SysFont('Roboto', 12)
            box.texts.append(Text('text to add', font))

        The above, verbose method would be preferred if you need more features of the RichText rendering that Text
        provides.
        """
        if 'font' not in args:
            args['font'] = self.font
        self.texts.append(Text(text, **args))


    def render(self, screen, origin: Point) -> Point:
        cursor = origin.copy()
        bounds = Rectangle(origin, self.width, self.height)
        try:
            for text in self.texts:
                cursor = text.render(screen, cursor, bounds, self.line_height, self.indent)
        except OverflowError:
            pass

        bottom_right = bounds.bottom_right.copy()
        if self.height == 0:
            bottom_right.y = cursor.y + self.texts[-1].font.size(' ')[1]

        # TODO: This is just for debug - remove this board once implemented.
        # pygame.draw.rect(screen, colors.RED, pygame.Rect(origin.x, origin.y, bottom_right.x - origin.x, bottom_right.y - origin.y), 1)

        return bottom_right






# End of File
