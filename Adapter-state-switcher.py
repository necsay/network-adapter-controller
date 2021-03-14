# - coding: ISO8859-9 --
import subprocess
import tkinter as tk
from collections import namedtuple
from functools import partial

def disablemethod(interface):
    subprocess.call('netsh interface set interface "{}" disabled'.format(interface.name))

def enablemethod(interface):
    subprocess.call('netsh interface set interface "{}" enabled'.format(interface.name))
    
def resetmethod(interface):
    subprocess.call('netsh interface set interface "{}" disabled'.format(interface.name))
    subprocess.call('netsh interface set interface "{}" enabled'.format(interface.name))

def main():
    # a quick way to make a class that will hold data, and nothing more.
    Interface = namedtuple("Interface", "admin state object_type name")


    rawtext = subprocess.check_output('netsh interface show interface')
    stringtext = rawtext.decode("ISO-8859-9").replace('\r\n','\n')
    
    dict = {"\x94":"ö", "\x81":"ü","\x8d":"ý", "§":"ð" ,"\x9f":"þ"}

    for toreplace, dictitem in dict.items():
        stringtext = stringtext.replace(toreplace, dictitem)
    
    listext = stringtext.splitlines()

    interfaces = []
    for line in listext[3:]: # skip the first 3 lines
        
        splitlist = line.split(maxsplit=3)
        if len(splitlist) == 4:
            interfaces.append(Interface(*splitlist))

    root= tk.Tk()
    root.title('Network Adapter State Switcher')
    root.resizable(width=False, height=False)


    frame1 = tk.Frame(root, bg='grey', bd = 10, relief=tk.GROOVE)
    frame1.pack(fill=tk.X)
    for i, interface in enumerate(interfaces):
        
        disable = tk.Button(frame1, text='Disable ' + interface.name.replace(" Baðlantýsý" , ""), command=partial(disablemethod, interface),bd=5, highlightthickness=0,bg='red',activebackground='tomato',fg='black')
        disable.grid(row=i, column=0, padx=50, pady=20, sticky='ew')
        
        reset = tk.Button(frame1, text='Reset ' + interface.name.replace(" Baðlantýsý",""), command=partial(resetmethod, interface),bd=5, highlightthickness=0,bg='yellow',activebackground='khaki',fg='black')
        reset.grid(row=i, column =1, padx=50, pady=20,sticky='ew')
        
        enable = tk.Button(frame1, text='Enable ' + interface.name.replace(" Baðlantýsý" , ""), command=partial(enablemethod, interface),bd=5, highlightthickness=0,bg='green',activebackground='lawngreen',fg='black')
        enable.grid(row=i, column=2, padx=50, pady=20, sticky='ew')

    data_label = tk.Label(root, bg='black', fg='white', text=stringtext,font="Consolas", justify=tk.LEFT, bd=10, relief=tk.GROOVE,padx=30)
    data_label.pack(fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
