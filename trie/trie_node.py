# edited by claude
# Author: Bryan Yeo & Joel Chua

class TrieNode:
    """
    Node class for the Trie data structure.
    Each node represents a character and contains references to its children.
    """
    def __init__(self, char):
        """
        Initialize a TrieNode with a character.
        
        Parameters:
        char (str): The character this node represents
        """
        self.char = char
        self.children = {}  # Dictionary to store child nodes
        self.is_terminal = False  # True if this node marks the end of a word
        self.frequency = 0  # Frequency of the word ending at this node
