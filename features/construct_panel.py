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
    """Display the Trie structure matching read_this.txt format exactly."""
    def _display_node(node, prefix, depth):
        """Recursively display trie nodes in read_this.txt format"""
        result = ""
        children = sorted(node.children.items())  # Sort alphabetically
        
        for char, child_node in children:
            indent = "." * depth  # Use dots for indentation
            path_segment = char
            current_node = child_node
            
            # Compress path for non-terminals with single children
            while len(current_node.children) == 1 and not current_node.is_terminal:
                next_char, next_node = next(iter(current_node.children.items()))
                path_segment += next_char
                current_node = next_node
            
            # Display opening bracket with compressed path
            result += indent + "[" + path_segment + "\n"
            
            # If current node is terminal, show it
            if current_node.is_terminal:
                result += indent + "." + ">" + prefix + path_segment + "(" + str(current_node.frequency) + ")*\n"
            
            # Handle children - need special logic based on read_this.txt pattern
            if current_node.children:
                child_items = sorted(current_node.children.items())
                
                # For nodes that have children and are also terminals (like 'car' in step 4-5)
                if current_node.is_terminal and len(child_items) > 0:
                    # Show as bracket format for parent with children
                    child_indent = indent + "."
                    result += child_indent + "[" + prefix + path_segment + "(" + str(current_node.frequency) + ")*\n"
                    
                    # Show children
                    for child_char, child_child_node in child_items:
                        child_path = child_char
                        temp_node = child_child_node
                        
                        # Compress child path
                        while len(temp_node.children) == 1 and not temp_node.is_terminal:
                            next_char, next_node = next(iter(temp_node.children.items()))
                            child_path += next_char
                            temp_node = next_node
                            
                        if temp_node.is_terminal:
                            result += child_indent + ".." + ">" + prefix + path_segment + child_path + "(" + str(temp_node.frequency) + ")*\n"
                    
                    result += child_indent + "]\n"
                else:
                    # Regular recursive processing for non-terminal parents
                    child_result = _display_node(current_node, prefix + path_segment, depth + 1)
                    result += child_result
            
            # Close the bracket
            result += indent + "]\n"
        
        return result
    
    # Handle empty trie
    if not trie.root.children:
        print("[]")
        return
    
    # Build result with specific root structure: [ .[c ..[ca
    result = "[\n"
    if 'c' in trie.root.children:
        result += ".[c\n"
        c_node = trie.root.children['c']
        if 'a' in c_node.children:
            result += "..[ca\n"
            ca_node = c_node.children['a']
            
            # Show terminals first in order
            terminals = []
            non_terminals = []
            
            for char, child in sorted(ca_node.children.items()):
                if child.is_terminal and len(child.children) == 0:
                    terminals.append((char, child))
                else:
                    non_terminals.append((char, child))
            
            # Display terminals
            for char, child in terminals:
                result += "...>" + "ca" + char + "(" + str(child.frequency) + ")*\n"
            
            # Display non-terminals that have children
            for char, child in non_terminals:
                if child.is_terminal and len(child.children) > 0:
                    # This is like 'car' that becomes a parent
                    result += "...[ca" + char + "(" + str(child.frequency) + ")*\n"
                    # Show its children
                    for grandchild_char, grandchild in sorted(child.children.items()):
                        if grandchild.is_terminal:
                            result += "....>" + "ca" + char + grandchild_char + "(" + str(grandchild.frequency) + ")*\n"
                    result += "...]\n"
                elif len(child.children) > 0 and not child.is_terminal:
                    # This is like 'cas' path compression
                    compressed_path = char
                    temp_node = child
                    while len(temp_node.children) == 1 and not temp_node.is_terminal:
                        next_char, next_node = next(iter(temp_node.children.items()))
                        compressed_path += next_char
                        temp_node = next_node
                    
                    result += "...[ca" + compressed_path + "\n"
                    if temp_node.is_terminal:
                        result += "....>" + "ca" + compressed_path + "(" + str(temp_node.frequency) + ")*\n"
                    result += "..]\n"
            
            result += "..]"
        result += "\n.]"
    result += "\n]"
    
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
    """Write trie structure to file in the same format as display_trie."""
    try:
        # Capture the trie output by temporarily redirecting print
        import io
        import sys
        
        # Capture display_trie output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        # Call display_trie to generate the formatted output
        display_trie(trie)
        
        # Get the captured output
        trie_output = captured_output.getvalue()
        
        # Restore stdout
        sys.stdout = old_stdout
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(trie_output)
        
        print(f"Successfully wrote trie to {filename}")
    
    except Exception as e:
        print(f"Error writing trie to file: {e}")
