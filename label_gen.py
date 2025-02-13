'''
Label generation script - v1.0
###################################################################################################
#####################################    About this script    #####################################
###################################################################################################

This script uses a graphical user interface to generate all possible combinations of values from 
different categories, then arranges them as labels in a letter sized PDF so they can be printed
on sticky label sheets. 

To reduce waste, this script also prompts the user to exclude any labels that have already been 
used from the sheet of labels that you plan on using.

###################################################################################################
########################################    Requirements    #######################################
###################################################################################################
- python3
- tkinter (TK) -  a python module for graphical user interfaces
- reportlab - a python module used to generate the PDF and arrange the labels evenly

###################################################################################################
###################################   HOW TO RUN THIS SCRIPT    ###################################
###################################################################################################

In terminal, enter:
cd /location/of/script/
python label_gen.py

You will be prompted to enter the name of your output files in terminal before the first GUI window
appears. In the first window, text is divided into 3 lines. Click "add category" on one of the 
lines, then enter all values from that category separated by commas. Any spaces or other characters
that you include between spaces will be included in your labels.

	Example: Adding a list of subject IDs in one category, a list of timepoints in a second 
	category, and different sample types in a third category will generate all pairwise 
	combinations of those values.

		Category 1: GP01,GP02,GP03
		Category 2: d1,d2,d3
		Category 3: NW, OS

		This will generate labels like this: GP01 d1 OS, GP01 d1 NW, GP01 d2 OS, etc...

		To separate values with more than just a "space", you can enter values like this:
				Category 1: GP01 -,GP02 -,GP03 -
				Category 2: d1 -,d2 -,d3 -
				Category 3: NW, OS

				This will generate labels like this: GP01 - d1 - OS, GP01 - d1 - NW, etc

After hitting submit, the script will give you another window that shows the layout of the label 
sheet. Click on labels that should not be used for printing, then hit submit. If there are not 
enough locations available to fit all of your labels on one page, the script will save the first
sheet, then prompt you to mark the locations of labels that should not be used on a second sheet.

	If all labels are available for printing, just select "submit" without any other action.

	Entire rows and columns can be de-selected by clicking on the light grey labels above and to
	the left of the grid.

###################################################################################################
#######################################    UPDATE NOTES    ########################################
###################################################################################################
02/07/2025 - v1.0 - Published
'''
###################################################################################################
###################################### Load required modules ######################################
###################################################################################################
import os
import sys

import tkinter as tk
from tkinter import *
from tkinter import ttk
from functools import partial

from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm

###################################################################################################
###################################################################################################

value_delimiter = ' '
label_font_size = 8
label_font_name = "Helvetica"
label_profile = '5x17' #can be '5x17' or '6x21'

###################################################################################################
###################################################################################################
PDF_file_name = input('Enter output filename:\n')


if label_profile == '5x17':
	column_names = ["A", "B", "C", "D", "E"]
	column_total = len(column_names)
	row_total = 17
	NUM_LABELS_X = column_total
	NUM_LABELS_Y = row_total 
	MARGIN_L = 1.6*cm
	MARGIN_R = MARGIN_L
	MARGIN_T = 0.25*cm
	MARGIN_B = MARGIN_T
	LABEL_WIDTH = 105.0
	LABEL_HEIGHT = 46.7

elif label_profile == '6x21':
	column_names = ["A", "B", "C", "D", "E", "F"]
	column_total = len(column_names)
	row_total = 21
	NUM_LABELS_X = column_total
	NUM_LABELS_Y = row_total 
	MARGIN_L = 0.45*cm
	MARGIN_R = MARGIN_L
	MARGIN_T = 0.25*cm
	MARGIN_B = MARGIN_T
	LABEL_WIDTH = 96.0
	LABEL_HEIGHT = 36.0

def add_category_input(a,b):
	category_num = len(category_dict[a])
	category_dict[a][category_num] = tk.Text(root, height=3, width=50)
	category_dict[a][category_num].grid(column=a,row=b)

def Close(): 
	root.destroy()
def Crash():
	sys.exit()
def take_input():
	for line_num in category_dict:
		output_dict[line_num] = {}
		for cat_num in category_dict[line_num]:
			cat_text = category_dict[line_num][cat_num]
			inputValue=cat_text.get("1.0","end-1c")
			split = inputValue.strip().split(',')
			output_dict[line_num][cat_num] = split
	Close()

root = tk.Tk()
root.title('Pairwise combination of categories')
label_1 = tk.Label(root,text='Line 1')
label_1.grid(column=0, row=0)
label_2 = tk.Label(root,text='Line 2')
label_2.grid(column=1, row=0)
label_3 = tk.Label(root,text='Line 3')
label_3.grid(column=2, row=0)
category_dict = {}
category_dict[0] = {}
category_dict[1] = {}
category_dict[2] = {}
output_categories = {}
output_dict = {}
add_button_1 = tk.Button(root, text='Add category', command = lambda: add_category_input(0,len(category_dict[0])+2))
add_button_1.grid(column=0, row=1)
add_button_2 = tk.Button(root, text='Add category', command = lambda: add_category_input(1,len(category_dict[1])+2))
add_button_2.grid(column=1, row=1)
add_button_3 = tk.Button(root, text='Add category', command = lambda: add_category_input(2,len(category_dict[2])+2))
add_button_3.grid(column=2, row=1)

take_info = tk.Button(root, text='Submit', command=lambda: take_input())
take_info.grid(column=0, row=99)#.pack(side=BOTTOM)
exit_button = tk.Button(root, text='Exit',command=Crash)
exit_button.grid(column=1, row=99)
instructions = Label(root,text='This script generates all possible combinations of values between categories. After adding a new category to a line, enter all values separated by commas.\nExample use: if you have individuals A, B, C, and D, and you collected samples on days 1,2, and 3, include "A,B,C,D" and "d1,d2,d3" in separate categories on any line.')
instructions.grid(column=0, row=101, columnspan=3)#.pack(side=BOTTOM)
root.mainloop()


newline_spacer = '|newline|'
def find_all_possible_barcode_combinations(barcode_sites):
	full_barcode_list = []
	barcode_site_list = sorted(list(set(list(barcode_sites.keys()))))
	for b in range(0,len(barcode_site_list)):
		site = barcode_site_list[b]
		full_barcode_list = list(set(full_barcode_list))
		nt_list = barcode_sites[site]
		building_barcodes = []
		if full_barcode_list == []:
			for num in range(0,len(nt_list)): 
				building_barcodes.append(nt_list[num])
		else:
			for bar_num in range(0,len(full_barcode_list)):
				for nt_num in range(0,len(nt_list)):
					growing_nt_string = full_barcode_list[bar_num]+nt_list[nt_num]
					building_barcodes.append(growing_nt_string)
		full_barcode_list = building_barcodes
	full_barcode_list = sorted(list(set(full_barcode_list)))
	return full_barcode_list
line_num_list = sorted(output_dict.keys())

full_string_list = []
for l in range(0,len(line_num_list)):
	line_num = line_num_list[l]
	if output_dict[line_num] == {}:
		output_dict[line_num] = {0:' '}
	
	out_strings = []
	catg_num_list = sorted(output_dict[line_num].keys())
	for c in range(0,len(catg_num_list)):
		full_string_list = list(set(full_string_list))
		building_strings = []
		catg_num = catg_num_list[c]
		local_catg_strings = output_dict[line_num][catg_num]
		if full_string_list == []:
			for string in local_catg_strings:
				building_strings.append(string)
		else:
			for i in range(0,len(full_string_list)):
				for string in local_catg_strings:
					new_string = full_string_list[i]+value_delimiter+string
					building_strings.append(new_string)
		full_string_list = building_strings
	full_string_list = sorted(list(set(full_string_list)))
	building_strings = []
	for i in range(0,len(full_string_list)):
		new_string = full_string_list[i]+newline_spacer
		building_strings.append(new_string)
	full_string_list = building_strings
label_list = full_string_list


def button_click(button_id):
	btn = btn_dict[button_id]
	btn.config(bg='crimson')
	try:
		cur_state = state_dict[buttonID]
	except:
		cur_state = 0
	if cur_state == 0:
		btn.config(bg='crimson')
		state_dict[buttonID] = 1
	elif cur_state == 1:
		state_dict[buttonID] = 0

def column_click(col_num):
	for r in range(1,row_total+1):
		buttonID = str(r)+'-'+str(col_num)
		btn = btn_dict[buttonID]
		try:
			cur_state = state_dict[buttonID]
		except:
			cur_state = 0
		if cur_state == 0:
			btn.config(bg='crimson')
			state_dict[buttonID] = 1
		elif cur_state == 1:
			state_dict[buttonID] = 0

def row_click(row_num):
	for c in range(1,column_total+1):
		buttonID = str(row_num)+'-'+str(c)
		btn = btn_dict[buttonID]
		try:
			cur_state = state_dict[buttonID]
		except:
			cur_state = 0
		if cur_state == 0:
			btn.config(bg='crimson')
			state_dict[buttonID] = 1
		elif cur_state == 1:
			state_dict[buttonID] = 0
			btn.config(bg='lightgreen')

def finish_click():
	root.destroy()


root = tk.Tk()
root.title('Select missing labels')
state_dict = {}
btn_dict = {}
for c in range(0,column_total+1):
	for r in range(0,row_total+1):
		buttonID = str(r)+'-'+str(c)
		btn_dict[buttonID] = tk.Button(root)
for c in range(0,column_total+1):
	for r in range(0,row_total+1):
		buttonID = str(r)+'-'+str(c)
		state_dict[buttonID] = 0
		if c == 0 and r == 0:
			pass
		elif r == 0 and c >0: # full column
			cell_ID = column_names[c-1]+str("{:02d}".format(r))
			btn_dict[buttonID] = tk.Button(root)
			btn_dict[buttonID].config(text=cell_ID, bg='lightgrey', command=lambda column_name=c: column_click(column_name))
			btn_dict[buttonID].grid(row=r, column=c, sticky="w")
		elif c == 0: # full row
			cell_ID = column_names[c-1]+str("{:02d}".format(r))
			btn_dict[buttonID] = tk.Button(root)
			btn_dict[buttonID].config(text=cell_ID, bg='lightgrey', command=lambda row_name=r: row_click(row_name))
			btn_dict[buttonID].grid(row=r, column=c, sticky="w")
		else:
			cell_ID = column_names[c-1]+str("{:02d}".format(r))
			btn_dict[buttonID] = tk.Button(root)
			btn_dict[buttonID].config(text=cell_ID, bg='lightgreen', command=lambda button=buttonID: button_click(button))
			btn_dict[buttonID].grid(row=r, column=c, sticky="w")
close_button = tk.Button(root, text='Submit',command=finish_click)
close_button.grid(row=row_total+1, column=0, sticky="w")
exit_button = tk.Button(root, text='Exit',command=Crash)
exit_button.grid(row=row_total+1, column=1, sticky="w")
instructions = Label(root,text='Select any labels on a sheet that new labels should not be printed on (e.g. Those labels are already used).\nSelect the grey cells to block out full rows or columns.')
instructions.grid(column=column_total+2, row=0)
root.mainloop()


PAGESIZE = letter
# PAGESIZE = (PAGESIZE[0]-(MARGIN_L+MARGIN_R),PAGESIZE[1]-(MARGIN_T+MARGIN_B))
font_size = label_font_size
line1_height = label_font_size*2
line2_height = label_font_size*1
line3_height = 0


def front_label(line1_string: str,line2_string: str,line3_string: str) -> Drawing:
	line1 = String(0, line1_height, line1_string, fontName=label_font_name, fontSize=label_font_size, textAnchor="middle")
	line1.x = LABEL_WIDTH / 2	# center text

	line2 = String(0, line2_height, line2_string, fontName=label_font_name, fontSize=label_font_size, textAnchor="middle")
	line2.x = LABEL_WIDTH / 2	# center text

	line3 = String(0, line3_height, line3_string, fontName=label_font_name, fontSize=label_font_size, textAnchor="middle")
	line3.x = LABEL_WIDTH / 2	# center text

	label_drawing = Drawing(LABEL_WIDTH, LABEL_HEIGHT)
	label_drawing.add(line1)
	label_drawing.add(line2)
	label_drawing.add(line3)
	return label_drawing


# PAGESIZE = letter
SHEET_TOP = PAGESIZE[1]

canvas_count = 0
label_canvas = Canvas(PDF_file_name+'-'+str(canvas_count)+'.pdf', pagesize=PAGESIZE)
label_num = -1
labels_remaining = len(label_list)
for var in range(0,99):
	if labels_remaining <=0:
		break
	else:
		for u in range(0, NUM_LABELS_Y):
			for i in range(0, NUM_LABELS_X):
				cellID = str(u+1)+'-'+str(i+1)
				try:
					cell_state = state_dict[cellID]
				except:
					cell_state = 0
				if cell_state == 0:
					label_num += 1
					labels_remaining -= 1
					if label_num < len(label_list):
						try:
							sticker = front_label(label_list[label_num].split(newline_spacer)[0],label_list[label_num].split(newline_spacer)[1],label_list[label_num].split(newline_spacer)[2])
						except:
							stiker = sticker = front_label('','','')
						x = i * LABEL_WIDTH+MARGIN_L#*cm
						y = SHEET_TOP - (u+1) * LABEL_HEIGHT + 2*MARGIN_T
						# y = SHEET_TOP - LABEL_HEIGHT - u * LABEL_HEIGHT - MARGIN_T/2
						renderPDF.draw(sticker, label_canvas, x, y)
		label_canvas.showPage()
		label_canvas.save()
		del label_canvas
		if labels_remaining >=1:
			canvas_count += 1
			label_canvas = Canvas(PDF_file_name+'-'+str(canvas_count)+'.pdf', pagesize=PAGESIZE)

			root = tk.Tk()
			root.title('Select missing labels')
			state_dict = {}
			btn_dict = {}
			for c in range(0,column_total+1):
				for r in range(0,row_total+1):
					buttonID = str(r)+'-'+str(c)
					btn_dict[buttonID] = tk.Button(root)
			for c in range(0,column_total+1):
				for r in range(0,row_total+1):
					buttonID = str(r)+'-'+str(c)
					state_dict[buttonID] = 0
					if c == 0 and r == 0:
						pass
					elif r == 0 and c >0: # full column
						cell_ID = column_names[c-1]+str("{:02d}".format(r))
						btn_dict[buttonID] = tk.Button(root)
						btn_dict[buttonID].config(text=cell_ID, bg='lightgrey', command=lambda column_name=c: column_click(column_name))
						btn_dict[buttonID].grid(row=r, column=c, sticky="w")
					elif c == 0: # full row
						cell_ID = column_names[c-1]+str("{:02d}".format(r))
						btn_dict[buttonID] = tk.Button(root)
						btn_dict[buttonID].config(text=cell_ID, bg='lightgrey', command=lambda row_name=r: row_click(row_name))
						btn_dict[buttonID].grid(row=r, column=c, sticky="w")
					else:
						cell_ID = column_names[c-1]+str("{:02d}".format(r))
						btn_dict[buttonID] = tk.Button(root)
						btn_dict[buttonID].config(text=cell_ID, bg='lightgreen', command=lambda button=buttonID: button_click(button))
						btn_dict[buttonID].grid(row=r, column=c, sticky="w")
			close_button = tk.Button(root, text='Submit',command=finish_click)
			close_button.grid(row=row_total+1, column=0, sticky="w")
			exit_button = tk.Button(root, text='Exit',command=Crash)
			exit_button.grid(row=row_total+1, column=1, sticky="w")
			root.mainloop()
		else:
			break

print("PRINT AT ACTUAL SIZE OR SCALE TO 100%")
