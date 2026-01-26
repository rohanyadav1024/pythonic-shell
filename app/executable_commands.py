class TrieNode:
    def __init__(self):
        self.children = [None] * 26  # Assuming only lowercase a-z
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def _char_to_index(self, char):
        return ord(char) - ord('a')

    def insert(self, word):
        node = self.root
        for char in word:
            index = self._char_to_index(char)
            if not node.children[index]:
                node.children[index] = TrieNode()
            node = node.children[index]
        node.is_end_of_word = True

    def _search_node(self, prefix):
        node = self.root
        for char in prefix:
            index = self._char_to_index(char)
            if not node.children[index]:
                return None
            node = node.children[index]
        return node

    def _collect_words(self, node, prefix, words):
        if node.is_end_of_word:
            words.append(prefix)
        for i in range(26):
            if node.children[i]:
                self._collect_words(node.children[i], prefix + chr(i + ord('a')), words)

    def autocomplete(self, prefix):
        node = self._search_node(prefix)
        words = []
        if node:
            self._collect_words(node, prefix, words)
        return words