# Own imports
from .Translations import strings

def t(string: str, namespace: str) -> str:
  """
  Parameters:
    `string` (`str`): The string to translate

    `namespace` (`str`): The namespace to translate the string in

  Returns the translated string
  """
  return strings[namespace][string]

