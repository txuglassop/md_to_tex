# .md to .tex Converter in Python

Converts `.md` files to `.tex`, with `obsidian.md` files in mind. Requires no formatting issues in the `.md` file. Can convert multiple `.md` files and concatenate them into a single `.tex` file.

Option to customise callout (theorems, definitions, lemmas, notes etc.) in `settings.py`. Replacing the default colour options with others, or adding more options is viable, among other settings.

If further packages are required for the .tex document to compile properly, then adding them in `initialise.tex` as you would for a `.tex` document will add these packages to the file.

## How to use

Clone the repository, and suppose /path/to/your/md/files is a path to the directory with the wanted `.md` files to be converted. Then, run
```
./start.sh /path/to/your/md/files
```
and you will be prompted for more information.

If no directory is provided, defaults the directory `start.sh` is in.

## Settings

See `settings.py` for all settings, which can be changed. What follows is more information for each setting option.

### Callout Colours

Colours for callouts in `.md` which are converted to `tkcolorbox`'s in `.tex` with the specified colour in `settings.py`.

To change colours for callouts, see `settings.py` and desired callout. Then, change the associated string to colour of choice. Note that default LaTeX colours, as well as `xcolor` with `dvipsnames` and `table` colours are supported.

### Default Figure Size

Currently, when converting figures, `main.py` defaults to converting all figures to the same size, which is a default of 7cm. To change this, edit the string associated with `figure_size` to the desired figure size.

### Skip Preamble

If `skip_preamble = True`, then no text before the first heading (`#`) will be copied to the `.tex` file, otherwise everything is copied.  

Sometimes, Obsidian plugins add text to the top of the `.md` file to signify settings, or you may have some type of preamble that is not desired in the `.tex` file. If this is the case, have this setting set to `True`, otherwise `False`.