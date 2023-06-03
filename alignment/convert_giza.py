#! /usr/bin/env python3

# converts the A3.final file format (produced by GIZA) to Pharaoh format (required for symmetrization)

import re, sys

def parse_giza_alignments(inputfile, outputfile, reverse=False):
    line_index = 0
    for line in inputfile:
        line = line.strip()
        if line.startswith("#"):
            line_index = 0
        elif line_index == 1:
            pass
        elif line_index == 2:
            links = []
            matches = re.findall(r'\(\{([0123456789 ]+)\}\)', line)
            match_list = []
            for m in matches:
                if m.strip() == "":
                    match_list.append([])
                else:
                    match_list.append([int(x)-1 for x in m.strip().split(" ")])
            del match_list[0]      # NULL alignments

            src_index = 0
            for match in match_list:
                if match != []:
                    for tgt_index in match:
                        if reverse:
                            links.append(f"{tgt_index}-{src_index}")
                        else:
                            links.append(f"{src_index}-{tgt_index}")
                src_index += 1
            outputfile.write(" ".join(links) + "\n")
        line_index += 1
        

if __name__ == "__main__":
    inputfile = open(sys.argv[1])
    outputfile = open(sys.argv[2], "w")
    reverse = len(sys.argv) > 3 and sys.argv[3] == "-r"
    parse_giza_alignments(inputfile, outputfile, reverse=reverse)
