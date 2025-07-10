# src/memory_linker/memory_graph.py

"""
Here comes AYAMAI’s long-term memory—let’s give it the ability to *remember, relink, and reimagine*. This module stores
 understanding fragments (U→D encodings) and connects them into evolving memory graphs that can be traversed during dreaming or introspection.
"""

import uuid
from collections import defaultdict

class MemoryNode:
    def __init__(self, concept, attributes=None, behaviors=None):
        self.id = str(uuid.uuid4())
        self.concept = concept
        self.attributes = attributes or []
        self.behaviors = behaviors or []
        self.links = defaultdict(list)  # relation_type -> [MemoryNode]

    def __repr__(self):
        return f"<U:{self.concept}>"

class MemoryGraph:
    def __init__(self):
        self.nodes = {}  # id -> MemoryNode
        self.index = {}  # concept -> node.id

    def add_node(self, concept, attributes=None, behaviors=None):
        if concept in self.index:
            return self.nodes[self.index[concept]]

        node = MemoryNode(concept, attributes, behaviors)
        self.nodes[node.id] = node
        self.index[concept] = node.id
        print(f"🧠 New memory node: {concept}")
        return node

    def link(self, source_concept, target_concept, relation_type="related_to"):
        src = self.add_node(source_concept)
        tgt = self.add_node(target_concept)
        src.links[relation_type].append(tgt)
        print(f"🔗 Linked '{src.concept}' → '{tgt.concept}' as [{relation_type}]")

    def get_related(self, concept, relation_type="related_to"):
        node = self.nodes.get(self.index.get(concept))
        if not node:
            return []
        return node.links.get(relation_type, [])

    def traverse_memory(self, start_concept, depth=2, visited=None):
        visited = visited or set()
        if start_concept in visited or depth == 0:
            return []
        visited.add(start_concept)

        node = self.nodes.get(self.index.get(start_concept))
        if not node:
            return []

        chain = [node.concept]
        for rel_type, targets in node.links.items():
            for tgt in targets:
                chain += self.traverse_memory(tgt.concept, depth - 1, visited)
        return chain


# Example usage
if __name__ == "__main__":
    mg = MemoryGraph()
    mg.link("Ayurveda", "5-element theory", "embeds")
    mg.link("5-element theory", "entropy", "explains")
    mg.link("entropy", "dreams", "guides")
    mg.link("dreams", "story generation", "enables")

    print("\n🧵 Narrative Path:")
    path = mg.traverse_memory("Ayurveda", depth=3)
    for step in path:
        print("→", step)
