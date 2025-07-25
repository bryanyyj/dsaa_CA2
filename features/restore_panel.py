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

from features.construct_panel import load_stopwords_to_trie, display_trie
from trie.trie_utils import wildcard_match, restore_line_all_matches, restore_line_best_matches

def run_restore_panel(trie):
    print("=== Predict/Restore Text ===")
    print(RESTORE_MENU)
    while True:
        cmd = input("Command [~ # $ ? & @ ! \\]: ").strip()

        # Load stopwords into trie
        if cmd == "~":
            load_stopwords_to_trie(trie)
            print("Loaded stopwords from data/stopwordsFreq.txt into Trie.")

        # Display the trie structure
        elif cmd == "#":
            display_trie(trie)

        # List all possible matches for a wildcard pattern
        elif cmd.startswith("$"):
            pattern = cmd[1:].strip()
            if not pattern:
                print("Please provide a pattern after '$'.")
            else:
                matches = wildcard_match(trie, pattern)
                if matches:
                    print(f"Matches for '{pattern}':")
                    for word, freq in matches:
                        print(f"{word} (frequency: {freq})")
                else:
                    print(f"No matches found for '{pattern}'.")

        # Restore best match for a wildcard pattern
        elif cmd.startswith("?"):
            pattern = cmd[1:].strip()
            if not pattern:
                print("Please provide a pattern after '?'.")
            else:
                matches = wildcard_match(trie, pattern)
                if matches:
                    best_word, best_freq = matches[0]
                    print(f"Best match for '{pattern}' is: {best_word} (frequency: {best_freq})")
                else:
                    print(f"No matches found for '{pattern}'.")

        # Restore all matches for text from file (with wildcards)
        elif cmd.startswith("&"):
            filename = input("Enter text filename to restore: ").strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                for i, line in enumerate(lines, 1):
                    print(f"\nLine {i}: {line.strip()}")
                    restored_lines = restore_line_all_matches(line, trie)
                    print("Possible restorations:")
                    for restored in restored_lines:
                        print(restored)

            except FileNotFoundError:
                print(f"File {filename} not found.")
            except Exception as e:
                print(f"Error processing file: {e}")

        # Restore text using best matches (from file)
        elif cmd.startswith("@"):
            filename = input("Enter text filename to restore: ").strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                print("\nRestored text using best matches:")
                for i, line in enumerate(lines, 1):
                    restored_line = restore_line_best_matches(line, trie)
                    print(f"Line {i}: {restored_line}")

            except FileNotFoundError:
                print(f"File {filename} not found.")
            except Exception as e:
                print(f"Error processing file: {e}")

        # Display instructions
        elif cmd == "!":
            print(RESTORE_INSTRUCTIONS)

        # Exit the program
        elif cmd == "\\":
            break

        # Handle invalid command
        else:
            print("Invalid command. Type ! for instructions.")
