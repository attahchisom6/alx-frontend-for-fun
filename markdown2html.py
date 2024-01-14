#!/bin/python3
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

    return line


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
    in_paragraph = False
    parsed_lines = []

    for line in lines:
        if syntax_line(line, "* ", "li") is None:
            if not line.strip(): # evaluate to true if line is empty
                if in_paragraph:
                    parsed_lines.append("\n\t<br />\n</p>\n")
                    in_paragraph = False
                else:
                    parsed_lines.append("\n")
            else: # non empty line
                if not in_paragraph:
                    parsed_lines.append("<p>\n\t{}".format(line.strip()))
                    in_paragraph = True
                else:
                    parsed_lines.append("\n\t{}".format(line.strip()))

        if in_paragraph:
            parsed_lines.append("\n\t<br>\n<\p>\n")
        return "".join(parsed_lines)


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
            if d_line:
                dash_array.append(d_line)
            elif ast_line:
                asterisk_array.append(ast_line)
            else:
                f_out.write(parse_heading(line))
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
