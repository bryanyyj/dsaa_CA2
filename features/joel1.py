# features/joel1.py

from trie.trie import Trie

def autocomplete_prefix(trie, prefix: str, limit=5):
    """Returns up to `limit` words from the trie that start with the given prefix."""
    results = []

    def dfs(node, path):
        if len(results) >= limit:
            return
        if node.is_terminal:
            results.append((path, node.frequency))
        for char in sorted(node.children.keys()):
            dfs(node.children[char], path + char)

    node = trie.root
    for char in prefix:
        if char in node.children:
            node = node.children[char]
        else:
            return []  # prefix not found

    dfs(node, prefix)
    return sorted(results, key=lambda x: x[1], reverse=True)

def run_joel1_feature(trie: Trie):
    print("\n=== Extra Feature 3: First & Last Word Auto-Complete ===")
    print("Type a partial sentence. This will suggest completions for the first and last words.")

    if not trie.get_keywords():
        print("⚠️ Trie is empty. Please load or construct it first.")
        return

    while True:
        sentence = input("\nEnter a sentence (or '\\' to return): ").strip()
        if sentence == "\\":
            break

        words = sentence.split()
        if not words:
            print("Please type something.")
            continue

        # First word suggestions
        first_prefix = words[0]
        print(f"\n🔍 Suggestions for first word '{first_prefix}':")
        first_suggestions = autocomplete_prefix(trie, first_prefix)
        if first_suggestions:
            for word, freq in first_suggestions:
                print(f" - {word} (frequency: {freq})")
        else:
            print("   😕 No suggestions found.")

        # Last word suggestions (only if more than 1 word)
        last_prefix = words[-1]
        if first_prefix != last_prefix:
            print(f"\n🔍 Suggestions for last word '{last_prefix}':")
            last_suggestions = autocomplete_prefix(trie, last_prefix)
            if last_suggestions:
                for word, freq in last_suggestions:
                    print(f" - {word} (frequency: {freq})")
            else:
                print("   😕 No suggestions found.")
