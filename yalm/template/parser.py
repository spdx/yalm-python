from . import template
import xml.dom.minidom as xml


class _XmlTransformer:
  """
  Transforms a template in a license XML into a json format.
  Based on spdx/LicenseListPublisher's code.
  See: https://github.com/spdx/LicenseListPublisher/blob/master/src/org/spdx/licensexml/LicenseXmlHelper.java
  """
  HSPACE_NODE = template.TextNode(' ')
  VSPACE_NODE = template.TextNode('\n')

  def __init__(self):
    self._transformers = {
        'list': self._transform_list_node,
        'alt': self._transform_alt_node,
        'optional': self._transform_optional_node,
        'br': self._transform_break_node,
        'p': self._transform_paragraph_node,
        'titleText': self._transform_optional_node,
        'copyrightText': self._transform_copyright_node,
        'bullet': self._transform_bullet_node,
        'item': self._transform_unprocessed,
        'text': self._transform_unprocessed,
        'standardLicenseHeader': self._transform_unprocessed,
    }

  def _transform_node(self, node: xml.Element) -> template.Node:
    if node.nodeType == xml.Node.TEXT_NODE:
      return self._transform_text_node(node)
    elif node.nodeType == xml.Node.ELEMENT_NODE:
      if node.tagName not in self._transformers:
        raise NotImplementedError("Unsupported node type")
      spacing = node.getAttribute('spacing') if node.hasAttribute('spacing') else 'default'
      result = []
      if spacing in ('default', 'before', 'both'):
        result.append(self.HSPACE_NODE)
      result.append(self._transformers[node.tagName](node))
      if spacing in ('after', 'both'):
        result.append(self.HSPACE_NODE)
      return template.SequentialNode(*result)
    else:
      raise NotImplementedError("Unsupported node type")

  def _transform_text_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.TEXT_NODE
    return template.TextNode(node.nodeValue)

  def _transform_list_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    results = []
    for child in node.childNodes:
      if child.nodeType == xml.Node.TEXT_NODE:
        results.append(self._transform_text_node(child))
      elif child.nodeType != xml.Node.ELEMENT_NODE:
        raise NotImplementedError(f"Unsupported node type")
      elif child.tagName == 'item':
        results.append(self.VSPACE_NODE)
        results.append(self._transform_unprocessed(child))
      elif child.tagName == 'list':
        results.append(self._transform_list_node(child))
      else:
        raise NotImplementedError("Unsupported node type")
    return template.SequentialNode(*results)

  def _transform_alt_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    original = self._transform_unprocessed(node)
    name = node.getAttribute('name')
    match = node.getAttribute('match')
    return template.VarNode(name, original, match)

  def _transform_optional_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    contents = self._transform_unprocessed(node)
    return template.OptionaltNode(contents)

  def _transform_break_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    assert not node.childNodes
    return self.VSPACE_NODE

  def _transform_paragraph_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    result = []
    result.append(self.VSPACE_NODE)
    for child in node.childNodes:
      result.append(self._transform_node(child))
    result.append(self.VSPACE_NODE)
    return template.SequentialNode(*result)

  def _transform_copyright_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    original = self._transform_unprocessed(node)
    name = 'copyright'
    match = '.{0,5000}'
    return template.VarNode(name, original, match)

  def _transform_bullet_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    original = self._transform_unprocessed(node)
    name = 'bullet'
    match = '.{0,20}'
    return template.VarNode(name, original, match)

  def _transform_unprocessed(self, node: xml.Element) -> template.Node:
    if node.nodeType == xml.Node.TEXT_NODE:
      return self._transform_text_node(node)
    elif node.nodeType == xml.Node.ELEMENT_NODE:
      return template.SequentialNode(*[self._transform_node(child) for child in node.childNodes])
    else:
      raise NotImplementedError("Unsupported node type")


def parse_xml(text: xml.Element) -> template.Node:
  """
  Parses a dom element in the spdx-license-XML format and returns a Node.
  """
  transformer = _XmlTransformer()
  tree = transformer._transform_node(text)
  tree = tree.simplify()
  return tree
