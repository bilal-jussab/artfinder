# Tech Test for Artfinder
# Author: Bilal Jussab
# Date: 24 - 04 - 2024
#
# This Python script reads all text files in a specified directory, creates an
# in-memory index of the files and their contents, and provides an interactive
# search prompt. The user can input search queries, and the script will return
# the filenames with the highest matching scores based on the query. The search
# results display the filenames along with their corresponding match scores.
#
# The user can continue searching or exit the interactive search prompt by
# typing :quit.

import os
import sys
import re

def read_files(directory):
    """
    Read all text files in the specified directory and return their contents.
    Args: directory (str): The path to the directory containing text files.
    Returns: list: A list of tuples containing filename and content pairs.
    """
    files = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as f:
                    content = f.read()
                    files.append((filename, content))
    except FileNotFoundError:
        print("Directory not found.")
    return files

def build_index(files):
    """
    Build an index of words and the filenames they are in.
    Args: files (list): A list of tuples containing filename and content pairs.
    Returns: dict: A dictionary where keys are words and values are lists of filenames.
    """
    index = {}
    for filename, content in files:
        for word in re.findall(r'\w+', content.lower()):
            if word not in index:
                index[word] = []
            index[word].append(filename)
    return index

def search(index, query):
    """
    Search the index for filenames containing the query words.
    Args:
    index (dict): The index of words and filenames.
    query (str): The search query.
    Returns: list: A list of tuples containing filename and score pairs, sorted by score.
    """
    query_words = query.lower().split()
    scores = {}
    file_scores = {}
    total_words = len(query_words)

    for word in query_words:
        if word in index:
            for filename in index[word]:
                if filename not in file_scores:
                    file_scores[filename] = 0
                file_scores[filename] += 1

    for filename, count in file_scores.items():
        score = round((count / total_words) * 100, 2)
        scores[filename] = score

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:10]

def main():
    """
    Main function to execute the text search engine.
    """
    if len(sys.argv) != 2:
        print("Usage: python <filename> <pathToDirectoryContainingTextFiles>")
        return

    directory = sys.argv[1]
    files = read_files(directory)
    print(f"{len(files)} files read in directory {directory}")

    while True:
        query = input("search> ")
        if query == ":quit":
            break

        results = search(build_index(files), query)

        if results:
            for filename, score in results:
                print(f"{filename} : {score}%")
        else:
            print("no matches found")

if __name__ == "__main__":
    main()