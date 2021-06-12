import re
from abc import ABC


class Node(ABC):
  def __init__(self, tag: str):
    self._tag = tag

  def _to_dict(self):
    return {
        'type': self._tag,
    }

  def _is_empty(self):
    return False

  def _normalize(self):
    pass

  @staticmethod
  def normalize(nodes: list[Node]) -> list[Node]:
    """
    Normalize the nodes to remove redundancy.
    First, we remove nodes that are empty.
    Then, consecutive text nodes are merged.
    """
    # Remove empty nodes
    nodes = list(filter(lambda node: not node._is_empty(), nodes))
    # Merge nodes
    nodes_merged = []
    for node in nodes:
      if nodes_merged and isinstance(node, TextNode) and isinstance(nodes_merged[-1], TextNode):
        nodes_merged[-1] = TextNode(nodes_merged[-1].text + node.text)
      else:
        nodes_merged.append(node)
    # Normalize
    for node in nodes_merged:
      node._normalize()
    return nodes_merged


  @staticmethod
  def to_dict(nodes: list[Node]) -> list:
    return [node._to_dict() for node in nodes]


class TextNode(Node):
  _regex_hspace = re.compile(r'[^\S\n\v\f\r\u2028\u2029]+')
  _regex_vspace = re.compile(r'\s*[\n\v\f\r\u2028\u2029]\s*')

  def __init__(self, text: str):
    super().__init__('text')
    self.text = text

  def _to_dict(self):
    return {
        **super()._to_dict(),
        'content': self.text,
    }

  def _is_empty(self):
    return not self.text

  def _normalize(self):
    self.text = self._regex_vspace.sub('\n', self.text)
    self.text = self._regex_hspace.sub(' ', self.text)
  
  def __str__(self):
    return re.escape(self.text)
  
  def __repr__(self):
    return f"TextNode({self.text})"


class OptionaltNode(Node):
  def __init__(self, contents: list[Node]):
    super().__init__('optional')
    self.contents = contents

  def _to_dict(self):
    return {
        **super()._to_dict(),
        'content': Node.to_dict(self.contents),
    }

  def _is_empty(self):
    return all(node._is_empty() for node in self.contents)

  def _normalize(self):
    self.contents = Node.normalize(self.contents)

  def __str__(self):
    return ''.join(map(str, self.contents))

  def __repr__(self):
    return f"OptionalNode([{', '.join(map(repr, self.contents))}])"


class VarNode(Node):
  def __init__(self, name: str, original: list[Node], pattern: str):
    super().__init__('var')
    self.name = name
    self.original = original
    self.pattern = pattern

  def _to_dict(self):
    return {
        **super()._to_dict(),
        'name': self.name,
        'content': Node.to_dict(self.original),
        'pattern': self.pattern,
    }

  def _normalize(self):
    self.original = Node.normalize(self.original)

  def __str__(self):
    return self.pattern

  def __repr__(self):
    return f"VarNode({self.name}, [{', '.join(map(repr, self.original))}], '{self.pattern}')"


def parse_json(nodes: list) -> list[Node]:
  """
  Deserialize nodes in json format.
  """
  results = []
  for node in nodes:
    assert 'type' in node
    if node['type'] == 'text':
      results.append(TextNode(node['content']))
    elif node['type'] == 'optional':
      content = parse_json(node['content'])
      results.append(OptionaltNode(content))
    elif node['type'] == 'var':
      name = node['name']
      content = parse_json(node['content'])
      pattern = node['pattern']
      results.append(VarNode(name, content, pattern))
    else:
      raise NotImplementedError('Unsupported node type')
  return results
