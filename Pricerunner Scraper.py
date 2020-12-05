import tkinter as tk
from tkinter import *
import tkinter.messagebox
import pyperclip
import urllib.request
import json
import statistics

def searcher(item, category):
    item_searchable = item.replace(" ", "%20")
    url = f'https://www.pricerunner.dk/public/search/v2/dk?q={item_searchable}' #DINTEXTHER erstattes med den tekst du vil søge efter. F,eks '3700x', eller 'b450'. Nu tager vi 3770x bare for et eksempel

    req = urllib.request.Request(url) 
    r = urllib.request.urlopen(req).read() 

    content = json.loads(r.decode('utf-8'))
    
    temp_price_list_ = []
    
    if len(content["products"])==0:
        final_prices.append("Noget gik galt :/")
    
    else:
        split_item = item.lower().split()
        for products in content["products"]:
            name_desc = str(products["name"]).lower().replace(" ", "")+str(products["description"]).lower().replace(" ", "")
            if any(word in name_desc for word in split_item):
                if products["category"]["name"] == f'{category}':
                    temp_price_list_.append((int(float((products["lowestPrice"]["amount"])))))
    
        if len(temp_price_list_)==0:
            final_prices.append("Noget gik galt :/")
        
        else:
            temp_price_list_.sort()
            if len(temp_price_list_)<4:
                final_prices.append(int(statistics.mean(temp_price_list_)))
            else:
                final_prices.append(int(statistics.mean(temp_price_list_[0:3])))
                                
def get_entry():
    
    global final_prices
    final_prices = []
    
    input_1 = entry_1.get()
    input_2 = entry_2.get()
    input_3 = entry_3.get()
    input_4 = entry_4.get()
    input_5 = entry_5.get()
    input_6 = entry_6.get()
    
    if input_1 == "":
        input_1 = "Ikke valgt"
        final_prices.append(0)
    else:
        searcher(input_1, "CPU")
    if input_2 == "":
        input_2 = "Ikke valgt"
        final_prices.append(0)
    else:
        searcher(input_2, "Bundkort")
    if input_3 == "":
        input_3 = "Ikke valgt"
        final_prices.append(0)
    else:
        searcher(input_3, "Grafikkort")
    if input_4 == "":
        input_4 = "Ikke valgt"
        final_prices.append(0)
    else:
        searcher(input_4, "Strømforsyninger")
    if input_5 == "":
        input_5 = "Ikke valgt"
        final_prices.append(0)
    else:
        searcher(input_5, "RAM")
    if input_6 == "":
        input_6 = "Ikke valgt"
        final_prices.append(0)
    else:
        searcher(input_6, "Harddiske")
    
    pc_parts = [input_1, input_2, input_3, input_4, input_5, input_6]
    
    final_price_list = (f'{pc_parts[0]}' + " --> " + f'{final_prices[0]}' + "\n" 
      f'{pc_parts[1]}' + " --> " + f'{final_prices[1]}' + "\n" 
      f'{pc_parts[2]}' + " --> " + f'{final_prices[2]}' + "\n" 
      f'{pc_parts[3]}' + " --> " + f'{final_prices[3]}' + "\n" 
      f'{pc_parts[4]}' + " --> " + f'{final_prices[4]}' + "\n" 
      f'{pc_parts[5]}' + " --> " + f'{final_prices[5]}' + "\n"
      "Total:    " + str(sum(filter(lambda i: isinstance(i, int), final_prices))))
    
    pyperclip.copy(final_price_list)
                        
    tkinter.messagebox.showinfo("Din pris", final_price_list)             

root = tk.Tk()

tk.Label(root, text="CPU").grid(row=0)
tk.Label(root, text="Bundkort").grid(row=1)
tk.Label(root, text="Grafikkort").grid(row=2)
tk.Label(root, text="PSU").grid(row=3)
tk.Label(root, text="RAM").grid(row=4)
tk.Label(root, text="Harddisk").grid(row=5)

entry_1 = tk.Entry(root)
entry_2 = tk.Entry(root)
entry_3 = tk.Entry(root)
entry_4 = tk.Entry(root)
entry_5 = tk.Entry(root)
entry_6 = tk.Entry(root)

entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)
entry_3.grid(row=2, column=1)
entry_4.grid(row=3, column=1)
entry_5.grid(row=4, column=1)
entry_6.grid(row=5, column=1)

button = tk.Button(root, text="Run", command=get_entry).grid(columnspan=2)

root.mainloop()