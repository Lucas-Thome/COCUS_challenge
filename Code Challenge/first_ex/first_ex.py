import sys
import os

def find_files_with_suffix(suffix, path):
    matched_files = []
    # List all files and directories in the current path
    items = os.listdir(path)
    for item in items:
        # Get the full path of the item
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and item.endswith(suffix):
            # If the item is a file and its name ends with the specified suffix, add it to the list
            matched_files.append(item_path.replace(os.sep, '/'))
        elif os.path.isdir(item_path):
            # If the item is a path call the function recursively and append the results to the current list.
            matched_files += find_files_with_suffix(suffix, item_path)

    return matched_files

def main():
    if len(sys.argv) != 3:
        print("Usage: python yourScript.py <suffix> <'path'>")
        sys.exit(1)

    suffix = sys.argv[1]
    path = sys.argv[2]

    # Validade Suffix
    suffix = suffix.split('.')[-1]
    if suffix == '':
        print('Please, provide a valid suffix.')
        sys.exit(1)

    # validate Path
    if not os.path.exists(path):
        print(f"Invalid path: '{path}'. Please, make sure the entire path is provided.")
        sys.exit(1)

    matched_files = find_files_with_suffix(suffix, path)

    if matched_files:
        print("\nMatching files:\n")
        for file in matched_files:
            print(file)
        print('\n')
    else:
        print(f"No matching files found with the suffix {suffix}.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error ocurred.\n Error message => {e}")

