# edited by claude
# Author: Bryan Yeo & Joel Chua
# latest edited: 28/07/2025

import string

# Function to load keywords from a file and return a list of non-empty lines
def load_keywords_from_file(filepath):
    """Reads keywords from a file and returns them as a list."""
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]  # Return non-empty lines
    except FileNotFoundError:
        print(f"⚠️ File '{filepath}' not found.")
        return []
    except Exception as e:
        print(f"⚠️ Error loading file: {e}")
        return []

# Function to write a list of keywords to a specified file
def write_keywords_to_file(filepath, keywords):
    """Writes the given keywords to a file, one per line."""
    try:
        with open(filepath, 'w') as f:
            for word in keywords:
                f.write(f"{word}\n")
        print(f"✅ Keywords successfully written to {filepath}")
    except Exception as e:
        print(f"⚠️ Error writing to file: {e}")

# Function to write all keywords and their frequencies from the Trie to a file
def write_keywords_from_trie(trie, filename):
    """Writes all keywords and their frequencies from the Trie to a file."""
    words = []

    def _collect(node, current_word):
        """Recursively collects terminal words from the Trie with their frequencies."""
        if node.is_terminal:
            words.append(f"{current_word},{node.frequency}")
        for child in node.children.values():
            _collect(child, current_word + child.char)

    _collect(trie.root, "")  # Start collecting from the root of the Trie

    try:
        with open(filename, "w", encoding="utf-8") as f:
            for entry in words:
                f.write(entry + "\n")
        print(f"✅ Keywords successfully written to {filename}")
    except Exception as e:
        print(f"⚠️ Error writing to file: {e}")

# Function to perform wildcard search, matching any word with a '*' in it
def wildcard_match(trie, pattern):
    """
    Recursively searches the trie to find all words matching the given pattern,
    where '*' matches any character at that position.
    Returns a list of (word, frequency) tuples sorted by frequency in descending order.
    """
    if pattern == "*":
        # Special case: if pattern is "*", return only single-character words
        return sorted(
            [(word, trie.get_word_frequency(word)) for word in trie.get_keywords() if len(word) == 1],
            key=lambda x: x[1],
            reverse=True
        )

    results = set()  # Use set to avoid duplicates

    def dfs(node, pattern_index, current_word):
        """Helper function for recursive depth-first search."""
        if pattern_index == len(pattern):
            if node.is_terminal:
                results.add((current_word, node.frequency))
            return

        current_char = pattern[pattern_index]

        # If the current character is a wildcard '*'
        if current_char == '*':
            # * matches exactly ONE character - explore all children and advance pattern
            for child in node.children.values():
                dfs(child, pattern_index + 1, current_word + child.char)
        else:
            # Otherwise, match the specific character
            if current_char in node.children:
                dfs(node.children[current_char], pattern_index + 1, current_word + current_char)

    dfs(trie.root, 0, "")
    return sorted(list(results), key=lambda x: x[1], reverse=True)

# Function to restore all matches for wildcard words in a line of text
def restore_line_all_matches(line, trie):
    """
    Restores all matches in a line of text by replacing wildcard words with all possible matches.
    Returns the text with wildcard replacements shown in ['word1','word2'] format.
    """
    words = line.strip().split()
    result_words = []

    for word in words:
        # Remove punctuation but preserve wildcards (*)
        punctuation_without_wildcard = string.punctuation.replace('*', '')
        clean_word = word.strip(punctuation_without_wildcard)
        suffix = word[len(clean_word):] if len(clean_word) < len(word) else ""  # Preserve punctuation at the end

        if "*" in clean_word:
            # If the word contains a wildcard '*', find all matching words
            matches = wildcard_match(trie, clean_word.lower())
            if matches:
                # Format matches as ['word1','word2','word3']
                match_words = []
                for match, _ in matches:
                    # If the first letter is uppercase, capitalize the match
                    if clean_word[0].isupper():
                        match = match.capitalize()
                    match_words.append(f"'{match}'")
                
                # Create the bracket format
                bracket_format = "[" + ",".join(match_words) + "]" + suffix
                result_words.append(bracket_format)
            else:
                result_words.append(word)  # If no match, retain the original word
        else:
            result_words.append(word)  # If no wildcard, retain the original word

    # Return the restored line as a single string
    return ' '.join(result_words)

# Function to restore a line by replacing wildcard words with the best match (highest frequency)
def restore_line_best_matches(line, trie):
    """
    Restores a line by replacing wildcard words with the highest frequency match only.
    Returns format with <word> brackets to show restored words.
    """
    words = line.strip().split()
    restored_words = []  # This will store the restored line of words

    for word in words:
        # Check if word is in bracket format ['word1','word2','word3']
        if word.startswith("[") and "]" in word:
            # Find the end of the bracket and preserve any trailing punctuation
            bracket_end = word.find("]")
            bracket_part = word[:bracket_end+1]
            suffix = word[bracket_end+1:]  # Any punctuation after the ]
            
            # Extract words from bracket format like ['of','on','or']
            bracket_content = bracket_part[1:-1]  # Remove [ and ]
            # Split by ',' and clean up quotes - handle both 'word' and word formats
            word_options = []
            for w in bracket_content.split(","):
                cleaned = w.strip().strip("'\"")
                if cleaned:  # Only add non-empty options
                    word_options.append(cleaned)
            
            if word_options:
                # Find the best match based on frequency in trie
                best_word = None
                best_freq = 0
                
                for option in word_options:
                    freq = trie.get_word_frequency(option.lower())
                    if freq > best_freq:
                        best_freq = freq
                        best_word = option
                
                if best_word:
                    restored_words.append("<" + best_word + ">" + suffix)
                else:
                    # If none found in trie, take the first option
                    restored_words.append("<" + word_options[0] + ">" + suffix)
            else:
                restored_words.append(word)  # Keep original if no valid options
        else:
            # Handle normal wildcards and regular words
            # Remove punctuation but preserve wildcards (*)
            punctuation_without_wildcard = string.punctuation.replace('*', '')
            clean_word = word.strip(punctuation_without_wildcard)
            suffix = word[len(clean_word):] if len(clean_word) < len(word) else ""  # Preserve punctuation at the end

            if "*" in clean_word:
                # If the word contains a wildcard '*', find the best match
                matches = wildcard_match(trie, clean_word.lower())
                if matches:
                    best_match, _ = matches[0]  # Select the best match (highest frequency)
                    if clean_word[0].isupper():
                        best_match = best_match.capitalize()  # Capitalize if the original word was capitalized
                    restored_words.append("<" + best_match + ">" + suffix)  # Add the match with <> brackets
                else:
                    restored_words.append(word)  # If no match, keep the original word
            else:
                restored_words.append(word)  # If no wildcard, keep the original word

    # Return the restored line as a single string
    return ' '.join(restored_words)
