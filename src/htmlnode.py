

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):

    def __init__(self, tag: str | None, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode value cannot be empty")  
        if self.tag is None:
            return self.value
        
        space = " " if self.props else ""

        return f"<{self.tag}{space}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    
        def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
            super().__init__(tag=tag, children=children, props=props)
    
        def to_html(self) -> str:
            if self.tag is None:
                raise ValueError("ParentNode must have a tag")
            
            if not self.children:
                raise ValueError("ParentNode must have children")

            children = "".join([child.to_html() for child in self.children])
            space = " " if self.props else ""
    
            return f"<{self.tag}{space}{self.props_to_html()}>{children}</{self.tag}>"
    