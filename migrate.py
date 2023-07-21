import yaml
import json
import os
import sys


source = sys.argv[1]
with open(source, 'r', encoding='utf-8') as handle:
    recipe = json.load(handle)

destination = os.path.splitext(source)[0] + '.yaml'
with open(destination, 'w', encoding='utf-8') as handle:
    yaml.safe_dump(recipe, handle, sort_keys=False)
