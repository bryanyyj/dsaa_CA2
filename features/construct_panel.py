# Joel's updated construct_panel.py 2.0
from trie.trie import Trie
from trie.trie_utils import load_keywords_from_file, write_keywords_to_file

trie = Trie()

CONSTRUCT_MENU = '''
------------------------------------------------------------
Construct/Edit Trie Commands:
'+', '-', '?', '#', '@', '~', '=', '!', '\\'
------------------------------------------------------------
+<keyword>   (add a keyword)
-<keyword>   (delete a keyword)
?<keyword>   (find a keyword)
#            (display Trie)
@            (write Trie to file)
~            (read keywords from file to make Trie)
=            (write keywords from Trie to file)
!            (print instructions)
\\           (exit)
------------------------------------------------------------
'''

CONSTRUCT_INSTRUCTIONS = '''
Construct/Edit Trie Commands:
+   Adds a new keyword to the current Trie.
-   Deletes a keyword from the current Trie.
?   Searches for a keyword in the current Trie.
#   Displays the current Trie on the screen.
@   Writes the current Trie to a file.
~   Reads keywords from a file to make a new Trie (thereby clearing the current Trie).
=   Writes all the keywords from the current Trie to a file.
!   Prints the instructions for the various Construct/Edit Trie Commands.
\\  Exits the Edit Trie Command Prompt and returns to the main menu.
'''

def load_stopwords_to_trie(trie, filepath="data/stopwordsFreq.txt"):
    """Load stopwords with their frequencies from file"""
    trie.clear()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    # Split only on first comma to handle edge cases
                    word, freq_str = line.split(",", 1)
                    word = word.strip()
                    try:
                        frequency = int(freq_str.strip())
                        if word:  # Only add non-empty words
                            trie.insert(word, frequency)
                    except ValueError:
                        print(f"Warning: Invalid frequency for word '{word}': {freq_str}")
                        continue
        print(f"Successfully loaded stopwords from {filepath}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"Error loading stopwords: {e}")

# New: Added the function to display the trie structure
def display_trie(trie):
    """Display the trie structure."""
    def _display_node(node, word):
        """Recursive helper function to traverse and display the trie."""
        # If it's a terminal node (end of a word), print the word and its frequency
        if node.is_terminal:
            print(f"Word: {word}, Frequency: {node.frequency}")
        
        # Recursively display each child node
        for child in node.children.values():
            _display_node(child, word + child.char)

    print("Trie structure:")
    _display_node(trie.root, "")

def run_construct_panel():
    print("=== Construct/Edit Trie ===")
    print(CONSTRUCT_MENU)
    while True:
        cmd = input("Command [+ - ? # @ ~ = ! \\]: ").strip()
        if cmd.startswith("+"):
            word = cmd[1:].strip()
            if word:
                trie.insert(word)
                print(f"Added: {word}")
            else:
                print("Please provide a keyword after '+'.")
        elif cmd.startswith("-"):
            word = cmd[1:].strip()
            if word:
                if trie.search(word):
                    trie.delete(word)
                    print(f"Deleted: {word}")
                else:
                    print(f"Warning: '{word}' not found in trie.")
            else:
                print("Please provide a keyword after '-'.")
        elif cmd.startswith("?"):
            word = cmd[1:].strip()
            if word:
                if trie.search(word):
                    freq = trie.get_word_frequency(word)
                    print(f"Found: {word} (frequency: {freq})")
                else:
                    print(f"Not found: {word}")
            else:
                print("Please provide a keyword after '?'.")
        elif cmd == "#":
            # New: Display the trie structure when user selects the '#' command
            print("Trie Display:")
            display_trie(trie)  # Calls the `display_trie` function to show the trie structure
        elif cmd == "@":
            filename = input("Enter filename to write trie to: ").strip()
            if filename:
                write_trie_to_file(trie, filename)
            else:
                print("Please provide a filename.")
        elif cmd == "~":
            filename = input("Enter filename to read keywords from (or press Enter for default): ").strip()
            if not filename:
                filename = "data/stopwordsFreq.txt"
            load_stopwords_to_trie(trie, filename)
        elif cmd == "=":
            filename = input("Enter filename to write keywords to: ").strip()
            if filename:
                write_keywords_from_trie(trie, filename)
            else:
                print("Please provide a filename.")
        elif cmd == "!":
            print(CONSTRUCT_INSTRUCTIONS)
        elif cmd == "\\":
            break
        else:
            print("Invalid command. Type ! for instructions.")

# Placeholder for writing the trie structure to a file
def write_trie_to_file(trie, filename):
    """Write trie structure to file - placeholder for now"""
    print(f"[Writing trie to {filename} - to be implemented]")

# Placeholder for writing all keywords from trie to a file
def write_keywords_from_trie(trie, filename):
    """Write all keywords from trie to file - placeholder for now"""
    print(f"[Writing keywords to {filename} - to be implemented]")


# Joel's updated construct_panel.py 1.0
# from trie.trie import Trie
# from trie.trie_utils import load_keywords_from_file, write_keywords_to_file

# trie = Trie()

# CONSTRUCT_MENU = '''
# ------------------------------------------------------------
# Construct/Edit Trie Commands:
# '+', '-', '?', '#', '@', '~', '=', '!', '\\'
# ------------------------------------------------------------
# +<keyword>   (add a keyword)
# -<keyword>   (delete a keyword)
# ?<keyword>   (find a keyword)
# #            (display Trie)
# @            (write Trie to file)
# ~            (read keywords from file to make Trie)
# =            (write keywords from Trie to file)
# !            (print instructions)
# \\           (exit)
# ------------------------------------------------------------
# '''

# CONSTRUCT_INSTRUCTIONS = '''
# Construct/Edit Trie Commands:
# +   Adds a new keyword to the current Trie.
# -   Deletes a keyword from the current Trie.
# ?   Searches for a keyword in the current Trie.
# #   Displays the current Trie on the screen.
# @   Writes the current Trie to a file.
# ~   Reads keywords from a file to make a new Trie (thereby clearing the current Trie).
# =   Writes all the keywords from the current Trie to a file.
# !   Prints the instructions for the various Construct/Edit Trie Commands.
# \\  Exits the Edit Trie Command Prompt and returns to the main menu.
# '''

# def load_stopwords_to_trie(trie, filepath="data/stopwordsFreq.txt"):
#     """Load stopwords with their frequencies from file"""
#     trie.clear()
#     try:
#         with open(filepath, "r", encoding="utf-8") as f:
#             for line in f:
#                 line = line.strip()
#                 if line and ',' in line:
#                     # Split only on first comma to handle edge cases
#                     word, freq_str = line.split(",", 1)
#                     word = word.strip()
#                     try:
#                         frequency = int(freq_str.strip())
#                         if word:  # Only add non-empty words
#                             trie.insert(word, frequency)
#                     except ValueError:
#                         print(f"Warning: Invalid frequency for word '{word}': {freq_str}")
#                         continue
#         print(f"Successfully loaded stopwords from {filepath}")
#     except FileNotFoundError:
#         print(f"Error: File {filepath} not found.")
#     except Exception as e:
#         print(f"Error loading stopwords: {e}")

# def run_construct_panel():
#     print("=== Construct/Edit Trie ===")
#     print(CONSTRUCT_MENU)
#     while True:
#         cmd = input("Command [+ - ? # @ ~ = ! \\]: ").strip()
#         if cmd.startswith("+"):
#             word = cmd[1:].strip()
#             if word:
#                 trie.insert(word)
#                 print(f"Added: {word}")
#             else:
#                 print("Please provide a keyword after '+'.")
#         elif cmd.startswith("-"):
#             word = cmd[1:].strip()
#             if word:
#                 if trie.search(word):
#                     trie.delete(word)
#                     print(f"Deleted: {word}")
#                 else:
#                     print(f"Warning: '{word}' not found in trie.")
#             else:
#                 print("Please provide a keyword after '-'.")
#         elif cmd.startswith("?"):
#             word = cmd[1:].strip()
#             if word:
#                 if trie.search(word):
#                     freq = trie.get_word_frequency(word)
#                     print(f"Found: {word} (frequency: {freq})")
#                 else:
#                     print(f"Not found: {word}")
#             else:
#                 print("Please provide a keyword after '?'.")
#         elif cmd == "#":
#             print("Trie Display:")
#             display_trie(trie)
#         elif cmd == "@":
#             filename = input("Enter filename to write trie to: ").strip()
#             if filename:
#                 write_trie_to_file(trie, filename)
#             else:
#                 print("Please provide a filename.")
#         elif cmd == "~":
#             filename = input("Enter filename to read keywords from (or press Enter for default): ").strip()
#             if not filename:
#                 filename = "data/stopwordsFreq.txt"
#             load_stopwords_to_trie(trie, filename)
#         elif cmd == "=":
#             filename = input("Enter filename to write keywords to: ").strip()
#             if filename:
#                 write_keywords_from_trie(trie, filename)
#             else:
#                 print("Please provide a filename.")
#         elif cmd == "!":
#             print(CONSTRUCT_INSTRUCTIONS)
#         elif cmd == "\\":
#             break
#         else:
#             print("Invalid command. Type ! for instructions.")

# def display_trie(trie):
#     """Display the trie structure - placeholder for now"""
#     print("[Trie structure display - to be implemented next]")

# def write_trie_to_file(trie, filename):
#     """Write trie structure to file - placeholder for now"""
#     print(f"[Writing trie to {filename} - to be implemented]")

# def write_keywords_from_trie(trie, filename):
#     """Write all keywords from trie to file - placeholder for now"""
#     print(f"[Writing keywords to {filename} - to be implemented]")

# bryan's version (ori)
# from trie.trie import Trie
# from trie.trie_utils import load_keywords_from_file, write_keywords_to_file

# trie = Trie()

# CONSTRUCT_MENU = '''
# ------------------------------------------------------------
# Construct/Edit Trie Commands:
# '+', '-', '?', '#', '@', '~', '=', '!', '\\'
# ------------------------------------------------------------
# +<keyword>   (add a keyword)
# -<keyword>   (delete a keyword)
# ?<keyword>   (find a keyword)
# #            (display Trie)
# @            (write Trie to file)
# ~            (read keywords from file to make Trie)
# =            (write keywords from Trie to file)
# !            (print instructions)
# \\           (exit)
# ------------------------------------------------------------
# '''

# CONSTRUCT_INSTRUCTIONS = '''
# Construct/Edit Trie Commands:
# +   Adds a new keyword to the current Trie.
# -   Deletes a keyword from the current Trie.
# ?   Searches for a keyword in the current Trie.
# #   Displays the current Trie on the screen.
# @   Writes the current Trie to a file.
# ~   Reads keywords from a file to make a new Trie (thereby clearing the current Trie).
# =   Writes all the keywords from the current Trie to a file.
# !   Prints the instructions for the various Construct/Edit Trie Commands.
# \\  Exits the Edit Trie Command Prompt and returns to the main menu.
# '''

# def load_stopwords_to_trie(trie, filepath="data/stopwordsFreq.txt"):
#     trie.clear()  # Assuming your Trie class has a clear() method; if not, implement it.
#     with open(filepath, "r", encoding="utf-8") as f:
#         for line in f:
#             word = line.split(",", 1)[0].strip()
#             if word:
#                 trie.insert(word)

# def run_construct_panel():
#     print("=== Construct/Edit Trie ===")
#     print(CONSTRUCT_MENU)
#     while True:
#         cmd = input("Command [+ - ? # @ ~ = ! \\]: ")
#         if cmd.startswith("+"):
#             word = cmd[1:].strip()
#             if word:
#                 trie.insert(word)
#                 print(f"Added: {word}")
#             else:
#                 print("Please provide a keyword after '+'.")
#         elif cmd.startswith("-"):
#             word = cmd[1:].strip()
#             if word:
#                 trie.delete(word)
#                 print(f"Deleted: {word}")
#             else:
#                 print("Please provide a keyword after '-'.")
#         elif cmd.startswith("?"):
#             word = cmd[1:].strip()
#             if word:
#                 print("Found!" if trie.search(word) else "Not found.")
#             else:
#                 print("Please provide a keyword after '?'.")
#         elif cmd == "#":
#             print("[Trie structure display not implemented yet]")
#         elif cmd == "@":
#             print("[Write Trie to file not implemented yet]")
#         elif cmd == "~":
#             load_stopwords_to_trie(trie)
#             print("Loaded stopwords from data/stopwordsFreq.txt into Trie.")
#         elif cmd == "=":
#             print("[Write keywords from Trie to file not implemented yet]")
#         elif cmd == "!":
#             print(CONSTRUCT_INSTRUCTIONS)
#         elif cmd == "\\":
#             break
#         else:
#             print("Invalid command. Type ! for instructions.")
