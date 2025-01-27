import argparse
import re

import colorama


# PATTERNS:
# Pattern to match a datetime in the format: DD-MM-YYYY HH:MM:SS.
DATETIME_PATTERN = r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}'
# Pattern to match a filename with an optional version and file extension.
NAME_PATTERN = r'^([a-zA-Z0-9_-]+)(?:[^a-zA-Z0-9]*([\d\.]+))?\.(\w+)$'


def parse_arguments():
    """
    Parses two positional command-line arguments: 'file1' and 'file2'.
    Returns the values of these arguments as a tuple.

    Args:
        None

    Returns:
        tuple: A tuple containing two elements
            - file1 (str): The first file path or name provided by the user.
            - file2 (str): The second file path or name provided by the user.

    Raises:
        SystemExit: If the user does not provide the required arguments,
        argparse will raise an error and the program will exit.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('file1')
    parser.add_argument('file2')

    args = parser.parse_args()
    return (args.file1, args.file2)


def read_file(path):
    """
    Opens and reads the file specified by the given 'path', processes its contents, 
    and returns both the original and normalized content.

    Args:
        path (str): The file path to be opened and read.

    Returns:
        tuple: A tuple containing two elements:
            - content (list): The original content of the file as a list of lines (str).
            - normalized_content (list): The normalized version of the content after processing.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
        PermissionError: If there are insufficient permissions to open the file.
        Exception: If any other error occurs while opening or reading the file.
    """
    try:
        with open(path, "r") as file:
            content = file.readlines()

        name, version = get_name_ver(path)
        normalized_content = normalize(content, name, version)
        return (content, normalized_content)
    except FileNotFoundError:
        print(f"Ошибка: файл '{path}' не найден.")
    except PermissionError:
        print("У вас нет прав для открытия файла.")
    except Exception as e:
        print(f"При открытии файла произошла ошибка: {e}")
    exit(1)


def get_name_ver(path):
    """
    Extracts the name and version from a file path based on the file's name.

    Args:
        path (str): The file path from which to extract the name and version.

    Returns:
        tuple: A tuple containing two elements:
            - name (str): The name of the file (without the version and extension).
            - version (str): The version of the file, or an empty string if no version is found.
        
        If the file name does not match the expected pattern, the function returns:
            - (None, None)
    """
    match = re.search(r'[^\\/]+$', path)
    filename = match.group(0)

    match = re.match(NAME_PATTERN, filename)
    if match:
        name = match.group(1)
        version = match.group(2) if match.group(2) else ''
        extension = match.group(3)
        return name, version
    else:
        return None, None


def remove_name_ver(line, name, version):
    """
    Removes the specified file name and version from the given line of text.

    Args:
        line (str): The line of text from which the name and version will be removed.
        name (str): The file name to be removed from the line.
        version (str): The file version to be removed from the line.

    Returns:
        str: A new line with the name and version removed.

    Raises:
        SystemExit: If either `name` or `version` is `None`, 
        the function prints an error message and terminates the program
        with exit code 1.
    """
    if name is None or version is None:
        print("Не удалось распарсить имя файла")
        exit(1)

    return line.replace(name, '').replace(version, '')


def normalize(content, name, version):
    """
    Normalizes the given content by removing datetime, paths, and file name/version.

    Args:
        content (list): A list of strings representing the content to be normalized.
        name (str): The file name to be removed from each line.
        version (str): The file version to be removed from each line.

    Returns:
        list: A list of normalized strings where datetime, paths, 
        and the file name/version have been removed from each line.
    """
    norm_content = []
    for line in content:
        # Remove datetime from the line
        rem_date = re.sub(DATETIME_PATTERN, '', line)
        # Pattern matching a path ending with the target file name.
        PATH_PATTERN = rf'\S+[\\/]+{re.escape(name)}[\\/]*'
        # Remove paths
        rem_paths = re.sub(PATH_PATTERN, '', rem_date)
        # delete name and version
        norm_line = remove_name_ver(rem_paths, name, version)
        # add to norm_line list
        norm_content.append(norm_line)
    return norm_content


def calc_lcs_matr(file1, file2):
    """
    Calculate the Longest Common Subsequence (LCS) matrix of two input lists of strings.

    Args:
        file1 (list of str): The first list of strings (e.g., lines from a file).
        file2 (list of str): The second list of strings (e.g., lines from a file).

    Returns:
        list: A 2D list (matrix) of size (len(file1) + 1) x (len(file2) + 1),
        where each element represents the length of the longest common subsequence 
        for the f the string lists file1 and file2
        from this point to the end of the lists.

    Example:
        >>> calc_lcs_matr(["hello", "big", "world"], ["hello", "world", "Python"])
        [[2, 1, 0, 0], 
         [1, 1, 0, 0], 
         [1, 1, 0, 0], 
         [0, 0, 0, 0]]
    """
    f1_len = len(file1)
    f2_len = len(file2)

    L = [[0 for _ in range(f2_len + 1)] for _ in range(f1_len + 1)]

    for i in range(f1_len - 1, -1, -1):
        for j in range(f2_len - 1, -1, -1):
            if file1[i] == file2[j]:
                L[i][j] = L[i + 1][j + 1] + 1
            else:
                L[i][j] = max(L[i + 1][j], L[i][j + 1])
    print(L)
    return L


def print_in_red(line):
    """
    Prints the given line of text in red color using colorama.

    Args:
        line (str): The text line to be printed in red.
    """
    print(colorama.Fore.RED + line, end = '')


def print_in_green(line):
    """
    Prints the given line of text in green color using colorama.

    Args:
        line (str): The text line to be printed in green.
    """
    print(colorama.Fore.GREEN + line, end = '')


def print_chunk(i, j, d, a, file1, file2):
    """
    Prints one fragment of the difference between two files, 
    such as added, deleted, changed.

    Args:
        i (int): The starting index in `file1` to print.
        j (int): The starting index in `file2` to print.
        d (int): The number of lines removed from `file1`.
        a (int): The number of lines added in `file2`.
        file1 (list of str): The first file content represented as a list of strings (lines).
        file2 (list of str): The second file content represented as a list of strings (lines).

    Example:
        >>> print_chunk(2, 2, 1, 3, ["Line1\n", "Line2\n", "Line3\n"], 
                        ["Line1\n", "Line2\n", "Line4\n", "Line5\n", "Line6\n"])
        3c3,5
        < Line3
        ---
        > Line4
        > Line5
        > Line6
    """

    # Helper function to return string with either one number or two separated by comma.
    # If the two numbers are equal, return just one, otherwise return both separated by a comma.
    two_nums = lambda a, b: "%d,%d" %(a, b) if a != b else "%d" %a

    if a and d:
        print(f"{two_nums(i + 1, i + d)}c{two_nums(j + 1, j + a)}")
    elif a:
        print(f"{i}a{two_nums(j + 1, j + a)}")
    elif d:
        print(f"{two_nums(i + 1, i + d)}d{j + a}")

    # Print the deleted lines (from file1) in red.
    for k in range(i, i + d):
        print_in_red(f"< {file1[k]}")

    # If both additions and deletions exist, print a separator line.
    if a and d:
        print("---")

    # Print the added lines (from file2) in green.
    for k in range(j, j + a):
        print_in_green(f"> {file2[k]}")


def find_chunks_by_matr(file1, file2, matr):
    """
    Finds and prints chunks of changes between two files based on the LCS matrix.

    Args:
        file1 (list of str): The first file's content, represented as a list of strings (lines).
        file2 (list of str): The second file's content, represented as a list of strings (lines).
        matr (list of list of int): The LCS matrix, which is a 2D list that holds the LCS length
        for every pair of suffixes from `file1` and `file2`.

    Returns:
        bool: Returns `True` if no changes (added or deleted) are detected between the files, 
        `False` otherwise.

    """
    no_diff = True
    i, j = 0, 0
    # Counters for added and deleted lines
    a, d = 0, 0 
    
    while i + d < len(file1) and j + a < len(file2):
        # Case when lines have changed (i.e., the LCS value is equal in adjacent cells)
        if matr[i + d][j + a] == matr[i + d + 1][j + a] and \
                matr[i + d][j + a] == matr[i + d][j + a + 1]:
            if matr[i + d][j + a] == matr[i + d + 1][j + a + 1]:
                a += 1
            d += 1
        # Case when there is a deletion (lines in file1 are missing in file2)
        elif matr[i + d][j + a] == matr[i + d + 1][j + a]:
            d += 1
        # Case when there is an addition (lines in file2 are new)
        elif matr[i + d][j + a] == matr[i + d][j + a + 1]:
            a += 1
        # Chunk has ended
        else:
            print_chunk(i, j, d, a, file1, file2)

            no_diff = no_diff and (not a) and (not d)
            i += d + 1
            j += a + 1
            a, d = 0, 0

    # Process remaining lines in file1 (if any)
    if i + d < len(file1):
        d = len(file1) - i 
    # Process remaining lines in file2 (if any)
    if j + a < len(file2):
        a = len(file2) - j

    # print the final chunk of difference between files
    print_chunk(i, j, d, a, file1, file2)

    # Return True if no differences (additions or deletions) were found, otherwise False
    return no_diff and (not a) and (not d)


def diff(file1_path, file2_path):
    """
    Compares two files and prints the differences between them, ignoring build time and location.

    This function reads the contents of two files specified by the paths `file1_path` and `file2_path`,
    normalizes them (removing timestamps and file paths), and calculates their longest common subsequence 
    (LCS) matrix. It then identifies and prints chunks of differences between the files.

    If the files are identical (after normalization), the function prints a message saying that the files 
    are identical without considering build time and location. If the files are not identical, it displays 
    the chunks of differences between them.

    Args:
        file1_path (str): The path to the first file to be compared.
        file2_path (str): The path to the second file to be compared.
    """
    f1_content, norm_f1 = read_file(file1_path)
    f2_content, norm_f2 = read_file(file2_path)
    if f1_content == f2_content:
        print("Файлы идентичны, различий нет.")
        exit()

    # Calculate the longest common subsequence (LCS) matrix.
    lcs_matr = calc_lcs_matr(norm_f1, norm_f2)
    
    # Find and print the differences between the files.
    no_diff = find_chunks_by_matr(f1_content, f2_content, lcs_matr)

    if no_diff:
        print("Файлы идентичны без учета времени и места сборки")


def main():
    colorama.init(autoreset=True)

    # Parse command line arguments for file paths.
    file1_path, file2_path = parse_arguments()

    # Compare the two files and display the result.
    diff(file1_path, file2_path)


if __name__ == '__main__':
    main()