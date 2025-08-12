# edited by claude
# Author: Bryan Yeo - Extra Feature 1: Typo Correction Suggestions
# features/bryan1.py

from trie.trie import Trie
from typing import List, Tuple

def levenshtein_distance(a: str, b: str) -> int:
    """Compute Levenshtein (edit) distance between strings a and b."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if i == 0:
                dp[i][j] = j  # insert all b's chars
            elif j == 0:
                dp[i][j] = i  # delete all a's chars
            elif a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],    # delete
                                   dp[i][j - 1],    # insert
                                   dp[i - 1][j - 1])  # replace
    return dp[-1][-1]

def suggest_corrections(word: str, keywords: List[str], max_distance: int = 2) -> List[Tuple[str, int]]:
    """Return list of (keyword, distance) pairs within max edit distance."""
    suggestions = []
    for kw in keywords:
        dist = levenshtein_distance(word.lower(), kw.lower())
        if dist <= max_distance:
            suggestions.append((kw, dist))
    return sorted(suggestions, key=lambda x: x[1])  # sort by closest match

def run_feature_bryan1(trie: Trie):
    print("\n=== Extra Feature 1: Typo Correction Suggestions ===")
    if trie is None or not trie.get_keywords():
        print("⚠️  The trie is empty. Please load or construct a trie first.")
        return

    while True:
        sentence = input("\nEnter a sentence (or '\\' to return to main menu): ").strip()
        if sentence == "\\":
            break

        words = sentence.split()
        keywords = trie.get_keywords()
        any_typos = False

        for word in words:
            clean_word = ''.join(filter(str.isalpha, word))  # remove punctuation
            if not clean_word:
                continue

            if trie.search(clean_word.lower()):
                continue  # word found, skip

            any_typos = True
            print(f"\n❌ '{clean_word}' not found in trie.")
            suggestions = suggest_corrections(clean_word, keywords)
            if suggestions:
                print("   🔍 Did you mean:")
                for s, d in suggestions[:3]:  # show top 3
                    print(f"     - {s} (edit distance {d})")
            else:
                print("   😕 No similar words found.")

        if not any_typos:
            print("✅ All words found in trie. Great job!")
