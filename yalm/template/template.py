import re
from abc import ABC, abstractmethod
from typing import Any


class TemplateParseError(Exception):
  pass


class Node(ABC):
  def __init__(self, tag: str):
    self._tag = tag

  def to_dict(self) -> Any:
    return {
        'type': self._tag,
    }

  def _is_empty(self) -> bool:
    return False

  def simplify(self) -> 'Node':
    return self


class SequentialNode(Node):
  def __init__(self, *nodes: Node) -> None:
    super().__init__('sequential')
    self.nodes = list(nodes)

  def to_dict(self) -> Any:
    return [node.to_dict() for node in self.nodes]

  def _is_empty(self) -> bool:
    return all(node._is_empty() for node in self.nodes)

  def trim_spaces(self, leading=True, trailing=True) -> 'SequentialNode':
    if self._is_empty():
      return self
    if leading and isinstance(self.nodes[0], TextNode):
      self.nodes[0] = self.nodes[0].trim_spaces(leading=True, trailing=False)
    if trailing and isinstance(self.nodes[-1], TextNode):
      self.nodes[0] = self.nodes[0].trim_spaces(leading=False, trailing=True)
    return self

  def simplify(self) -> Node:
    # Normalize
    self.nodes = [node.simplify() for node in self.nodes if not node._is_empty()]
    # Flatten nodes
    nodes_flat = []
    for node in self.nodes:
      if isinstance(node, self.__class__):
        # flatten nested seq
        nodes_flat += node.nodes
      else:
        nodes_flat.append(node)
    # Merge nodes
    nodes_merged = []
    for node in nodes_flat:
      if nodes_merged and isinstance(node, TextNode) and isinstance(nodes_merged[-1], TextNode):
        # concat texts
        nodes_merged[-1] = TextNode(nodes_merged[-1].text + node.text)
      else:
        nodes_merged.append(node)
    self.nodes = nodes_merged
    # If there is only one node, this node can be "unwrapped"
    if len(self.nodes) == 1:
      return self.nodes[0]
    return self

  def __str__(self):
    return ''.join(map(str, self.nodes))

  def __repr__(self):
    return f"SequentialNode({', '.join(map(repr, self.nodes))})"


class TextNode(Node):
  _regex_hspace = re.compile(r'[^\S\n\v\f\r\u2028\u2029]+')
  _regex_vspace = re.compile(r'\s*[\n\v\f\r\u2028\u2029]\s*')

  def __init__(self, text: str):
    super().__init__('text')
    self.text = text

  def to_dict(self):
    return {
        **super().to_dict(),
        'content': self.text,
    }

  def _is_empty(self):
    return self.text == ''

  def trim_spaces(self, leading=True, trailing=True) -> 'TextNode':
    if leading:
      self.text = self.text.lstrip()
    if trailing:
      self.text = self.text.rstrip()
    return self

  def __str__(self):
    return re.escape(self.text)

  def __repr__(self):
    return f"TextNode({repr(self.text)})"


class OptionaltNode(Node):
  def __init__(self, content: Node):
    super().__init__('optional')
    self.content = content

  def to_dict(self):
    return {
        **super().to_dict(),
        'content': self.content.to_dict(),
    }

  def _is_empty(self):
    return self.content._is_empty()

  def simplify(self):
    self.content = self.content.simplify()
    return self

  def __str__(self):
    return f"(?:{self.content})?"

  def __repr__(self):
    return f"OptionalNode({repr(self.content)})"


class VarNode(Node):
  def __init__(self, name: str, original: Node, pattern: str):
    super().__init__('var')
    self.name = name
    self.original = original
    self.pattern = pattern

  def to_dict(self):
    return {
        **super().to_dict(),
        'name': self.name,
        'content': self.original.to_dict(),
        'pattern': self.pattern,
    }

  def simplify(self):
    self.original = self.original.simplify()
    return self

  def __str__(self):
    return f"(?:{self.pattern})"

  def __repr__(self):
    return f"VarNode({repr(self.name)}, {repr(self.original)}, {repr(self.pattern)})"


def parse_json(node: Any) -> Node:
  """
  Deserialize nodes in json format.
  """
  if type(node) == list:
    contents = [parse_json(c) for c in node]
    return SequentialNode(*contents)
  elif node['type'] == 'text':
    return TextNode(node['content'])
  elif node['type'] == 'optional':
    content = parse_json(node['content'])
    return OptionaltNode(content)
  elif node['type'] == 'var':
    name = node['name']
    content = parse_json(node['content'])
    pattern = node['pattern']
    return VarNode(name, content, pattern)
  else:
    raise NotImplementedError('Unsupported node type')
