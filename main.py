"""
*********************************************************
* ST1507 DSAA: Predictive Text Editor (using tries)    *
*---------------------------------------------------------*
* Done by: Bryan Tan() & Joel Chua ()        *
* Class: DAAA/01                                      *
*********************************************************
"""

from features.joel2 import run_feature_joel2
from features.joel1 import run_joel1_feature
from features.construct_panel import run_construct_panel
from features.restore_panel import run_restore_panel
from features.bryan1 import run_feature_bryan1
from features.bryan2 import run_feature_bryan2
from trie.trie import Trie


def display_menu():
    print("""
==== Heatherthorn Post Restoration ====
Group: Bryan & Joel
Class: DAAA/01

1. Construct/Edit Trie
2. Predict/Restore Text
3. Extra Feature 1 (Bryan)
4. Extra Feature 2 (Bryan)
5. Extra Feature 3 (Joel - First/Last Word Auto-Complete)
6. Extra Feature 4 (Joel - Top N Frequent Words)
7. Exit
""")

def main():
    trie = Trie()
    while True:
        display_menu()
        choice = input("Enter choice: ")
        
        if choice == '1':
            run_construct_panel(trie)
        elif choice == '2':
            run_restore_panel(trie)
        elif choice == '3':
            run_feature_bryan1(trie)
        elif choice == '4':
            run_feature_bryan2(trie)
        elif choice == '5':
            run_joel1_feature(trie)
        elif choice == '6':
            run_feature_joel2(trie)
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
