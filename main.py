"""
*********************************************************
* ST1507 DSAA: Predictive Text Editor (using tries)    *
*---------------------------------------------------------*
* Done by: Bryan Tan() & Joel Chua ()        *
* Class: DAAA/01                                      *
*********************************************************
"""

from features.construct_panel import run_construct_panel
from features.restore_panel import run_restore_panel # new
from trie.trie import Trie

def display_menu():
    """
    Please select your choice ('1','2','3','4','5','6','7'):
    1. Construct/Edit Trie
    2. Predict/Restore Text
    =======================================================
    3. Extra Feature One (Bryan):
    4. Extra Feature Two (Bryan):
    =======================================================
    5. Extra Feature One (Joel):
    6. Extra Feature Two (Joel):
    =======================================================
    7. Exit
    """
    print("""
==== Heatherthorn Post Restoration ====
Group: Bryan & Joel
Class: DAAA/01

1. Construct/Edit Trie
2. Predict/Restore Text
3. Extra Feature 1 (Bryan)
4. Extra Feature 2 (Bryan)
5. Extra Feature 3 (Joel)
6. Extra Feature 4 (Joel)
7. Exit
""")

def main():
    # new 
    trie = Trie()
    while True:
        display_menu()
        choice = input("Enter choice: ")
        
        if choice == '1':
            run_construct_panel(trie)
        elif choice == '2':
            run_restore_panel(trie)
        elif choice == '3':
            print("Extra Feature 1")
        elif choice == '4':
            print("Extra Feature 2")
        elif choice == '5':
            print("Extra Feature 3")
        elif choice == '6':
            print("Extra Feature 4")
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid input. Please select again.")

if __name__ == "__main__":
    main()

# # Joel's directory: cd C:\Users\Joelc\OneDrive\Desktop\MAIN\SCHOOL\dsaa_CA2

# from features.construct_panel import run_construct_panel
# from features.restore_panel import run_restore_panel
# # new
# from trie.trie import Trie

# def display_menu():
#     print("""
# ==== Heatherthorn Post Restoration ====
# Group: Bryan & Joel     Class: DAAA/01

# 1. Construct/Edit Trie
# 2. Predict/Restore Text
# 3. Extra Feature 1 (Bryan)
# 4. Extra Feature 2 (Bryan)
# 5. Extra Feature 3 (Joel)
# 6. Extra Feature 4 (Joel)
# 7. Exit
# """)

# def main():
#     # new 
#     trie = Trie()
#     while True:
#         display_menu()
#         choice = input("Select an option: ")
#         if choice == '1':
#             run_construct_panel(trie)
#         elif choice == '2':
#             run_restore_panel(trie)
#         elif choice == '3':
#             print("Extra Feature 1")
#         elif choice == '4':
#             print("Extra Feature 2")
#         elif choice == '7':
#             print("Exiting...")
#             break
#         else:
#             print("Invalid input. Please select again.")

# if __name__ == "__main__":
#     main()
