# edited by claude  
# Author: Bryan Yeo & Joel Chua
# LATEST EDITED: 28/07/2025
from trie.trie import Trie
from trie.trie_utils import load_keywords_from_file, write_keywords_to_file, write_keywords_from_trie

# Construct/Edit Trie Command Menu
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

# Construct/Edit Trie Command Instructions
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

# Function to load stopwords with their frequencies from file and populate the Trie
def load_stopwords_to_trie(trie, filepath="data/stopwordsFreq.txt"):
    """Load stopwords with their frequencies from file and insert them into the trie."""
    trie.clear()  # Clear the existing Trie data
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and ',' in line:  # Ensure line is not empty and contains a comma
                    word, freq_str = line.split(",", 1)
                    word = word.strip()
                    try:
                        frequency = int(freq_str.strip())
                        if word:
                            trie.insert(word, frequency)  # Insert word with frequency
                    except ValueError:
                        print(f"Warning: Invalid frequency for word '{word}': {freq_str}")
                        continue
        print(f"Successfully loaded stopwords from {filepath}")
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    except Exception as e:
        print(f"Error loading stopwords: {e}")

# Function to display the Trie structure in the exact format specified in Appendix A  
def display_trie(trie):
    """Display the Trie structure matching Appendix A format exactly."""
    def _display_node(node, current_path, indent_level):
        """Recursively build the trie display string"""
        result = ""
        children = sorted(node.children.items())  # Sort children alphabetically
        
        for char, child_node in children:
            new_path = current_path + char
            dots = ".." * indent_level
            
            # Add the character bracket
            result += dots + "[" + char + "\n"
            
            # Simple logic: compress only single non-terminal chains
            current_node = child_node
            compressed_path = new_path
            
            # Compress consecutive single non-terminal children
            while (len(current_node.children) == 1 and not current_node.is_terminal):
                next_char, next_node = next(iter(current_node.children.items()))
                compressed_path += next_char
                current_node = next_node
            
            # Show compressed path if we compressed anything
            if len(compressed_path) > len(new_path):
                result += dots + ".." + "[" + compressed_path + "\n"
                
                # Show terminal word if current node is terminal
                if current_node.is_terminal:
                    result += dots + "..." + ">" + compressed_path + f"({current_node.frequency})*" + "\n"
                
                # Process any children recursively
                if current_node.children:
                    child_result = _display_node(current_node, compressed_path, indent_level + 2)
                    result += child_result
                
                result += dots + ".." + "]" + "\n"
            else:
                # No compression - handle current node
                if current_node.is_terminal:
                    result += dots + ".." + ">" + new_path + f"({current_node.frequency})*" + "\n"
                
                # Process children
                if current_node.children:
                    child_result = _display_node(current_node, new_path, indent_level + 1)
                    result += child_result
            
            result += dots + "]" + "\n"
        
        return result
    
    # Handle empty trie case
    if not trie.root.children:
        print("[]")
        return
    
    # Build result matching Appendix A format exactly
    result = "["
    root_content = _display_node(trie.root, "", 0)
    result += root_content.rstrip() + "\n]"
    
    print(result)

# Function to handle all user commands in the construct/edit Trie panel
def run_construct_panel(trie):
    """Start the Construct/Edit Trie panel where users can add, delete, and search words in the trie."""
    print("=== Construct/Edit Trie ===")
    print(CONSTRUCT_MENU)
    
    while True:
        cmd = input("Command [+ - ? # @ ~ = ! \\]: ").strip()
        
        # Handle the "+<word>,<frequency>" or "+<word>" command to add keywords
        if cmd.startswith("+"):
            word_input = cmd[1:].strip()
            if ',' in word_input:
                # Handle case for +<word>,<frequency>
                word, freq_str = word_input.split(',', 1)
                word = word.strip()
                try:
                    freq = int(freq_str.strip())
                    if freq <= 0:
                        print("⚠️ Frequency must be a positive number.")
                        continue
                    trie.insert(word, freq)  # Insert word with given frequency
                    print(f"Added: {word} with frequency {freq}")
                except ValueError:
                    print("⚠️ Invalid frequency. Example usage: +dog,999999999")
            else:
                # Handle case for just +<word> without frequency
                word = word_input
                if word:
                    trie.insert(word)  # Default frequency 1
                    print(f"Added: {word}")
                else:
                    print("⚠️ Invalid command. Example usage: +dog or +dog,10")
        
        # Handle the "-<word>" command to delete keywords
        elif cmd.startswith("-"):
            word = cmd[1:].strip()
            if word:
                if trie.search(word):
                    trie.delete(word)  # Delete word from Trie
                    print(f"Deleted: {word}")
                else:
                    print("Is not a keyword in trie")
            else:
                print("⚠️ Please provide a keyword after '-'.")
        
        # Handle the "?<word>" command to find keywords
        elif cmd.startswith("?"):
            word = cmd[1:].strip()
            if word:
                if trie.search(word):
                    print(f'Keyword "{word}" is present')
                else:
                    print(f'Keyword "{word}" is not present')
            else:
                print("⚠️ Please provide a keyword after '?'.")
        
        # Handle the "#" command to display the Trie structure
        elif cmd == "#":
            print("Trie Display:")
            display_trie(trie)
        
        # Handle the "@" command to write the Trie to a file
        elif cmd == "@":
            filename = input("Enter filename to write trie to: ").strip()
            if filename:
                write_trie_to_file(trie, filename)  # Save Trie to file
            else:
                print("⚠️ Please provide a filename.")
        
        # Handle the "~" command to load keywords from a file
        elif cmd == "~":
            filename = input("Enter filename to read keywords from (or press Enter for default): ").strip()
            if not filename:
                filename = "data/stopwordsFreq.txt"  # Default filename
            load_stopwords_to_trie(trie, filename)
        
        # Handle the "=" command to write keywords from Trie to a file
        elif cmd == "=":
            filename = input("Enter filename to write keywords to: ").strip()
            if filename:
                write_keywords_from_trie(trie, filename)
            else:
                print("⚠️ Please provide a filename.")
        
        # Handle the "!" command to print the instructions
        elif cmd == "!":
            print(CONSTRUCT_INSTRUCTIONS)
        
        # Handle the "\\" command to exit the construct/edit trie panel
        elif cmd == "\\":
            break
        
        # Handle invalid commands
        else:
            print("⚠️ Invalid command. Type ! for instructions.")

# Function to write the trie structure to a file (currently just a placeholder)
def write_trie_to_file(trie, filename):
    """Write trie structure to file (placeholder)."""
    print(f"[Writing trie to {filename} - to be implemented]")
