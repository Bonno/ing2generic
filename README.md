# ing2generic

 This script converts the ing <https://www.ing.nl> csv files into more generic csv files which can be imported by FireflyIII <https://github.com/JC5/firefly-iii>
 
 Usage
-----
::

    usage: ing2generic [-h] [-o, --outfile OUTFILE] [-d, --directory DIR] [-c, --convert] csvfile

    This program converts ING (www.ing.nl) CSV files to generic csv files. The default output filename is the input filename.

    positional arguments:
      csvfile                      A csvfile to process

    optional arguments:
      -h, --help                 show this help message and exit
      -o, --outfile OUTFILE Output filename
      -d, --directory DIR   Directory to store output, default is ./converted
      -c, --convert            Convert decimal separator to dots (.), default is false


Output
------
A generic csv file converted from the csv file (default in the folder ./converted)
