# features/joel2.py

def get_top_n_words(trie, n=5):
    """Traverse the trie and return the top N most frequent words."""
    results = []

    def dfs(node, path):
        if node.is_terminal:
            results.append((path, node.frequency))
        for char, child in node.children.items():
            dfs(child, path + char)

    dfs(trie.root, "")
    return sorted(results, key=lambda x: x[1], reverse=True)[:n]

def run_feature_joel2(trie):
    print("\n=== Extra Feature 4: Top N Most Frequent Words ===")

    if not trie.get_keywords():
        print("⚠️ Trie is empty. Please load or construct it first.")
        return

    while True:
        try:
            user_input = input("Enter how many top words to display (or '\\' to return): ").strip()
            if user_input == "\\":
                break

            n = int(user_input)
            if n <= 0:
                print("Please enter a number greater than 0.")
                continue

            top_words = get_top_n_words(trie, n)
            if top_words:
                print(f"\nTop {n} most frequent words:")
                for i, (word, freq) in enumerate(top_words, 1):
                    print(f"{i}. {word} (frequency: {freq})")
            else:
                print("No words found in the Trie.")
        except ValueError:
            print("⚠️ Please enter a valid number.")
