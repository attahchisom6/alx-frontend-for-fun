#!/bin/python3
import os
import sys
import re

"""def parse_heading(line):
    parse heading to html
    heading_match = re.match(r'^(#{1,6})\s*(.*)$', line)

    if heading_match:
        level_heading = len(heading_match.group(1))
        text_heading = heading_match.group(2).strip();
        return '<h{}>{}</h{}>\n'.format(level_heading, text_heading, level_heading)

    if line.startswith("- "):
        ul_items = ["<li>{}</li>".format(item.strip()) for item in line.split("- ")[1:]]
        UL_items = []
        for ul_item in ul_items:
            UL_items.append(ul_item)
        L = "".join(UL_items)
        print(L)
        return "<ul>\n" + L + "</ul>\n"
    return line"""
def parse_heading(line):
    """parse heading to html"""
    heading_match = re.match(r'^(#{1,6})\s*(.*)$', line)

    if heading_match:
        level_heading = len(heading_match.group(1))
        text_heading = heading_match.group(2).strip()
        return '<h{}>{}</h{}>\n'.format(level_heading, text_heading, level_heading)

    """if line.startswith("- "):
        line = dashed_line(line);
        print("here is the line: {}".format(line));
        # print("line 0: {}".format(line[0]))
        ul_items = ["\t<li>{}</li>\n".format(item.strip()) for item in line]
        return "<ul>\n" + "".join(ul_items) + "</ul>\n" """

    return line


def dashed_line(l):
    """
    parse line that start with - into  single string"""
    Lines = []
    line = ""
    Modified = []
    n = ""
    k = ""
    # for l in lines:
    if l.startswith("- "):
        Lines.append(l.strip());
        line = "".join(Lines)
        n = line
        Modified.append("<li>{}</li>".format(line[2:]))
        k = "".join(Modified)

        html = "<ul>{}</ul>".format("".join(Modified))
        print(f'line: {n}')
        print(f"Modified: {k}")
        print(f"html: {html}")
        return html
    return l

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
        for line in lines:
            line = dashed_line(line)
            if line:
                f_out.write(parse_heading(line))
            

if __name__ == "__main__":
    if len(sys.argv) < 3:
        markdown()
    else:
        filename = sys.argv[1];
        file_output=sys.argv[2];
        markdown(filename=filename, file_output=file_output)
    sys.exit(0)
