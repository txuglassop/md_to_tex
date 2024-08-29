from shutil import copy
from textwrap import dedent
from glob import glob

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

def write_file (md):
    print("hello!")


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
        index = input("Enter index (or 'q' to exit): ")
        int_index = int(index)

        if int_index in range(len(md_files)):
            write_file( md_files[int(int_index)] )
        elif index == 'q':
            break
        else:
            print("Invalid index")

main()