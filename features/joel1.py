# edited by claude
# Author: Joel Chua - Extra Feature 1: First & Last Word Auto-Complete
# LATEST EDITED: 28/07/2025

from trie.trie import Trie

def autocomplete_prefix(trie, prefix: str, limit=5):
    """
    Returns up to `limit` words from the trie that start with the given prefix.
    The results are sorted by frequency in descending order.
    
    Parameters:
    - trie: The Trie instance that holds the words and their frequencies.
    - prefix: The prefix to match words against.
    - limit: The maximum number of words to return (default is 5).
    
    Returns:
    - A list of tuples containing the matching words and their frequencies.
    """
    results = []

    def dfs(node, path):
        """
        Performs a depth-first search (DFS) on the Trie to find matching words.
        It adds words to the results if they are terminal nodes.
        
        Parameters:
        - node: The current TrieNode being visited.
        - path: The current word being built from the Trie.
        """
        if node.is_terminal:
            results.append((path, node.frequency))  # Add word and frequency
        for char in sorted(node.children.keys()):
            dfs(node.children[char], path + char)

    node = trie.root
    # Traverse the trie based on the prefix
    for char in prefix:
        if char in node.children:
            node = node.children[char]
        else:
            return []  # Return empty list if prefix is not found

    dfs(node, prefix)
    # Return sorted results by frequency (descending order) and limit to the requested number
    return sorted(results, key=lambda x: x[1], reverse=True)[:limit]

def run_joel1_feature(trie: Trie):
    """
    Runs the First & Last Word Auto-Complete feature. The user is prompted to
    input a sentence, and the function suggests completions for the first and 
    last words based on the Trie data.
    
    Parameters:
    - trie: The Trie instance containing the words for autocomplete.
    """
    print("\n=== Extra Feature 3: First & Last Word Auto-Complete ===")
    print("Type a partial sentence. This will suggest completions for the first and last words.")

    if not trie.get_keywords():
        print("⚠️ Trie is empty. Please load or construct it first.")
        return

    while True:
        sentence = input("\nEnter a sentence (or '\\' to return): ").strip()

        if sentence == "\\":
            break

        # Split the sentence into words and check if it's empty
        words = sentence.split()
        if not words:
            print("⚠️ Please type something.")
            continue

        # Get the first word and suggest completions
        first_prefix = words[0]
        print(f"\n🔍 Suggestions for first word '{first_prefix}':")
        first_suggestions = autocomplete_prefix(trie, first_prefix)
        if first_suggestions:
            for word, freq in first_suggestions:
                print(f" - {word} (frequency: {freq})")
        else:
            print("   😕 No suggestions found for the first word.")

        # Get the last word and suggest completions (only if more than one word is entered)
        last_prefix = words[-1]
        if first_prefix != last_prefix:
            print(f"\n🔍 Suggestions for last word '{last_prefix}':")
            last_suggestions = autocomplete_prefix(trie, last_prefix)
            if last_suggestions:
                for word, freq in last_suggestions:
                    print(f" - {word} (frequency: {freq})")
            else:
                print("   😕 No suggestions found for the last word.")
