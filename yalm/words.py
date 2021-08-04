import re as _re

_valid_word = _re.compile(r"\b[a-zA-Z]+'?s?\b")


def get_common_size(x_list: list, y_list: list, x_sorted=False, y_sorted=False) -> int:
  if not x_sorted:
    x_list = sorted(x_list)
  if not y_sorted:
    y_list = sorted(y_list)
  cur, n, match = 0, len(y_list), 0
  for x in x_list:
    while cur < n and y_list[cur] < x:
      cur += 1
    if cur < n and y_list[cur] == x:
      cur += 1
      match += 1
  return match


def get_dice_coefficient(x_list: list, y_list: list, x_sorted=False, y_sorted=False) -> float:
  match = get_common_size(x_list, y_list, x_sorted, y_sorted)
  return 2 * match / (len(x_list) + len(y_list))


def is_subset_of(x_list: list, y_list: list, x_sorted=False, y_sorted=False) -> bool:
  if len(x_list) > len(y_list):
    return False
  if not x_sorted:
    x_list = sorted(x_list)
  if not y_sorted:
    y_list = sorted(y_list)
  cur, n = 0, len(y_list)
  for x in x_list:
    while cur < n and y_list[cur] < x:
      cur += 1
    if cur < n and y_list[cur] == x:
      cur += 1
    else:
      return False
  return True


def _normalize_word(word, equivalent_words):
  word = word.lower()
  for pair in equivalent_words:
    if word == pair['from']:
      return pair['to']
  return word

def split_and_normalize(text, equivalent_words: list=[], sort: bool=False):
  words = _valid_word.findall(text)
  words = [_normalize_word(word, equivalent_words) for word in words]
  if sort:
    words.sort()
  return words
