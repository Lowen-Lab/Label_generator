# Label_generator

## What this script does

This script generates all possible combinations of user entered values to automate the process of printing labels for microfuge tubes. The script uses a graphical user interface for user input, and exports PDFs for printing.

A key feature of the script is waste reduction. It asks users to select what cells in a partially-used sheet should remain empty. 

# How to use this script

After downloading the script, open a terminal window and follow these instructions:

```
cd /location/of/script
python label_gen.py
```

The first prompt is for what to name the PDF files with your labels. After hitting enter, the script will make a new window where you will add the information you wish to have in each of the 3 lines available. In the example below, I clicked "add category" under Line 1, then entered an experiment title. For the second line, I added three separate categories for the sample IDs, the day of sampling, and the replicate numbers. Note that I separate unique values within a category with commas. On the last line I added my initials and the date. 
![alt text](https://github.com/Lowen-Lab/Label_generator/blob/main/window1.png)

After hitting "Submit", the script will generate all possible combinations of values between all categories, and generate labels with those values separated by spaces. Note that there is no limit to the number of cateogories or values that you can add per line, only the practical limit of the width of the labels. The script preserves the order within a line that categories are entered (e.g. the values from the first category will always appear before values from the second category).
   - Note: If you wish to change the delimiter from the default "space" between values, you can open the script and edit the "value_delimiter" value to a string of your choice.

The script will then give the user the option of selecting areas of the sheet of labels that are already used, or should otherwise not be used for printing.
![alt text](https://github.com/Lowen-Lab/Label_generator/blob/main/window2.png)

Full rows and columns can be blocked out by clicking on the grey column and row labels on the left and top of the grid.

If more than one page is needed for all labels the user entered, the script will continue to prompt the user to verify which labels are available for printing. 

After hitting "Submit" for the final time, the script will save the labels as PDFs and print a reminder that the page needs to be printed at "Actual size" or "Scaled to 100%" to have proper label spacing.

An example output of the script is available in this repository. 
   - Note: You can easily modify the font and font size by opening the script in a text editor and changing the "label_font_name" and "label_font_size" values

This script currently only has two label profiles for divbio 5x17 and 6x21 letter sized label sheets.

# How to install the dependencies of this script

The requirements to run this pipeline are:
1. Python3
   * We recommend using [miniconda](https://docs.conda.io/en/latest/miniconda.html) to install python and the required packages

2. Two python packages:
   - tkinter
   - reportlab
   * Using conda, these packages can be installed using the following conda commands:
      - conda install tk
      - conda install -c anaconda reportlab
