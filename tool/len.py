from functools import reduce
import unicodedata


def len(text):
  return reduce(
    lambda x, y: x + y,
    map(
      lambda char: char_length(char),
      text
  ))


def take(text, length):
  count = 0
  idx = -1
  for i, char in enumerate(text):
    count += char_length(char)
    if count > length:
      break
    else:
      idx = i
  return text[:idx + 1]


def char_length(char):
  eaw = unicodedata.east_asian_width(char)
  if eaw == 'F':
    return 2
  elif eaw == 'W':
    return 2
  elif eaw == 'A':
    return 2
  else:
    return 1
