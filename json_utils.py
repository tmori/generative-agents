#!/usr/bin/python
# -*- coding: utf-8 -*-

def fix_quotes(line):
    fixed_line = ""
    quote_mode = False
 
    for char in line:
        if quote_mode == False:
            if char == '"':
                quote_mode = True
        else:
            if char == '"':
                quote_mode = False
            elif char == ':' or char == '\n':
                fixed_line += '"'
                quote_mode = False
        fixed_line += char

    return fixed_line

def fix_backslashes(json_string):
    # 不正なバックスラッシュを修正する
    fixed_string = json_string.replace("\\", "\\\\")
    return fixed_string

def parse_one_entry(line: str, key: str):
    string_without_quotes = line.replace('"', '')
    entries = string_without_quotes.split(":")
    contents = []
    #skip DetailedStrategy
    #get contents
    for entry in entries:
        if line in entry:
            continue
        else:
            contents.append(entry)
    new_contents = " ".join(contents)
    #recreate line
    new_line = '"' + key + '": ' + '"' + new_contents + '",'
    print(new_line)
    return new_line

def parse_plan(org_data: str):
    lines = org_data.split("\n")
    output_lines = []
    start_flag = False
    for line in lines:
        if start_flag == False:
            if "{" in line:
                start_flag = True
                output_lines.append(fix_quotes(line))
            else:
                pass
        else:
            if "DetailedStrategy" in line:
                line = parse_one_entry(line, "DetailedStrategy")
            output_lines.append(fix_quotes(fix_backslashes(line)))

    return "\n".join(output_lines)
