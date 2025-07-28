# LATEST EDITED: 28/07/2025

# Predict/Restore Text Command Menu
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

# Instructions for the Predict/Restore Text Commands
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

# Import necessary modules
from features.construct_panel import load_stopwords_to_trie, display_trie
from trie.trie_utils import wildcard_match, restore_line_all_matches, restore_line_best_matches

def run_restore_panel(trie):
    """
    This function handles the restoration of words or text from a file based on wildcards and frequencies.
    The user interacts through the terminal with different commands to restore words or display the Trie.
    """
    print("=== Predict/Restore Text ===")
    print(RESTORE_MENU)
    
    while True:
        cmd = input("Command [~ # $ ? & @ ! \\]: ").strip()

        # Load stopwords into the Trie from a file
        if cmd == "~":
            load_stopwords_to_trie(trie)
            print("Loaded stopwords from data/stopwordsFreq.txt into Trie.")

        # Display the current Trie structure
        elif cmd == "#":
            display_trie(trie)

        # List all possible matching keywords based on wildcard pattern
        elif cmd.startswith("$"):
            pattern = cmd[1:].strip()
            if not pattern:
                print("⚠️ Please provide a pattern after '$'.")
                continue  # Prompt for valid pattern if empty
            matches = wildcard_match(trie, pattern)
            if matches:
                print(f"Matches for '{pattern}':")
                for word, freq in matches:
                    print(f"{word} (frequency: {freq})")
            else:
                print(f"😕 No matches found for '{pattern}'.")

        # Restore the best match for a word with wildcards
        elif cmd.startswith("?"):
            pattern = cmd[1:].strip()
            if not pattern:
                print("⚠️ Please provide a pattern after '?'.")
                continue  # Prompt for valid pattern if empty
            matches = wildcard_match(trie, pattern)
            if matches:
                best_word, best_freq = matches[0]  # Best match is the first match
                print(f"Best match for '{pattern}' is: {best_word} (frequency: {best_freq})")
            else:
                print(f"😕 No matches found for '{pattern}'.")

        # Restore all matches for text from a file, considering wildcards
        elif cmd.startswith("&"):
            filename = input("Enter text filename to restore: ").strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                # Process each line and restore possible matches
                for i, line in enumerate(lines, 1):
                    print(f"\nLine {i}: {line.strip()}")
                    restored_lines = restore_line_all_matches(line, trie)
                    print("Possible restorations:")
                    for restored in restored_lines:
                        print(restored)

            except FileNotFoundError:
                print(f"⚠️ File {filename} not found.")
            except Exception as e:
                print(f"⚠️ Error processing file: {e}")

        # Restore text using the best matches from a file
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
                print(f"⚠️ File {filename} not found.")
            except Exception as e:
                print(f"⚠️ Error processing file: {e}")

        # Display the instructions for all available commands
        elif cmd == "!":
            print(RESTORE_INSTRUCTIONS)

        # Exit the command prompt and return to the main menu
        elif cmd == "\\":
            break

        # Handle invalid commands
        else:
            print("⚠️ Invalid command. Type ! for instructions.")
