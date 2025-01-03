import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_special_chars(self):
        node = HTMLNode(props={"data-test": "test&<>"})
        self.assertEqual(node.props_to_html(), ' data-test="test&<>"')

    class TestHTMLNode(unittest.TestCase):
        def test_props_to_html_with_special_chars(self):
            node = HTMLNode(props={"data-test": "test&<>"})
            self.assertEqual(node.props_to_html(), ' data-test="test&<>"')

    def test_props_to_html_with_numbers(self):
        node = HTMLNode(props={"width": "100", "height": "200"})
        self.assertTrue(' width="100"' in node.props_to_html())
        self.assertTrue(' height="200"' in node.props_to_html())

    def test_init_with_children_list(self):
        child1 = HTMLNode("p", "first")
        child2 = HTMLNode("p", "second") 
        node = HTMLNode("div", children=[child1, child2])
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].value, "first")
        self.assertEqual(node.children[1].value, "second")

    def test_init_with_all_params(self):
        child = HTMLNode("span", "child")
        node = HTMLNode(
            tag="div",
            value="parent",
            children=[child],
            props={"class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "parent")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.props["class"], "container")
        
    def test_props_to_html_with_boolean_props(self):
        node = HTMLNode(props={"checked": True, "disabled": False})
        self.assertTrue(' checked="True"' in node.props_to_html())
        self.assertTrue(' disabled="False"' in node.props_to_html())

    def test_nested_children_init(self):
        grandchild = HTMLNode("b", "bold")
        child = HTMLNode("p", children=[grandchild])
        parent = HTMLNode("div", children=[child])
        self.assertEqual(parent.children[0].children[0].value, "bold")

    def test_repr(self):
        node = HTMLNode("div", "hello", None, {"class": "btn"})
        self.assertEqual(repr(node), 'HTMLNode(div,hello,None,{\'class\': \'btn\'})')

    def test_repr_with_children(self):
        child = HTMLNode("span", "child")
        node = HTMLNode("div", "parent", [child], {"class": "container"})
        self.assertEqual(repr(node), 'HTMLNode(div,parent,[HTMLNode(span,child,None,None)],{\'class\': \'container\'})')

    def test_repr_with_no_props(self):
        node = HTMLNode("div", "hello")
        self.assertEqual(repr(node), 'HTMLNode(div,hello,None,None)')

class TestLeafNode(unittest.TestCase):
    def test_leafnode_basic(self):
        node = LeafNode("span", "Hello Leaf")
        self.assertEqual(node.to_html(), '<span>Hello Leaf</span>')
        self.assertIsNone(node.children)

    def test_leafnode_no_value(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leafnode_repr(self):
        node = LeafNode("img", None, {"src": "image.png"})
        self.assertEqual(repr(node), "LeafNode(img, None, {'src': 'image.png'})")

    def test_leafnode_props_to_html(self):
        node = LeafNode("input", None, {"type": "checkbox", "checked": True})
        with self.assertRaises(ValueError):
            node.to_html()
        self.assertIn(' type="checkbox"', node.props_to_html())
        self.assertIn(' checked="True"', node.props_to_html())
        
class TestParentNode(unittest.TestCase):
    def test_parentnode_basic(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>child</span></div>')

    def test_parentnode_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")]).to_html()

    def test_parentnode_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parentnode_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == '__main__':
    unittest.main()