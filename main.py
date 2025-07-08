# Joel's directory: cd C:\Users\Joelc\OneDrive\Desktop\MAIN\SCHOOL\dsaa_CA2

from features.construct_panel import run_construct_panel
from features.restore_panel import run_restore_panel

def display_menu():
    print("""
==== Heatherthorn Post Restoration ====
Group: Bryan & Joel     Class: DAAA/01
1. Construct/Edit Trie
2. Predict/Restore Text
3. Extra Feature 1
4. Extra Feature 2
7. Exit
""")

def main():
    while True:
        display_menu()
        choice = input("Select an option: ")
        if choice == '1':
            run_construct_panel()
        elif choice == '2':
            run_restore_panel()
        elif choice == '3':
            print("Extra Feature 1")
        elif choice == '4':
            print("Extra Feature 2")
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid input. Please select again.")

if __name__ == "__main__":
    main()
