Cocktails
========================================================================================================================
After years of struggling to come up with the best forum for aggregating various drink recipes I have landed on this tool, unoriginally and simply named `cocktails`.  This Python based tool is used to help create, validate, render and search Cocktail (and their ingredients) recipes, stored along side this tool as .yaml files.

My intent here is to capture the recipes needed to make various mixed drinks and cocktails that I enjoy, along with any notes that I have about the ingredients or the preparation.  I originally had no intentions of building such a tool to maintain these recipes but alas, after many years of tinkering and a desire for some scripts a tool was born.  It quickly took on a similar look and format to many other tools I created at the time so it just felt natural to run with it.

A schema has been developed and is tied to the `ingredients` and `recipes` folders with VS Code workspace settings.  The `recipes` folder contains the various drink recipes while the `ingredients` folder contains recipes for some of the ingredients that need to be prepared for various drink recipes.

> **_DISCLAIMER:_**: The recipes presented here are (mostly) alcoholic.  The author assumes no responsibility for how you use this information.  Please drink responsibly.



Anti-Patterns
------------------------------------------------------------------------------------------------------------------------
This repository does not contain "basic" drinks like "rum and coke" or "whisky neat".  If you can fully comprehend a recipe from the title alone, it serves no place here.




How to use `Cocktails`
------------------------------------------------------------------------------------------------------------------------
1. Start by installing [Python 10+](https://www.python.org/downloads/) and [poetry](https://python-poetry.org/) if you don't already have them.

> **Side bar**: If you are a Python developer and haven't yet heard of Poetry, you need to check it out.  By and large THE best Python dependency manager, in my opinion, and it just keeps getting better.

2. `git clone github.com/jwjulien/cocktails` to your get a copy of the source on your PC.
3. Run `poetry install` to install required dependencies.
4. Run `poetry shell` to spawn a shell session with the new virtual environment.
5. Run `cocktails --help` to see what else it can do.




Reporting Bugs
------------------------------------------------------------------------------------------------------------------------
Officially this project is using [my version of the B bug tracker](https://github.com/jwjulien/b) to report and track bugs.  This means that the bugs are just YAML format text files in the .bugs directory, `B` just helps to manage them, so feel free to browse them.

Admittedly, this is not for everyone as it requires pulling, editing, committing, and pushing to report each and every bug or feature request.  Feel free to submit issues on Github and pull requests would certainly be appreciated.




Future
------------------------------------------------------------------------------------------------------------------------
Perhaps one day this repository might: (this is a shrinking list)

- Certainly contain more drink recipes.
- Filter by glass: "list all shots"
- Filter by preparation: "blended drinks"
- Grep with ingredients: "drinks with tequila"
- etc.