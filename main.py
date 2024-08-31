from shutil import copy
from textwrap import dedent
from glob import glob
from re import sub

# initialise packages, date, title etc.
def init_file (name, author, date):
    copy("initialise_doc.tex", name)

    with open(name, "a") as f:
        info = dedent(f"""
                      
            \\title{{{name}}}
            \\author{{{author}}}
            \\date{{{date}}}

            \\begin{"document"}

            \\begin{"titlepage"}
                \\maketitle
            \\end{"titlepage"}

            \\newpage

            \\tableofcontents

            \\newpage

            
        """)

        f.write(info)

# given a line, convert any * or ** formatting to LaTeX equivalent
def handle_formatting_line (line):
    line = sub(r"\*\*(.*?)\*\*", r"\\textbf{\1}", line)
    line = sub(r"\*(.*?)\*", r"\\textit{\1}", line)

    return line

# given a line that begins with #, converts it to .tex format
def handle_heading_line (line):
    new_line = line

    # handle heading cases
    translator = str.maketrans('', '', '0123456789.#\n')

    if line.startswith('# '):
        new_line = r"\subsection{" + line.translate(translator).lstrip() + "}\n"
    elif line.startswith('## '):
        new_line = r"\subsubsection{" + line.translate(translator).lstrip() + "}\n"
    elif line.startswith('###'):
        new_line = r"\subsubsubsection{" + line.translate(translator).lstrip() + "}\n"

    return new_line


# convert the md files to tex, and write them to the main file
def write_file (name, md):
    f_main = open(name, "a")

    f_main.write("\n\\section{" + md.rstrip(".md") + "}\n\n")

    with open(md, "r") as f:
        lines = f.readlines()
    
    in_list = False # to keep track of whether we are in an itemize environment

    for i in range(len(lines)):
        line = handle_formatting_line(lines[i])

        if line.startswith('-') and in_list == False:
            f_main.write("\\begin{itemize}\n\\item[-] ")
            in_list = True
            line = line[1:].lstrip()
        elif line.startswith('-') and in_list == True:
            f_main.write("\\item[-] ")
            line = line[1:].lstrip()
        elif in_list == True:
            f_main.write("\\end{itemize}\n")
            in_list = False

        if line.startswith('#'):
            f_main.write(handle_heading_line(line))
        elif line.startswith("$$"):
            if "\\begin{align}" in lines[i+1] or "\\end{align}" in lines[i-1]:
                continue
            else:
                f_main.write(line)
        else:
            f_main.write(line)

    f_main.close()


def main ():
    name = input("Enter name of file (do not add .tex): ")
    author = input("Enter author's name: ")
    date = input("Enter date: ")

    name = name + ".tex"

    new_file = open(name, "w+")
    
    init_file(name, author, date)

    # file has been initialised
    print("\nAll .md files found in current directory:")
    md_files = glob('*.md')

    for i in range(len(md_files)):
        print("[" + str(i) + "] " + md_files[i])

    while True:
        index = input("Enter index for .md file to convert (or 'q' to exit): ")

        if index == 'q':
            break

        int_index = int(index)
        
        if int_index in range(len(md_files)):
            write_file(name, md_files[int(int_index)])
        else:
            print("Invalid index")

    # add a \end{document} in wahtnot before

    new_file.close

main()