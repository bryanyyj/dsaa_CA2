RESTORE_MENU = '''
------------------------------------------------------------
Predict/Restore Text Commands:
'~', '#', '$', '?', '&', '@', '!', '\\'
------------------------------------------------------------
~            (read keywords from file to make Trie)
#            (display Trie)
$            (list all possible matching keywords)
?            (restore a word using best keyword match)
&            (restore a text using all matching keywords)
@            (restore a text using best keyword matches)
!            (print instructions)
\\           (exit)
------------------------------------------------------------
'''

RESTORE_INSTRUCTIONS = '''
Predict/Restore Text Commands:
~   Reads keywords from a file to make a new prefix trie (take note, thereby it clears the current prefix trie).
#   Displays the current prefix trie on the screen.
$   Lists all possible matching keywords.
?   Restores a word using the best keyword match as based on word frequencies.
&   Restores a text using all matching keywords.
@   Restores a text using the best keyword matches as based on word frequencies.
!   Prints the instruction for the various Predict/Restore Text Commands.
\\  Exits the Command Prompt and returns to the main menu.
'''

from features.construct_panel import load_stopwords_to_trie
from trie.trie import Trie

trie = Trie()  # Shared trie instance for restore panel

def run_restore_panel():
    print("=== Predict/Restore Text ===")
    print(RESTORE_MENU)
    while True:
        cmd = input("Command [~ # $ ? & @ ! \\]: ")
        if cmd == "~":
            load_stopwords_to_trie(trie)
            print("Loaded stopwords from data/stopwordsFreq.txt into Trie.")
        elif cmd == "#":
            print("[Display Trie not implemented yet]")
        elif cmd == "$":
            print("[List all possible matching keywords not implemented yet]")
        elif cmd == "?":
            print("[Restore a word using best keyword match not implemented yet]")
        elif cmd == "&":
            print("[Restore a text using all matching keywords not implemented yet]")
        elif cmd == "@":
            print("[Restore a text using best keyword matches not implemented yet]")
        elif cmd == "!":
            print(RESTORE_INSTRUCTIONS)
        elif cmd == "\\":
            break
        else:
            print("Invalid command. Type ! for instructions.")
