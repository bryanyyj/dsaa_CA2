def load_keywords_from_file(filepath):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def write_keywords_to_file(filepath, keywords):
    with open(filepath, 'w') as f:
        for word in keywords:
            f.write(f"{word}\n")
