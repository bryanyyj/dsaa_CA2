# # Joel's updated contruct_panel.py 3.0
from trie.trie import Trie
from trie.trie_utils import load_keywords_from_file, write_keywords_to_file, write_keywords_from_trie

# trie = Trie()

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
                    word, freq_str = line.split(",", 1)
                    word = word.strip()
                    try:
                        frequency = int(freq_str.strip())
                        if word:
                            trie.insert(word, frequency)
                    except ValueError:
                        print(f"Warning: Invalid frequency for word '{word}': {freq_str}")
                        continue
        print(f"Successfully loaded stopwords from {filepath}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"Error loading stopwords: {e}")

def display_trie(trie):
    """Display the trie structure."""
    def _display_node(node, word):
        if node.is_terminal:
            print(f"Word: {word}, Frequency: {node.frequency}")
        for child in node.children.values():
            _display_node(child, word + child.char)

    print("Trie structure:")
    _display_node(trie.root, "")

def run_construct_panel(trie):
    print("=== Construct/Edit Trie ===")
    print(CONSTRUCT_MENU)
    while True:
        cmd = input("Command [+ - ? # @ ~ = ! \\]: ").strip()
        
        if cmd.startswith("+"):
            word_input = cmd[1:].strip()
            if ',' in word_input:
                # Handle +<word>,<frequency>
                word, freq_str = word_input.split(',', 1)
                word = word.strip()
                try:
                    freq = int(freq_str.strip())
                    trie.insert(word, freq)
                    print(f"Added: {word} with frequency {freq}")
                except ValueError:
                    print("⚠️ Invalid frequency. Example usage: +dog,999999999")
            else:
                # Handle +<word>
                word = word_input
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
            print("Trie Display:")
            display_trie(trie)
        
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

def write_trie_to_file(trie, filename):
    """Write trie structure to file - placeholder for now"""
    print(f"[Writing trie to {filename} - to be implemented]")
