# edited by claude
# Author: Bryan Yeo - Extra Feature 2: Enhanced Pattern Search

import re

def parse_pattern(pattern: str) -> list:
    """
    Parses a regex-like pattern into a list of tokens.
    Supports:
    - '.' wildcard
    - '[abc]' character set
    - '{n}' exact count of wildcards
    """
    tokens = []
    i = 0
    while i < len(pattern):
        if pattern[i] == '.':
            tokens.append('.')
            i += 1
        elif pattern[i] == '[':
            j = i + 1
            while j < len(pattern) and pattern[j] != ']':
                j += 1
            tokens.append(set(pattern[i+1:j]))
            i = j + 1
        elif pattern[i] == '{':
            j = i + 1
            while j < len(pattern) and pattern[j] != '}':
                j += 1
            n = int(pattern[i+1:j])
            tokens.extend(['.'] * n)
            i = j + 1
        else:
            tokens.append(pattern[i])
            i += 1
    return tokens

def enhanced_pattern_search(trie, pattern: str) -> list:
    results = []
    tokens = parse_pattern(pattern)

    def dfs(node, idx, path):
        if idx == len(tokens):
            if node.is_terminal:
                results.append((path, node.frequency if hasattr(node, 'frequency') else 0))
            return

        token = tokens[idx]
        if token == '.':
            for char, child in node.children.items():
                dfs(child, idx + 1, path + char)
        elif isinstance(token, set):  # character set
            for char in token:
                if char in node.children:
                    dfs(node.children[char], idx + 1, path + char)
        elif token in node.children:
            dfs(node.children[token], idx + 1, path + token)

    dfs(trie.root, 0, "")
    return sorted(results, key=lambda x: x[1], reverse=True)

def run_feature_bryan2(trie):
    print("\n=== Extra Feature 2: Enhanced Pattern Search ===")
    print("Supports:")
    print(" - '.' for any single character (e.g. c.t)")
    print(" - '[ae]' for character sets (e.g. c[ae]t)")
    print(" - '{n}' for exact wildcard counts (e.g. b.{2}d)")

    if not trie.get_keywords():
        print("⚠️ Trie is empty. Please construct or load a trie first.")
        return

    while True:
        pattern = input("\nEnter a pattern (or '\\' to return): ").strip().lower()
        if pattern == "\\":
            break

        matches = enhanced_pattern_search(trie, pattern)
        if matches:
            print(f"\n🔍 Matches for pattern '{pattern}' (sorted by frequency):")
            for word, freq in matches:
                print(f" - {word} (freq: {freq})")
        else:
            print("😕 No matches found.")
