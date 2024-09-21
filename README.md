# .md to .tex Converter in Python

Converts .md files to .tex, with obsidian.md files in mind. Requires no formatting issues in the .md file. Can convert multiple .md files and concatenate them into a single .tex file.

Option to customise callout (theorems, definitions, lemmas, notes etc.) in `settings.py`. Replacing the default colour options with others, or adding more options is viable.

If further packages are required for the .tex document to compile properly, then adding them in `initialise.tex` as you would for a .tex document will add these packages to the file.

## How to use

Clone the repository into a directory with the .md files to be converted. Then, run
```
./start
```
and you will be prompted for more information.
