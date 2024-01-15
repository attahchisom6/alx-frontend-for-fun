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
        return html
    return None

def parse_paragraph(lines):
    """
    parse desired content to html paragrapgh
    """
    current_paragraph, paragraphs = [], []
    flag = False

    for k, line in enumerate(lines):
        heading = parse_heading(line)
        syntaxes = syntax_line(line, "- ", "li") or syntax_line(line, "* ", "li")
        if not heading and not syntaxes:
            print(f"paragraph lines: {line}")
            current_paragraph.append(line.strip())
            print(f"current paragraph: {current_paragraph}")

            """if k > 0 and not lines[k - 1].strip() and k < len(lines) - 1 and  not lines[k + 1].strip() and lines[k]:
                paragraphs.append("<p>\n\t{}\n</p>\n".format(lines[k].strip()))
                current_paragraph = []
            elif k > 0 and not lines[k - 1].strip() and k < len(lines) - 1 and \
        lines[k + 1].strip() and lines[k]:
                paragraphs.append("<p>\n\t{}\n\t<br />\n\t{}\n</p>\n".format(lines[k].strip(), lines[k + 1].strip()))
                current_paragraph = []"""

    tup = list_parser(current_paragraph)
    print(f"tupe: {tup[1]}")
    """if line.startswith("- "):
        line = dashed_line(line);
        print("here is the line: {}".format(line));
        # print("line 0: {}".format(line[0]))
        ul_items = ["\t<li>{}</li>\n".format(item.strip()) for item in line]
        return "<ul>\n" + "".join(ul_items) + "</ul>\n" """

    return "".join(paragraphs);


def list_parser(A):
    """
    parse a list into a items with diverse properties and return a tuple of them
    """
    isolated_items = []
    non_isolated_groups = []
    current_group = []

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
            else:
                current_group.append(A[k])

        if current_group:
            non_isolated_groups.append(current_group)
            current_group = []

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
            heading = parse_heading(line)
            if d_line:
                dash_array.append(d_line)
            elif ast_line:
                asterisk_array.append(ast_line)
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
