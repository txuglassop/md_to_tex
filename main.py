from shutil import copy
from textwrap import dedent
from glob import glob
from re import sub, search
import settings
from sys import argv
from os import chdir, getcwd, path

# initialise packages, date, title etc.
def init_file (name, author, date, og_dir):
    init_tex = path.join(og_dir, "initialise_doc.tex")
    copy(init_tex, name)

    with open(name, "a") as f:
        info = dedent(f"""
                      
            \\title{{{name.removesuffix(".tex")}}}
            \\author{{{author}}}
            \\date{{{date}}}

            \\begin{{document}}

            \\begin{{titlepage}}
                \\maketitle
            \\end{{titlepage}}

            \\newpage

            \\tableofcontents

            \\newpage

            
        """)

        f.write(info)

# given a line, convert any * or ** formatting to LaTeX equivalent
# also handle misc cases
def handle_formatting_line (line):
    line = sub(r"\*\*(.*?)\*\*", r"\\textbf{\1}", line)
    line = sub(r"\*(.*?)\*", r"\\textit{\1}", line)

    if "{align}" in line:
        line = line.replace("align", "align*")
    
    if r"`\begin{proof}`" in line:
        line = line.replace(r"`\begin{proof}`", r"\begin{proof}")

    if r"`\end{proof}`" in line:
        line = line.replace(r"`\end{proof}`", r"\end{proof}")

    if r"***" in line:
        line = line.replace(r"***", r"\noindent\rule{15.2cm}{0.4pt}")

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

def init_callout (f_main, line):
    callout_type = search(r"\[!(.*?)\]", line).group(1)

    # streamline callout names
    if any(substring in callout_type for substring in ["thm", "theo", "Thm"]):
        callout_type = "theorem"
    elif any(substring in callout_type for substring in ["def", "Def"]):
        callout_type = "definition"
    elif any(substring in callout_type for substring in ["lemma", "Lem"]):
        callout_type = "lemma"
    elif any(substring in callout_type for substring in ["Info", "inf"]):
        callout_type = "info"
    elif any(substring in callout_type for substring in ["warn", "Warn"]):
        callout_type = "warning"
    elif any(substring in callout_type for substring in ["tip"]):
        callout_type = "tip"
    else:
        callout_type = "note"

    colour = getattr(settings, callout_type)
    title = search(r"\](.*)", line).group(1).lstrip()
    title = callout_type.capitalize() + ": " + title

    f_main.write("\\begin{tcolorbox}[colback=" + colour + "!5!white,colframe=" + colour + "!75!black,title=" + title + "]\n")
    
def handle_figure (f_main, line):
    fig = search(r"\[\[(.*?)\]\]", line).group(1)
    width = getattr(settings, "figure_size")

    f_main.write("\\begin{figure}[h]\n\centering\n\includegraphics[width=" + width + "]{" + fig + "}\n\\end{figure}\n\n")

# convert the md files to tex, and write them to the main file
def write_file (name, md):
    f_main = open(name, "a")

    f_main.write("\n\\section{" + md.rstrip(".md") + "}\n\n")

    with open(md, "r") as f:
        lines = f.readlines()
    
    in_list = False # to keep track of whether we are in an itemize environment
    in_callout = False # keep track of whether we are in a callout
    if getattr(settings, "skip_preamble"):
        started = False
    else:
        started = True

    for i in range(len(lines)):
        line = handle_formatting_line(lines[i])

        # skip all the stuff at the top until we reach the first heading
        if started == False and not line.startswith('#'):
            continue
        
        started = True

        # handle callouts (theorems, lemmas, notes, warnings etc.)
        if line.startswith('>[') and in_callout == False:
            init_callout(f_main, line)
            in_callout = True
            continue # the function will write the line for us
        elif line.startswith('>') and in_callout:
            line = line[1:].lstrip()
        elif in_callout == True:
            if in_list:
                f_main.write("\\end{itemize}\n")
                in_list = False
            f_main.write("\\end{tcolorbox}\n")
            in_callout = False

        # handle lists
        if line.startswith('-') and in_list == False:
            f_main.write("\\begin{itemize}\n\\item[-] ")
            in_list = True
            line = line[1:].lstrip()
        elif line.startswith('-') and in_list:
            f_main.write("\\item[-] ")
            line = line[1:].lstrip()
        elif in_list:
            f_main.write("\\end{itemize}\n")
            in_list = False

        # handle figures
        if line.startswith("![["):
            handle_figure(f_main, line)
            continue
        
        # handle headings
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

if __name__ == "__main__":
    og_dir = getcwd()
    directory = argv[1]
    chdir(directory)

    name = input("Enter name of file (do not add .tex): ")
    author = input("Enter author's name: ")
    date = input("Enter date: ")

    name = name + ".tex"

    new_file = open(name, "w+")
    
    init_file(name, author, date, og_dir)

    # file has been initialised
    print("\nAll .md files found in {directory}:")
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

    new_file.close

    f = open(name, "+a")
    f.write("\n\n" + r"\end{document}")

    f.close()

