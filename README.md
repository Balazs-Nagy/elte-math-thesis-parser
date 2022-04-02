# ELTE math thesis parser

This script creates a webscraper object that collects information regarding to
theses that were submitted to either program of the the Institute of Mathematics,
Faculty of Science, Eötvös Loránd University.
The author, supervisor, title, year of defence and the thesis itself in .pdf are all publicly available
and accessible [via this link](https://www.math.elte.hu/kepzesek/diplomamunkak/).

The goal of writing this script was to practice objected-oriented webscraping
and also to create a list of theses that is more convenient to go through
to find topics that I am interested in.

The following features are currently implemented:
- parse specific programs or by setting the `programs` parameter of the `parse_all()`
method to `None` will parse all available programs,
- use the `to_excel()` method to export the data gathered in the previous point
and a list of all available programs to Excel,
- use the `download()` method to save a copy of the collected theses to disk in .pdf format.

The `main.py` presents the above usage.