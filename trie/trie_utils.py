import string

def load_keywords_from_file(filepath):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def write_keywords_to_file(filepath, keywords):
    with open(filepath, 'w') as f:
        for word in keywords:
            f.write(f"{word}\n")

def write_keywords_from_trie(trie, filename):
    """Write all keywords and their frequencies from the trie to a file."""
    words = []

    def _collect(node, current_word):
        if node.is_terminal:
            words.append(f"{current_word},{node.frequency}")
        for child in node.children.values():
            _collect(child, current_word + child.char)

    _collect(trie.root, "")

    try:
        with open(filename, "w", encoding="utf-8") as f:
            for entry in words:
                f.write(entry + "\n")
        print(f"Keywords successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def wildcard_match(trie, pattern):
    """
    Recursively search the trie to find all words matching the pattern,
    where '*' matches any single character.
    Returns a list of (word, frequency) tuples sorted by frequency descending.
    """
    if pattern == "*":
        return sorted(
            [(word, trie.get_word_frequency(word)) for word in trie.get_keywords()],
            key=lambda x: x[1],
            reverse=True
        )

    results = []

    def dfs(node, pattern_index, current_word):
        if pattern_index == len(pattern):
            if node.is_terminal:
                results.append((current_word, node.frequency))
            return

        current_char = pattern[pattern_index]

        if current_char == '*':
            for child in node.children.values():
                dfs(child, pattern_index + 1, current_word + child.char)
        else:
            if current_char in node.children:
                dfs(node.children[current_char], pattern_index + 1, current_word + current_char)

    dfs(trie.root, 0, "")
    return sorted(results, key=lambda x: x[1], reverse=True)

def restore_line_all_matches(line, trie):
    """
    Restores all matches in a line of text by replacing wildcard words with all possible matches.
    """
    words = line.strip().split()
    possibilities = [[]]

    for word in words:
        clean_word = word.strip(string.punctuation)
        suffix = word[len(clean_word):] if len(clean_word) < len(word) else ""

        if "*" in clean_word:
            matches = wildcard_match(trie, clean_word.lower())
            if matches:
                new_possibilities = []
                for base in possibilities:
                    for match, _ in matches:
                        if clean_word[0].isupper():
                            match = match.capitalize()
                        new_possibilities.append(base + [match + suffix])
                possibilities = new_possibilities
            else:
                for base in possibilities:
                    base.append(word)
        else:
            for base in possibilities:
                base.append(word)

    return [' '.join(words) for words in possibilities]

def restore_line_best_matches(line, trie):
    """
    Restores a line by replacing '*' words with the highest frequency match only.
    """
    words = line.strip().split()
    restored_words = []

    for word in words:
        clean_word = word.strip(string.punctuation)
        suffix = word[len(clean_word):] if len(clean_word) < len(word) else ""

        if "*" in clean_word:
            matches = wildcard_match(trie, clean_word.lower())
            if matches:
                best_match, _ = matches[0]
                if clean_word[0].isupper():
                    best_match = best_match.capitalize()
                restored_words.append(best_match + suffix)
            else:
                restored_words.append(word)
        else:
            restored_words.append(word)

    return ' '.join(restored_words)
