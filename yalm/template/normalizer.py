import os
import re
from .template import Node, SequentialNode, TextNode, OptionaltNode, VarNode


class Normalizer:
  def __call__(self, node: Node) -> Node:
    if isinstance(node, SequentialNode):
      return self.normalize_sequential(node)
    if isinstance(node, TextNode):
      return self.normalize_text(node)
    if isinstance(node, OptionaltNode):
      return self.normalize_optional(node)
    if isinstance(node, VarNode):
      return self.normalize_var(node)
    raise NotImplementedError("Unsupported node type")

  def normalize_sequential(self, node: SequentialNode) -> Node:
    node.nodes = [self(node) for node in node.nodes]
    return node

  def normalize_text(self, node: TextNode) -> Node:
    return node

  def normalize_optional(self, node: OptionaltNode) -> Node:
    node.content = self(node.content)
    return node

  def normalize_var(self, node: VarNode) -> Node:
    node.original = self(node.original)
    return node


class SequentialNormalizer(Normalizer):
  def __init__(self, *normalizers: list[Normalizer]):
    self.normalizers = normalizers

  def __call__(self, node: Node) -> Node:
    for normalizer in self.normalizers:
      node = normalizer(node)
    return node


class LowercaseNormalizer(Normalizer):
  """
  Converts the string into lowercase.
  """

  def normalize_text(self, node: TextNode) -> Node:
    node.text = node.text.lower()
    return node


class EquivalentWordsNormalizer(Normalizer):
  """
  Checks each word against the equivalent words
  list to avoid mismatch of equivalent words.
  """

  def __init__(self, equivalentwords) -> None:
    self.equivalentwords = equivalentwords

  def normalize_text(self, node: TextNode) -> Node:
    for rule in self.equivalentwords:
      node.text = node.text.replace(rule['from'], rule['to'])
    return node


class CopyrightSymbolNormalizer(Normalizer):
  """
  Removes the copyright symbol and the possibilities 
  of mismatch due to it.
  """

  def normalize_text(self, node: TextNode) -> Node:
    node.text = node.text.replace("copyright", '')
    node.text = node.text.replace('(c)', '')
    return node


class BulletsNumberingNormalizer(Normalizer):
  """
  The most important and error prone function is the handling
  of the bullets and numbering cases. The case has just 1 error
  prone possibility and requirement that the numbering should
  carry a space after it or else it gets matched with the
  version. (1. ) will match while (1.) will not.
  """

  def normalize_text(self, node: TextNode) -> Node:
    regex_to_substitute = [
        r'([0-9]+\.){2,}',
        r'[0-9]+\.[\D]',
        r'^[a-z]\.',
        r'[a-z]\)',
        r'[0-9]\)',
        r'^[A-Z]\.',
        r'^[mdclxvi]+\.',
    ]
    for x in regex_to_substitute:
      node.text = re.sub(x, '', node.text)
    return node


class PunctuationNormalizer(Normalizer):
  """
  Replaces the common punctuations with ` to avoid errors.
  """
  _pattern_period = re.compile(r'\.(?=[a-z])')
  _pattern_comma = re.compile(r'\,(?=[a-z])')
  _pattern_hyphen = re.compile(r'\-(?=[a-z])')

  def normalize_text(self, node: TextNode) -> Node:
    punctuations = ['/', '\'', '\"', '`']
    node.text = node.text.replace('_', '-')
    node.text = node.text.replace('--', '-')

    for x in punctuations:
      node.text = node.text.replace(x, '`')

    node.text = self._pattern_period.sub('.`', node.text)
    node.text = self._pattern_comma.sub(',`', node.text)
    node.text = self._pattern_hyphen.sub('-`', node.text)
    return node


class LicenseTitleNormalizer(Normalizer):
  def normalize_text(self, node: TextNode) -> Node:
    node.text = node.text.replace('end of terms and conditions', '')
    return node


class WhiteSpaceNormalizer(Normalizer):
  """
  All the Whitespace and the tabs are removed. At the end of
  this function the input file just becomes a single long
  string which is easier to match.
  """
  _optional_space = OptionaltNode(TextNode('`'))

  def normalize_text(self, node: TextNode) -> Node:
    node.text = re.sub(r'\s+', '`', node.text)
    node.text = re.sub(r'\`+', '`', node.text)
    return node

  def normalize_optional(self, node: OptionaltNode) -> Node:
    node.content = node.content.trim()
    node.content = self(node.content)
    return SequentialNode(self._optional_space, node, self._optional_space)


class Trimmer(Normalizer):
  """
  All leading/trailing spaces are removed.
  """

  def __init__(self, char: str = None, l: bool = True, r: bool = True):
    self.char = char
    self.l = l
    self.r = r

  def __call__(self, node: Node) -> Node:
    return node.trim(char=self.char, l=self.l, r=self.r)


class TemplateSimplifier(Normalizer):
  """
  Structure of a template is simplified as much as possible.
  """

  def __call__(self, node: Node) -> Node:
    return node.simplify()


class TextNormalizer(SequentialNormalizer):
  def __init__(self, equivalentwords=[]) -> None:
    super().__init__(
        LowercaseNormalizer(),
        EquivalentWordsNormalizer(equivalentwords),
        CopyrightSymbolNormalizer(),
        BulletsNumberingNormalizer(),
        PunctuationNormalizer(),
        LicenseTitleNormalizer(),
        WhiteSpaceNormalizer(),
        Trimmer(char='`'),
    )


class TemplateNormalizer(SequentialNormalizer):
  def __init__(self, equivalentwords=[]) -> None:
    super().__init__(
        LowercaseNormalizer(),
        EquivalentWordsNormalizer(equivalentwords),
        PunctuationNormalizer(),
        WhiteSpaceNormalizer(),
        Trimmer(char='`'),
        TemplateSimplifier(),
    )
