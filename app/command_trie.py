class TrieNode:
    def __init__(self):
        self.children = {}  # Use dict to support any characters
        self.is_end_of_word = False
        self.word = None  # Store the full word for retrieval

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word  # Store the original word

    def _search_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node, words):
        if node.is_end_of_word:
            words.append(node.word)
        for child in node.children.values():
            self._collect_words(child, words)

    def autocomplete(self, prefix):
        node = self._search_node(prefix)
        words = []
        if node:
            self._collect_words(node, words)
        return words