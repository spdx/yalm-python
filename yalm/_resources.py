from importlib import resources
import json
from yalm import resources as data
from yalm.resources import words, template, regex
from yalm.template import template
import regex as re

class KeyedDocument:
  def __init__(self, key: str, document: str):
    self.key = key
    self.document = document

  def __repr__(self) -> str:
    return repr(self.document)

  def __str__(self) -> str:
    return str(self.document)


class ResourceLoader:
  def __init__(self):
    self._meta = None
    self._equivalent_words = None
    self._expected_duplicates = None
    self._index = None
    self._words = {}
    self._template = {}
    self._regex = {}
    self._positive_samples = {}

  def _escape_license_id(self, license: str) -> str:
    return re.sub(r'\W', '_', license)

  @property
  def meta(self):
    if self._meta is None:
      self._meta = json.loads(resources.read_text(data, 'meta.json'))
    return self._meta

  @property
  def equivalent_words(self):
    if self._equivalent_words is None:
      self._equivalent_words = json.loads(resources.read_text(data, 'equivalentwords.json'))
    return self._equivalent_words

  @property
  def expected_duplicates(self):
    if self._expected_duplicates is None:
      self._expected_duplicates = json.loads(resources.read_text(data, 'expected-duplicates.json'))
    return self._expected_duplicates

  @property
  def index(self):
    if self._index is None:
      self._index = json.loads(resources.read_text(data, 'licenses.json'))
    return self._index

  def get_words(self, license) -> list[str]:
    license = self._escape_license_id(license)
    if license not in self._words:
      self._words[license] = json.loads(resources.read_text(words, f"{license}.json"))
    return self._words[license]

  def get_template(self, license) -> template.Node:
    license = self._escape_license_id(license)
    if license not in self._template:
      data = json.loads(resources.read_text(template, f"{license}.json"))
      self._template[license] = template.parse_json(data)
    return self._template[license]

  def get_regex(self, license) -> re.Pattern:
    license = self._escape_license_id(license)
    if license not in self._regex:
      self._regex[license] = re.compile(resources.read_text(regex, license), re.IGNORECASE)
    return self._regex[license]

  def get_positive_sample(self, license, key) -> KeyedDocument:
    # ensure the sample is loaded
    self.get_positive_samples(license)
    license = self._escape_license_id(license)
    return self._positive_samples[license][key]

  def get_positive_samples(self, license) -> list[KeyedDocument]:
    license = self._escape_license_id(license)
    if license not in self._positive_samples:
      path = f"yalm.resources.tests.classfier.positive.{license}"
      results = {}
      for item in resources.contents(path):
        if not item.endswith('.txt'):
          continue
        value = resources.read_text(path, item)
        results[item] = KeyedDocument(item, value)
      self._positive_samples[license] = results
    return list(self._positive_samples[license].values())

  def clear(self) -> None:
    self._meta = None
    self._equivalent_words = None
    self._expected_duplicates = None
    self._index = None
    self._words = {}
    self._template = {}
    self._regex = {}
    self._positive_samples = {}
