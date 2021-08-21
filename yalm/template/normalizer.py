import os
import re
from .template import Node, SequentialNode, TextNode, OptionalNode, VarNode
import terregex


class Normalizer:
  def __call__(self, node: Node, *, pred: Node = None, succ: Node = None, parent: Node = None) -> Node:
    if isinstance(node, SequentialNode):
      return self.normalize_sequential(node, pred=pred, succ=succ, parent=parent)
    if isinstance(node, TextNode):
      return self.normalize_text(node, pred=pred, succ=succ, parent=parent)
    if isinstance(node, OptionalNode):
      return self.normalize_optional(node, pred=pred, succ=succ, parent=parent)
    if isinstance(node, VarNode):
      return self.normalize_var(node, pred=pred, succ=succ, parent=parent)
    raise NotImplementedError("Unsupported node type")

  def normalize_sequential(self,
                           node: SequentialNode,
                           *,
                           pred: Node = None,
                           succ: Node = None,
                           parent: Node = None) -> Node:
    preds = [pred] + node.nodes[:-1]
    succs = node.nodes[1:] + [succ]
    node.nodes = [self(n, pred=p, succ=s, parent=node) for p, n, s in zip(preds, node.nodes, succs)]
    return node.simplify()

  def normalize_text(self, node: TextNode, *, pred: Node = None, succ: Node = None, parent: Node = None) -> Node:
    return node

  def normalize_optional(self,
                         node: OptionalNode,
                         *,
                         pred: Node = None,
                         succ: Node = None,
                         parent: Node = None) -> Node:
    node.content = self(node.content, pred=pred, succ=succ, parent=parent)
    return node

  def normalize_var(self, node: VarNode, *, pred: Node = None, succ: Node = None, parent: Node = None) -> Node:
    node.original = self(node.original, pred=pred, succ=succ, parent=parent)
    return node


class SequentialNormalizer(Normalizer):
  def __init__(self, *normalizers: list[Normalizer]):
    self.normalizers = normalizers

  def __call__(self, node: Node, *, pred: Node = None, succ: Node = None, parent: Node = None) -> Node:
    for normalizer in self.normalizers:
      node = normalizer(node, pred=pred, succ=succ, parent=parent)
    return node


class LowercaseNormalizer(Normalizer):
  """
  Converts the string into lowercase.
  """

  def __init__(self):
    self.normalize_regex = terregex.Transformer()

    @self.normalize_regex.add_rule()
    def rule1(literal: terregex.Literal):
      literal.string = literal.string.lower()

  def normalize_text(self, node: TextNode, **_) -> Node:
    node.text = node.text.lower()
    return node

  def normalize_var(self, node: VarNode, **_):
    node.pattern = self.normalize_regex(node.pattern)
    return node


class EquivalentWordsNormalizer(Normalizer):
  """
  Checks each word against the equivalent words
  list to avoid mismatch of equivalent words.
  """

  def __init__(self, equivalentwords) -> None:
    self.equivalentwords = equivalentwords

  def normalize_text(self, node: TextNode, **_) -> Node:
    for rule in self.equivalentwords:
      node.text = node.text.replace(rule['from'], rule['to'])
    return node


class CopyrightSymbolNormalizer(Normalizer):
  """
  Removes the copyright symbol and the possibilities 
  of mismatch due to it.
  """

  def normalize_text(self, node: TextNode, **_) -> Node:
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

  def normalize_text(self, node: TextNode, **_) -> Node:
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

  def normalize_text(self, node: TextNode, **_) -> Node:
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
  def normalize_text(self, node: TextNode, **_) -> Node:
    node.text = node.text.replace('end of terms and conditions', '')
    return node


class WhiteSpaceNormalizer(Normalizer):
  """
  All the Whitespace and the tabs are removed. At the end of
  this function the input file just becomes a single long
  string which is easier to match.
  """
  _optional_space = OptionalNode(TextNode('`'))

  def __init__(self):
    self.normalize_regex = terregex.Transformer()

    @self.normalize_regex.add_rule()
    def rule1(literal: terregex.Literal):
      literal.string = literal.string.replace(' ', '`')

  def normalize_text(self, node: TextNode, *, pred: Node = None, succ: Node = None, **_) -> Node:
    if isinstance(pred, OptionalNode) or isinstance(pred, VarNode):
      node.trim(r=False)
    if isinstance(succ, OptionalNode) or isinstance(succ, VarNode):
      node.trim(l=False)
    node.text = re.sub(r'\s+', '`', node.text)
    node.text = re.sub(r'\`+', '`', node.text)
    return node

  def normalize_optional(self, node: OptionalNode, **_) -> Node:
    node.content = node.content.trim()
    node.content = self(node.content)
    return SequentialNode(self._optional_space, node, self._optional_space)

  def normalize_var(self, node: VarNode, **_):
    node.pattern = self.normalize_regex(node.pattern)
    return SequentialNode(self._optional_space, node, self._optional_space)


class Trimmer(Normalizer):
  """
  All leading/trailing spaces are removed.
  """

  def __init__(self, char: str = None, l: bool = True, r: bool = True):
    self.char = char
    self.l = l
    self.r = r

  def __call__(self, node: Node, **_) -> Node:
    return node.trim(char=self.char, l=self.l, r=self.r)


class TemplateSimplifier(Normalizer):
  """
  Structure of a template is simplified as much as possible.
  """

  def __call__(self, node: Node, **_) -> Node:
    return node.simplify()


class RegexRepeatLimit(Normalizer):
  """
  Limit maximum repetiton number of regexes in var tags
  """

  def __init__(self, max_repeat):
    self.max_repeat = max_repeat
    self.normalize_regex = terregex.Transformer()

    @self.normalize_regex.add_rule()
    def transform_min_repeat(literal: terregex.MinRepeat):
      if literal.max is None or literal.max > self.max_repeat:
        literal.max = self.max_repeat

    @self.normalize_regex.add_rule()
    def transform_max_repeat(literal: terregex.MaxRepeat):
      if literal.max is None or literal.max > self.max_repeat:
        literal.max = self.max_repeat

  def normalize_var(self, node: VarNode, **_):
    node.pattern = self.normalize_regex(node.pattern)
    return node
  

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
        RegexRepeatLimit(500),
        TemplateSimplifier(),
    )


class TemplateNormalizer(SequentialNormalizer):
  def __init__(self, equivalentwords=[]) -> None:
    super().__init__(
        LowercaseNormalizer(),
        EquivalentWordsNormalizer(equivalentwords),
        PunctuationNormalizer(),
        WhiteSpaceNormalizer(),
        Trimmer(char='`'),
        RegexRepeatLimit(500),
        TemplateSimplifier(),
    )
