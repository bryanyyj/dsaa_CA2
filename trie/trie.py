from trie.trie_node import TrieNode

class Trie:
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        node.is_terminal = True
        node.frequency += 1

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_terminal

    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_terminal:
                    return False
                node.is_terminal = False
                return len(node.children) == 0
            char = word[depth]
            if char not in node.children:
                return False
            should_delete = _delete(node.children[char], word, depth + 1)
            if should_delete:
                del node.children[char]
                return not node.is_terminal and len(node.children) == 0
            return False
        _delete(self.root, word, 0)

    def clear(self):
        self.root = TrieNode("")
