from yalm._resources import ResourceLoader as _ResourceLoader
from yalm.template.template import Node as _Node
import re as _re
from typing import Union as _Union
from yalm.template import normalizer as _normalizer, template as _template
from yalm.words import split_and_normalize as _split_and_normalize, \
    is_subset_of as _is_subset_of

class SpdxLicense:
  def __init__(self, identifier: str, name: str, priority: float, resources: _ResourceLoader) -> None:
    self.id = identifier
    self.name = name
    self.priority = priority
    self._resources = resources

  @property
  def template(self) -> _Node:
    return self._resources.get_template(self.id)

  @property
  def regex(self) -> _re.Pattern:
    return self._resources.get_regex(self.id)

  @property
  def words(self) -> list[str]:
    return self._resources.get_words(self.id)

  @property
  def positive_samples(self) -> list[str]:
    return self._resources.get_positive_samples(self.id)

  def _test_words(self, words: list[str], words_sorted: bool=False) -> _Union[float, bool]:
    return _is_subset_of(self.words, words, x_sorted=True, y_sorted=words_sorted)

  def _test_regex(self, text: str) -> bool:
    return self.regex.fullmatch(text) is not None

class LicenseMatch:
  def __init__(self, text, template):
    self.text = text
    self.template = template

_resources = _ResourceLoader()
_normalizer = _normalizer.TextNormalizer(_resources.equivalent_words)
spdx_licenses: list[SpdxLicense] = [SpdxLicense(item['id'], item['name'], item['priority'], _resources) for item in _resources.index]

def _normalize_text(text: str) -> str:
  return _normalizer(_template.TextNode(text)).text

def detect_license(text: str) -> LicenseMatch:
  words = _split_and_normalize(text, _resources.equivalent_words, sort=True)
  normalized_text = _normalize_text(text)
  for license in spdx_licenses:
    if license._test_words(words, words_sorted=True) and license._test_regex(normalized_text):
      return LicenseMatch(text, license)
  return None
