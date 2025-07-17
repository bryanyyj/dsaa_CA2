# recent changes:
# 1. added search_with_wildcard
# 2. added restore_best_match

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
    
    # latest update
    def search_with_wildcard(self, word):
        """
        Searches for words in the trie that match the given word with wildcards ('*').
        Wildcard matches any character at that position.
        """
        def _search_with_wildcard(node, word, index):
            if index == len(word):
                return [word] if node.is_terminal else []
            
            # If the character is a wildcard, we need to explore all child nodes
            if word[index] == "*":
                matches = []
                for child in node.children.values():
                    matches += _search_with_wildcard(child, word, index + 1)
                return matches
            
            # If it's a normal character, move down the tree
            if word[index] in node.children:
                return _search_with_wildcard(node.children[word[index]], word, index + 1)
            return []

        return _search_with_wildcard(self.root, word, 0)
    
    # latest update
    def restore_best_match(self, word):
        """
        Restores a word by matching it to the best word in the trie, based on frequency.
        """
        matches = self.search_with_wildcard(word)
        if matches:
            best_match = max(matches, key=lambda match: self.get_word_frequency(match))
            return best_match
        return None