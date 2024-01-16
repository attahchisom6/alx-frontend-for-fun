#!/bin/python3
import ast
import os
import sys
import re

def parse_heading(line):
    """parse heading to html"""
    heading_match = re.match(r'^(#{1,6})\s*(.*)$', line)

    if heading_match:
        level_heading = len(heading_match.group(1))
        text_heading = heading_match.group(2).strip()
        return '<h{}>{}</h{}>\n'.format(level_heading, text_heading, level_heading)

    return ""


def syntax_line(line, symbol, tag):
    """parse line with chosen symbol to html"""
    Lines = []
    l = ""
    Modified = []

    if line.startswith(symbol):
        Lines.append(line.strip());
        l = "".join(Lines)
        Modified.append("\t<{}>{}</{}>\n".format(tag, l[2:], tag))

        html = "{}".format("".join(Modified))
        Lines, l, Modified = [], "", []
        return html

    elif line.startswith(symbol) and line.endswith(symbol):
        Lines.append(line.strip())
        l = "".join(Lines)
        Modified.append("<{}>{}</{}>".format(tag, l[2:-4], tag))
        html2 = "".join(Modified)
        Lines, l, Modified = [], "", []
        return html2

    return None

def parse_paragraph(lines):
    """
    parse desired content to html paragrapgh
    """
    current_paragraph, paragraphs = [], []

    for k, line in enumerate(lines):
        heading = parse_heading(line)
        syntaxes = syntax_line(line, "- ", "li") or syntax_line(line, "* ", "li") or syntax_line(line, "**", "b")
        if not heading and not syntaxes:
            print(f"paragraph lines: {line}")
            current_paragraph.append(line.strip())
            print(f"current paragraph: {current_paragraph}")

    isolated_items, non_isolated_groups = list_parser(current_paragraph)
    print(f"tupe: {non_isolated_groups}")

    if isolated_items != []:
        k = 0
        while k < len(isolated_items):
            if isolated_items[k]:
                paragraphs.append("<p>\n\t{}\n</p>\n".format(isolated_items[k]))
            k += 1

    if non_isolated_groups:
        p = 0
        while p < len(non_isolated_groups):
            if non_isolated_groups[p]:
                paragraphs.append("<p>\n{}\n</p>\n".format("\n".join(non_isolated_groups[p])))
            p += 1

    print(f"paragraphs array: {paragraphs}")
    return "".join(paragraphs)


def list_parser(A):
    """
    parse a list into a items with diverse properties and return a tuple of them
    """
    isolated_items = []
    non_isolated_groups = []

    # logic to get non_isolated_groups: join items to aid the use of regex
    joined_text = "\n".join(A)
    non_isolated_groups_text = re.split(r"\n\s*\n", joined_text)
    non_isolated_groups_text = [group.strip() for group in non_isolated_groups_text if group.strip()]

    # logic to extract isolated items
    for k in range(len(A)):
        if A[k] != "":
            if k == 0:
                if k + 1 < len(A) and A[k + 1] == "":
                    isolated_items.append(A[k])
            elif k == len(A) - 1:
                if A[k - 1] == "":
                    isolated_items.append(A[k])
            elif 0 < k and k < len(A) - 1:
                if A[k - 1] == "" and A[k + 1] == "":
                    isolated_items.append(A[k])
        else:
            isolated_items = []

    # logic to filter out isolated items from non isolated groups
    non_isolated_groups = [group.split("\n") for group in non_isolated_groups_text if group not in isolated_items] if isolated_items else [group.split("\n") for group in non_isolated_groups_text]

    non_isolated_groups = [
            ["\t" + item + "\n\t<br />" if index != len(items) - 1 else "\t" + item for index, item in enumerate(items)]
            for items in non_isolated_groups
        ]

    print(f"isolated items: {isolated_items}")
    return isolated_items, non_isolated_groups


def markdown(filename=None, file_output=None):
    """
    A mark down script to convert markdown to html
    """
    if filename is None or file_output is None:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1);

    if not os.path.exists(filename):
        print("Missing {}".format(filename), file=sys.stderr)
        sys.exit(1)

    with open(filename, encoding="utf-8") as f:
        lines = f.readlines();

    with open(file_output, "w", encoding="utf-8") as f_out:
        dash_array = []
        asterisk_array = []
        for line in lines:
            d_line = syntax_line(line, "- ", "li")
            ast_line = syntax_line(line, "* ", "li")
            bold_line = syntax_line(line, "**", "b")
            heading = parse_heading(line)
            if d_line:
                dash_array.append(d_line)
            elif ast_line:
                asterisk_array.append(ast_line)
            elif bold_line:
                print(f"bold line:{bold_line}")
                f_out.write(bold_line)
            else:
                f_out.write(heading)
        if dash_array:
            f_out.write("<ul>\n{}\n</ul>\n".format("".join(dash_array)))
        if asterisk_array:
            f_out.write("<ol>\n{}\n</ol>\n".format("".join(asterisk_array)))
        f_out.write(parse_paragraph(lines))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        markdown()
    else:
        filename = sys.argv[1];
        file_output=sys.argv[2];
        markdown(filename=filename, file_output=file_output)
        sys.exit(0)
