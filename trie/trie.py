# Joel's Updated trie.py
from trie.trie_node import TrieNode

class Trie:
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word, frequency=1):
        """Insert word with specified frequency (default 1 for new words)"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        
        if node.is_terminal:
            # Word already exists - add to frequency
            node.frequency += frequency
        else:
            # New word - set frequency
            node.is_terminal = True
            node.frequency = frequency

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
                node.frequency = 0  # Reset frequency
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

    def get_word_frequency(self, word):
        """Get frequency of a word (0 if not found)"""
        node = self.root
        for char in word:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.frequency if node.is_terminal else 0

# bryan's version (ori)
# from trie.trie_node import TrieNode

# class Trie:
#     def __init__(self):
#         self.root = TrieNode("")

#     def insert(self, word):
#         node = self.root
#         for char in word:
#             if char not in node.children:
#                 node.children[char] = TrieNode(char)
#             node = node.children[char]
#         node.is_terminal = True
#         node.frequency += 1

#     def search(self, word):
#         node = self.root
#         for char in word:
#             if char not in node.children:
#                 return False
#             node = node.children[char]
#         return node.is_terminal

#     def delete(self, word):
#         def _delete(node, word, depth):
#             if depth == len(word):
#                 if not node.is_terminal:
#                     return False
#                 node.is_terminal = False
#                 return len(node.children) == 0
#             char = word[depth]
#             if char not in node.children:
#                 return False
#             should_delete = _delete(node.children[char], word, depth + 1)
#             if should_delete:
#                 del node.children[char]
#                 return not node.is_terminal and len(node.children) == 0
#             return False
#         _delete(self.root, word, 0)

#     def clear(self):
#         self.root = TrieNode("")
