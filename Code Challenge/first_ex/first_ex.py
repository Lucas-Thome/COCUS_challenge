import sys
import os

def find_files_with_suffix(suffix, path):
    matched_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(suffix):
                matched_files.append(os.path.join(root, file).replace(os.sep, '/'))
    
    return matched_files

def main():
    if len(sys.argv) != 3:
        print("Usage: python yourScript.py <suffix> <'path'>")
        sys.exit(1)

    suffix = sys.argv[1]
    path = sys.argv[2]

    if not os.path.exists(path):
        print(f"Invalid path: '{path}'. Please provide the entire path.")
        sys.exit(1)

    matched_files = find_files_with_suffix(suffix, path)

    if matched_files:
        print("\nMatching files:\n")
        for file in matched_files:
            print(file)
        print('\n')
    else:
        print("No matching files found.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error ocurred.\n Error message => {e}")

