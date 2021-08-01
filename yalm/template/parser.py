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
    self.transformers = {
        'list': self.transform_list_node,
        'alt': self.transform_alt_node,
        'optional': self.transform_optional_node,
        'br': self.transform_break_node,
        'p': self.transform_paragraph_node,
        'titleText': self.transform_optional_node,
        'copyrightText': self.transform_copyright_node,
        'bullet': self.transform_bullet_node,
        'item': self.transform_unprocessed,
        'text': self.transform_unprocessed,
        'standardLicenseHeader': self.transform_unprocessed,
    }

  def transform_node(self, node: xml.Element) -> template.Node:
    if node.nodeType == xml.Node.TEXT_NODE:
      return self.transform_text_node(node)
    elif node.nodeType == xml.Node.ELEMENT_NODE:
      if node.tagName not in self.transformers:
        raise NotImplementedError("Unsupported node type")
      spacing = node.getAttribute('spacing') if node.hasAttribute('spacing') else 'default'
      result = []
      if spacing in ('default', 'before', 'both'):
        result.append(self.HSPACE_NODE)
      result.append(self.transformers[node.tagName](node))
      if spacing in ('after', 'both'):
        result.append(self.HSPACE_NODE)
      return template.SequentialNode(*result)
    else:
      raise NotImplementedError("Unsupported node type")

  def transform_text_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.TEXT_NODE
    return template.TextNode(node.nodeValue)

  def transform_list_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    results = []
    for child in node.childNodes:
      if child.nodeType == xml.Node.TEXT_NODE:
        results.append(self.transform_text_node(child))
      elif child.nodeType != xml.Node.ELEMENT_NODE:
        raise NotImplementedError(f"Unsupported node type")
      elif child.tagName == 'item':
        results.append(self.VSPACE_NODE)
        results.append(self.transform_unprocessed(child))
      elif child.tagName == 'list':
        results.append(self.transform_list_node(child))
      else:
        raise NotImplementedError("Unsupported node type")
    return template.SequentialNode(*results).trim()

  def transform_alt_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    original = self.transform_unprocessed(node)
    name = node.getAttribute('name')
    match = node.getAttribute('match')
    return template.VarNode(name, original, match)

  def transform_optional_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    contents = self.transform_unprocessed(node)
    return template.OptionalNode(contents)

  def transform_break_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    assert not node.childNodes
    return self.VSPACE_NODE

  def transform_paragraph_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    return template.SequentialNode(self.VSPACE_NODE, self.transform_unprocessed(node), self.VSPACE_NODE)

  def transform_copyright_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    original = self.transform_unprocessed(node)
    name = 'copyright'
    match = '.{0,5000}'
    return template.VarNode(name, original, match)

  def transform_bullet_node(self, node: xml.Element) -> template.Node:
    assert node.nodeType == xml.Node.ELEMENT_NODE
    original = self.transform_unprocessed(node)
    name = 'bullet'
    match = '.{0,20}'
    return template.VarNode(name, original, match)

  def transform_unprocessed(self, node: xml.Element) -> template.Node:
    if node.nodeType == xml.Node.TEXT_NODE:
      return self.transform_text_node(node)
    elif node.nodeType == xml.Node.ELEMENT_NODE:
      return template.SequentialNode(*[self.transform_node(child) for child in node.childNodes]).trim()
    else:
      raise NotImplementedError("Unsupported node type")


def parse_xml(text: xml.Element) -> template.Node:
  """
  Parses a dom element in the spdx-license-XML format and returns a Node.
  """
  transformer = _XmlTransformer()
  text.setAttribute('spacing', 'none')
  tree = transformer.transform_node(text)
  tree = tree.simplify()
  return tree
