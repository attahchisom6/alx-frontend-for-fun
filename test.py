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

    for group_text in non_isolated_groups_text:
        group_lines = group_text.split('\n')
        non_isolated_groups.append(group_lines)

    return isolated_items, non_isolated_groups

# Example usage
A = ['', '', '', 'Hello', '', "I'm a text", 'with 2 lines', 'with 3 lines', 'with 4 lines', '', 'Good', '', 'with 5 lines', 'with 7 lines']
isolated_items, non_isolated_groups = list_parser(A)

print("Isolated Items:", isolated_items)
print("Non-Isolated Groups:", non_isolated_groups)
