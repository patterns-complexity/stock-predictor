# Imports
from os import getenv
from json import load

strings = {}

with open(f"strings/{getenv('LANGUAGE')}.json", "r") as f:
  strings = load(f)
