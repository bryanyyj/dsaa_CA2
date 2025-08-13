# edited by claude
# Author: Bryan Yeo & Joel Chua  
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
            filename = input("Please enter input file: ").strip()
            if not filename:
                filename = "data/stopwordsFreq.txt"  # Default filename
            load_stopwords_to_trie(trie, filename)

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
                print(f'Restored keyword "{best_word}"')
            else:
                print(f"😕 No matches found for '{pattern}'.")

        # Restore all matches for text from a file, considering wildcards
        elif cmd.startswith("&"):
            filename = input("Enter text filename to restore: ").strip()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                # Process each line and restore possible matches
                restored_content = []
                for line in lines:
                    restored_line = restore_line_all_matches(line, trie)
                    restored_content.append(restored_line)
                    print(restored_line)

                # Ask if user wants to save the restored content
                save_choice = input("Please enter output file (or press Enter to skip): ").strip()
                if save_choice:
                    try:
                        with open(save_choice, "w", encoding="utf-8") as f:
                            for line in restored_content:
                                f.write(line + "\n")
                        print(f"Restored text saved to {save_choice}")
                    except Exception as e:
                        print(f"⚠️ Error saving file: {e}")
                else:
                    print("File not saved.")

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

                # Process and display restored content
                restored_content = []
                for line in lines:
                    restored_line = restore_line_best_matches(line, trie)
                    restored_content.append(restored_line)
                    print(restored_line)

                # Ask if user wants to save the restored content
                save_choice = input("Please enter output file (or press Enter to skip): ").strip()
                if save_choice:
                    try:
                        with open(save_choice, "w", encoding="utf-8") as f:
                            for line in restored_content:
                                f.write(line + "\n")
                        print(f"Restored text saved to {save_choice}")
                    except Exception as e:
                        print(f"⚠️ Error saving file: {e}")
                else:
                    print("File not saved.")

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
