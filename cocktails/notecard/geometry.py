# ======================================================================================================================
#      File:  /notecard/geometry.py
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
"""Classes that help represent geometric primitives."""

# ======================================================================================================================
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass



# ======================================================================================================================
# Point Class
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Point:
    """A point class that offers an X and Y coordinate as integers."""
    x: int
    y: int

    def copy(self) -> 'Point':
        return Point(self.x, self.y)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other) -> None:
        self.x += other.x
        self.y += other.y

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __isub__(self, other: 'Point') -> None:
        self.x -= other.x
        self.y -= other.y




# ======================================================================================================================
# Rectangle Class
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Rectangle:
    top_left: Point
    width: int
    height: int

    @property
    def bottom_right(self) -> Point:
        return Point(self.top_left.x + self.width, self.top_left.y + self.height)

    @property
    def left(self) -> int:
        return self.top_left.x

    @property
    def right(self) -> int:
        return self.bottom_right.x

    @property
    def top(self) -> int:
        return self.top_left.y

    @property
    def bottom(self) -> int:
        return self.bottom_right.y




# End of File
