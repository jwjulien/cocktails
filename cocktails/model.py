# ======================================================================================================================
#      File:  /cocktails/model.py
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
"""A proper in-memory model for a recipe that can be read/written to YAML files.

Follows the same schema as the .json schema located in the schema folder.
"""

# ======================================================================================================================
# Imports
# ----------------------------------------------------------------------------------------------------------------------
import dataclasses
from enum import Enum
from typing import Dict, List




# ======================================================================================================================
# Enumerations
# ----------------------------------------------------------------------------------------------------------------------
class Unit(Enum):
    Barspoon = 'barspoon'
    Cup = 'cup'
    Dash = 'dash'
    Drop = 'drop'
    Gram = 'gram'
    Ounce = 'ounce'
    Rinse = 'rinse'
    Splash = 'splash'
    Spritz = 'spritz'
    Teaspoon = 'teaspoon'
    Tablespoon = 'tablespoon'
    Twist = 'twist'


# ----------------------------------------------------------------------------------------------------------------------
class Preparation(Enum):
    Blended = 'blended'
    Built = 'built'
    Stirred = 'stirred'
    Shaken = 'shaken'


# ----------------------------------------------------------------------------------------------------------------------
class Served(Enum):
    Neat = 'neat'
    OnARock = 'on a rock'
    OnCrushedIce = 'on crushed ice'
    OnTheRocks = 'on the rocks'
    StraightUp = 'straight up'


# ----------------------------------------------------------------------------------------------------------------------
class Glass(Enum):
    Collins = 'collins'
    Coupe = 'coupe'
    Fishbowl = 'fishbowl'
    Highball = 'highball'
    Hurricane = 'hurricane'
    Lowball = 'lowball'
    Martini = 'martini'
    Mug = 'mug'
    Shot = 'shot'
    Tiki = 'tiki'
    Toddy = 'toddy'
    Wine = 'wine'




# ======================================================================================================================
# Ingredient Dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass
class Ingredient:
    ingredient: str
    unit: Unit = 'each'
    quantity: float = 1.0
    notes: str = None
    suggested: str = None
    examples: List[str] = dataclasses.field(default_factory=list)


    @staticmethod
    def from_dict(data: Dict) -> 'Ingredient':
        return Ingredient(
            ingredient=data['ingredient'],
            unit=Unit(data['unit']) if 'unit' in data else None,
            quantity=data.get('quantity'),
            notes=data.get('notes'),
            suggested=data.get('suggested'),
            examples=data.get('examples', []),
        )


    def to_dict(self) -> Dict:
        data = {}
        for attribute in ['ingredient', 'unit', 'quantity', 'notes', 'suggested', 'examples]']:
            value = getattr(self, attribute)
            if value:
                if isinstance(value, Enum):
                    value = value.value()
                data[attribute] = value
        return data




# ======================================================================================================================
# Recipe Dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass
class Recipe:
    title: str
    version: int
    ingredients: List[Ingredient]
    instructions: List[str]
    description: str = ''
    yield_: int = None
    author: str = ''
    source: str = ''
    preparation: Preparation = None
    served: Served = None
    glass: Glass = None
    notes: str = ''


    @staticmethod
    def from_dict(data: Dict) -> 'Recipe':
        """Construct a recipe from the provided python dict object."""
        return Recipe(
            title=data['title'],
            version=data['version'],
            ingredients=[Ingredient.from_dict(ingredient) for ingredient in data['ingredients']],
            instructions=data['instructions'],
            description=data.get('description'),
            source=data.get('source'),
            author=data.get('author'),
            yield_=data.get('yield'),
            preparation=Preparation(data['preparation']) if 'preparation' in data else None,
            served=Served(data['served']) if 'served' in data else None,
            glass=Glass(data['glass']) if 'glass' in data else None,
            notes=data.get('notes'),
        )


    def to_dict(self) -> Dict:
        data = {
            'title': self.title,
            'version': self.version,
            'ingredients': [ingredient.to_dict() for ingredient in self.ingredients],
            'instructions': self.instructions,
        }
        if self.description:
            data['description'] = self.description
        if self.source:
            data['source'] = self.source
        if self.author:
            data['author'] = self.author
        if self.yield_:
            data['yield'] = self.yield_
        if self.preparation:
            data['preparation'] = self.preparation.value()
        if self.served:
            data['served'] = self.served.value()
        if self.glass:
            data['glass'] = self.glass.value()
        if self.notes:
            data['notes'] = self.notes





# End of File
