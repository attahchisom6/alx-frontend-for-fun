#!/bin/python3

import re

def list_parser(A):
    """
    parse a list into items with diverse properties and return a tuple of them
    """
    isolated_items = []
    non_isolated_groups = []

    # Join the list into a single string for regex processing
    joined_text = "\n".join(A)

    # Split based on empty lines
    non_isolated_groups_text = re.split(r'\n\s*\n', joined_text)

    # Remove empty strings from the split result
    non_isolated_groups_text = [group.strip() for group in non_isolated_groups_text if group.strip()]

    # Check for isolated items based on the defined rules
    for k in range(len(A)):
        if A[k] != "":
            if k == 0:
                if k + 1 < len(A) and A[k + 1] == "":
                    isolated_items.append(A[k])
            elif k == len(A) - 1:
                if A[k - 1] == "":
                    isolated_items.append(A[k])
            elif A[k - 1] == "" and A[k + 1] == "":
                isolated_items.append(A[k])

    # Filter isolated items from non-isolated groups
    non_isolated_groups = [group.split('\n') for group in non_isolated_groups_text if group not in isolated_items]

    return isolated_items, non_isolated_groups

# Example usage
A = ['', '', '', 'Hello', '', "I'm a text", 'with 2 lines', 'with 3 lines', 'with 4 lines', '', 'Good', '', 'with 5 lines', 'with 7 lines']
isolated_items, non_isolated_groups = list_parser(A)

print("Isolated Items:", isolated_items)
print("Non-Isolated Groups:", non_isolated_groups)
