# edited by claude
# Author: Bryan Yeo & Joel Chua
# Latest edited: 28/07/2025

from trie.trie_node import TrieNode
from typing import List

class Trie:
    def __init__(self):
        """
        Initialize the Trie with a root node.
        The root node is a placeholder for the start of the trie.
        """
        self.root = TrieNode("")

    def insert(self, word, frequency=1):
        """
        Insert a word into the trie with the given frequency.
        If the word already exists, its frequency is increased.
        
        Parameters:
        word (str): The word to insert.
        frequency (int): The frequency of the word (default is 1).
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)  # Create new node if character doesn't exist
            node = node.children[char]
        
        if node.is_terminal:
            # If the word already exists, increment the frequency
            node.frequency += frequency
        else:
            # Mark as terminal and set the frequency for the new word
            node.is_terminal = True
            node.frequency = frequency

    def search(self, word):
        """
        Search for a word in the trie.
        
        Parameters:
        word (str): The word to search for.
        
        Returns:
        bool: True if the word is found, False otherwise.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_terminal

    def delete(self, word):
        """
        Delete a word from the trie.
        If the word is found, it is removed from the trie.
        
        Parameters:
        word (str): The word to delete.
        """
        def _delete(node, word, depth):
            # Base case: If depth equals the length of the word
            if depth == len(word):
                if not node.is_terminal:
                    return False  # Word not found
                node.is_terminal = False
                node.frequency = 0  # Reset frequency
                return len(node.children) == 0  # Return True if node has no children to delete

            char = word[depth]
            if char not in node.children:
                return False  # Character not found in the children
            
            should_delete = _delete(node.children[char], word, depth + 1)
            
            # Delete the node if it's no longer terminal and has no children
            if should_delete:
                del node.children[char]
                return not node.is_terminal and len(node.children) == 0
            return False

        _delete(self.root, word, 0)

    def clear(self):
        """Clear the trie, resetting the root node."""
        self.root = TrieNode("")

    def get_word_frequency(self, word):
        """
        Get the frequency of a word in the trie.
        
        Parameters:
        word (str): The word whose frequency is to be fetched.
        
        Returns:
        int: The frequency of the word, or 0 if the word is not found.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return 0  # Word not found
            node = node.children[char]
        return node.frequency if node.is_terminal else 0

    def search_with_wildcard(self, word):
        """
        Search for words that match the given pattern with wildcards ('*').
        Wildcard matches any character at that position.
        
        Parameters:
        word (str): The pattern to search, with '*' as a wildcard.
        
        Returns:
        list: A list of matching words.
        """
        def _search_with_wildcard(node, word, index):
            # Base case: if we reach the end of the word and it's a terminal node
            if index == len(word):
                return [word] if node.is_terminal else []
            
            # If the current character is a wildcard, explore all children
            if word[index] == "*":
                matches = []
                for child in node.children.values():
                    matches += _search_with_wildcard(child, word, index + 1)
                return matches
            
            # If it's a normal character, move down the trie
            if word[index] in node.children:
                return _search_with_wildcard(node.children[word[index]], word, index + 1)
            return []

        return _search_with_wildcard(self.root, word, 0)

    def restore_best_match(self, word):
        """
        Restores a word by matching it to the best word in the trie based on frequency.
        
        Parameters:
        word (str): The word pattern to restore with wildcards.
        
        Returns:
        str: The best match word or None if no match is found.
        """
        matches = self.search_with_wildcard(word)
        if matches:
            # Return the best match based on frequency
            best_match = max(matches, key=lambda match: self.get_word_frequency(match))
            return best_match
        return None

    def get_keywords(self) -> List[str]:
        """
        Get a list of all terminal (complete) keywords in the trie.
        
        Returns:
        List[str]: List of all words that are marked as terminal in the trie.
        """
        result = []

        def dfs(node, prefix):
            """Recursive depth-first search (DFS) to collect all words."""
            if node.is_terminal:
                result.append(prefix)  # Append complete words
            for char, child in node.children.items():
                dfs(child, prefix + char)  # Recursively call for all child nodes

        dfs(self.root, "")
        return result
