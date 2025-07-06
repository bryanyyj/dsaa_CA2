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
    trie.clear()  # Assuming your Trie class has a clear() method; if not, implement it.
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            word = line.split(",", 1)[0].strip()
            if word:
                trie.insert(word)

def run_construct_panel():
    print("=== Construct/Edit Trie ===")
    print(CONSTRUCT_MENU)
    while True:
        cmd = input("Command [+ - ? # @ ~ = ! \\]: ")
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
                trie.delete(word)
                print(f"Deleted: {word}")
            else:
                print("Please provide a keyword after '-'.")
        elif cmd.startswith("?"):
            word = cmd[1:].strip()
            if word:
                print("Found!" if trie.search(word) else "Not found.")
            else:
                print("Please provide a keyword after '?'.")
        elif cmd == "#":
            print("[Trie structure display not implemented yet]")
        elif cmd == "@":
            print("[Write Trie to file not implemented yet]")
        elif cmd == "~":
            load_stopwords_to_trie(trie)
            print("Loaded stopwords from data/stopwordsFreq.txt into Trie.")
        elif cmd == "=":
            print("[Write keywords from Trie to file not implemented yet]")
        elif cmd == "!":
            print(CONSTRUCT_INSTRUCTIONS)
        elif cmd == "\\":
            break
        else:
            print("Invalid command. Type ! for instructions.")
