# edited by claude
# Author: Joel Chua - Extra Feature 2: Top N Most Frequent Words
# LATEST EDITED: 28/07/2025

# features/joel2.py

def get_top_n_words(trie, n=5):
    """
    Traverse the trie and return the top N most frequent words.
    
    Parameters:
    - trie: The Trie instance containing the words and their frequencies.
    - n: The number of top frequent words to return (default is 5).
    
    Returns:
    - A list of tuples containing the top N words and their frequencies, sorted by frequency in descending order.
    """
    results = []

    def dfs(node, path):
        """
        Depth-First Search (DFS) helper function to traverse the trie and collect words with their frequencies.
        
        Parameters:
        - node: The current TrieNode being visited.
        - path: The current word being built from the Trie.
        """
        if node.is_terminal:
            results.append((path, node.frequency))  # Add word and frequency if it's a terminal node
        for char, child in node.children.items():
            dfs(child, path + char)  # Recursively call DFS on all child nodes

    dfs(trie.root, "")  # Start DFS from the root of the Trie
    # Sort the results by frequency (descending) and return the top N words
    return sorted(results, key=lambda x: x[1], reverse=True)[:n]

def run_feature_joel2(trie):
    """
    Runs the Top N Most Frequent Words feature. Prompts the user to input how many top words to display, 
    and then shows those words from the Trie based on frequency.
    
    Parameters:
    - trie: The Trie instance containing the words for autocomplete.
    """
    print("\n=== Extra Feature 4: Top N Most Frequent Words ===")

    if not trie.get_keywords():
        print("⚠️ Trie is empty. Please load or construct it first.")
        return

    while True:
        try:
            # Ask the user how many top words they want to display
            user_input = input("Enter how many top words to display (or '\\' to return): ").strip()
            if user_input == "\\":
                break  # Exit the loop if the user types '\\'

            # Ensure the user enters a valid number for N
            n = int(user_input)
            if n <= 0:
                print("⚠️ Please enter a number greater than 0.")
                continue  # Prompt again if the number is invalid

            top_words = get_top_n_words(trie, n)  # Get the top N most frequent words from the Trie
            if top_words:
                print(f"\nTop {n} most frequent words:")
                for i, (word, freq) in enumerate(top_words, 1):
                    print(f"{i}. {word} (frequency: {freq})")
            else:
                print("⚠️ No words found in the Trie.")

        except ValueError:
            # Handle the case where the user doesn't enter a valid integer
            print("⚠️ Please enter a valid number.")
