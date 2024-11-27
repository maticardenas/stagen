import unittest

from utils import is_markdown_heading, is_markdown_codeblock, is_markdown_ordered_list


class TestUtils(unittest.TestCase):

    def test_is_markdown_heading(self):
        self.assertTrue(is_markdown_heading("# This is a heading"))
        self.assertTrue(is_markdown_heading("## This is a heading"))
        self.assertTrue(is_markdown_heading("### This is also a heading"))
        self.assertTrue(is_markdown_heading("#### This is also a heading"))
        self.assertTrue(is_markdown_heading("##### This is also a heading"))
        self.assertTrue(is_markdown_heading("###### This is a heading"))
        self.assertFalse(is_markdown_heading("This is not a heading"))
        self.assertFalse(is_markdown_heading("###This is not a heading"))
        
    
    def test_is_markdown_codeblock(self):
        markdown_text = "```one line code block```"
        self.assertTrue(is_markdown_codeblock(markdown_text))
    
    def test_is_markdown_codeblock_multiline(self):
        markdown_text = """```
        multiline code block```"""
        self.assertTrue(is_markdown_codeblock(markdown_text))

    def test_is_markdown_codeblock_no_codeblock(self):
        markdown_text = "This is not a code block"
        self.assertFalse(is_markdown_codeblock(markdown_text))
    
    def test_is_markdown_codeblock_no_closed_backticks(self):
        markdown_text = """```not closed codeblock"""
        self.assertFalse(is_markdown_codeblock(markdown_text))

    def test_is_markdown_ordered_list(self):
        markdown_text = "1. First item\n2. Second item\n3. Third item"
        self.assertTrue(is_markdown_ordered_list(markdown_text))
    
    def test_is_markdown_ordered_list_not_ordered(self):
        markdown_text = "1. First item\n3. Third item"
        self.assertFalse(is_markdown_ordered_list(markdown_text))
    
    def test_is_markdown_ordered_list_no_number(self):
        markdown_text = "First item\nSecond item\nThird item"
        self.assertFalse(is_markdown_ordered_list(markdown_text))

    def test_is_markdown_ordered_list_no_dot(self):
        markdown_text = "1 First item\n2 Second item\n3 Third item"
        self.assertFalse(is_markdown_ordered_list(markdown_text))