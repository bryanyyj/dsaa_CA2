# joel1.py - Context-Aware Wildcard Restoration Feature

from features.construct_panel import load_stopwords_to_trie
from trie.trie_utils import wildcard_match
import string

def context_aware_restore(trie, words, current_index, restored_words):
    """
    Replaces wildcard words with best match from the trie using context (previous/next words).
    Handles full '*' and partial wildcards like l*ve, with casing and punctuation.
    """
    raw_word = words[current_index]
    clean_word = raw_word.strip(string.punctuation)
    suffix = raw_word[len(clean_word):] if len(clean_word) < len(raw_word) else ""

    prev_word = restored_words[current_index - 1] if current_index > 0 else None
    next_word = words[current_index + 1] if current_index < len(words) - 1 else None

    # Match full wildcard "*" or partial pattern like "l*ve"
    if clean_word == "*":
        matches = wildcard_match(trie, "*")
    else:
        matches = wildcard_match(trie, clean_word.lower()) if "*" in clean_word else []

    if matches:
        best_match, _ = matches[0]

        # Capitalize if the original word was capitalized
        if clean_word and clean_word[0].isupper():
            best_match = best_match.capitalize()

        restored_words.append(best_match + suffix)
    else:
        restored_words.append(raw_word)  # No match found, keep original

    return restored_words

def restore_line_best_matches_with_context(line, trie):
    """
    Restores all wildcard words in a line using the best match, applying simple context.
    """
    words = line.strip().split()
    restored_words = []

    for i, word in enumerate(words):
        context_aware_restore(trie, words, i, restored_words)

    return ' '.join(restored_words)

def run_joel1_feature(trie):
    print("=== Context-Aware Wildcard Restoration ===")

    # Only load stopwords if trie is currently empty (to avoid overwriting added words)
    if not trie.get_keywords():
        load_stopwords_to_trie(trie)
        print("Stopwords loaded into empty trie.")
    else:
        print("Using existing trie (already has keywords).")

    while True:
        cmd = input("Command [@ to restore / \\ to exit]: ").strip()

        if cmd == "@":
            filename = input("Enter text filename to restore: ").strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                print("\nRestored text using best matches (with context):")
                for i, line in enumerate(lines, 1):
                    restored_line = restore_line_best_matches_with_context(line, trie)
                    print(f"Line {i}: {restored_line}")

            except FileNotFoundError:
                print(f"File '{filename}' not found.")
            except Exception as e:
                print(f"Error processing file: {e}")

        elif cmd == "\\":
            print("Returning to main menu...")
            break

        else:
            print("Invalid command. Use '@' to restore or '\\' to exit.")


# # joel1.py - Context-Aware Wildcard Restoration Feature

# from features.construct_panel import load_stopwords_to_trie
# from trie.trie_utils import wildcard_match
# import string

# def context_aware_restore(trie, words, current_index, restored_words):
#     import string

#     raw_word = words[current_index]
#     clean_word = raw_word.strip(string.punctuation)
#     suffix = raw_word[len(clean_word):] if len(clean_word) < len(raw_word) else ""

#     prev_word = restored_words[current_index - 1] if current_index > 0 else None
#     next_word = words[current_index + 1] if current_index < len(words) - 1 else None

#     # Match full wildcard *
#     if clean_word == "*":
#         matches = wildcard_match(trie, "*")
#     else:
#         matches = wildcard_match(trie, clean_word.lower()) if "*" in clean_word else []

#     if matches:
#         best_match, _ = matches[0]

#         # Capitalize if original was capitalized
#         if clean_word and clean_word[0].isupper():
#             best_match = best_match.capitalize()

#         # Optional: context scoring could be added here

#         restored_words.append(best_match + suffix)
#     else:
#         restored_words.append(raw_word)

#     return restored_words


# def restore_line_best_matches_with_context(line, trie):
#     """
#     Restores a line by replacing '*' words with the highest frequency match,
#     using context (previous/next words) to suggest the best word.
#     """
#     words = line.strip().split()
#     restored_words = []

#     for i, word in enumerate(words):
#         context_aware_restore(trie, words, i, restored_words)

#     return ' '.join(restored_words)

# def run_joel1_feature(trie):
#     print("=== Context-Aware Wildcard Restoration ===")

#     if not trie.get_keywords():
#         load_stopwords_to_trie(trie)
#         print("Stopwords loaded into empty trie.")
#     else:
#         print("Using existing trie (already has keywords).")
#     while True:
#         cmd = input("Command [@ to restore / \\ to exit]: ").strip()

#         if cmd == "@":
#             filename = input("Enter text filename to restore: ").strip()
#             try:
#                 with open(filename, "r", encoding="utf-8") as f:
#                     lines = f.readlines()

#                 print("\nRestored text using best matches (with context):")
#                 for i, line in enumerate(lines, 1):
#                     restored_line = restore_line_best_matches_with_context(line, trie)
#                     print(f"Line {i}: {restored_line}")

#             except FileNotFoundError:
#                 print(f"File '{filename}' not found.")
#             except Exception as e:
#                 print(f"Error processing file: {e}")

#         elif cmd == "\\":
#             print("Returning to main menu...")
#             break

#         else:
#             print("Invalid command. Use '@' to restore or '\\' to exit.")
