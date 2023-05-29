"""
Created on Tue Apr 18 11:04:14 2023

@author: dioge
"""
from tkinter import filedialog, GROOVE, DISABLED, NORMAL, StringVar, IntVar, LabelFrame, W
import pysid
from pysid.identification.pemethod import arx
# from pysid.identification.recursive import els,rls
from pysid.io.csv_data import load_data
import customtkinter as ctk

ctk.set_appearance_mode("Dark") #dark, System or light
ctk.set_default_color_theme("blue")
# Main window
root = ctk.CTk() # Create the main window
root.title(f'Pysid(v0.1)') # window title
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
root.geometry('240x420+%d+%d' % (ws/2-200,hs/2-180)) #window size

#information-window
def info_window():
    sub_window = ctk.CTkToplevel(root)
    sub_window.focus_set()
    #just add another item to the list of strings
    s = [  "- The default separator is comma\n",
           "- In .csv files, the order of the columns should be inputs(u), outputs(y).",
           "- The orders of the polynomials should be integers.",
           "- Use .csv or .txt files.",
           "- The Least Squares Solution (LS) and Recursive Least Squares Solution (RLS) \n should give very similar results, differing only in implementation.",
           "ekfuhwihuwueih"]

    # Set the sub-window title
    sub_window.title("Informations")
    sub_window.geometry("630x300")
    #displays the itens in the list
    for i in range(len(s)):
        text_label = ctk.CTkLabel(sub_window, text=s[i], anchor=W)
        text_label.pack(pady=5, padx=5)

# making of the button that calls "info_window()"
infoButton = ctk.CTkButton(root, text="Relevant information", command=info_window)
infoButton.grid(row=4, column=0, sticky="w", padx=10, pady=1)# Pack the button widget into the window


def advOptionsWindow():
    pass #TODO

def info_window_parameters():
    # Create the sub-window
    sub_window = ctk.CTkToplevel(root)
    sub_window.focus_set()
    # sub_window.grab_set()
    s = [  "- Na é ...",
           "- Nb é",
           ]

    # Set the sub-window title
    sub_window.title("Informations")
    sub_window.geometry("630x300")

    for i in range(len(s)):
        text_label = ctk.CTkLabel(sub_window, text=s[i], anchor=W)
        text_label.pack(pady=5, padx=5)

tab_window = ctk.CTkToplevel(root)
tab_window.withdraw()
tabs = ctk.CTkTabview(tab_window, width=200)
i = 0
def response_tab(s,na):
    global i
    global tab_window
    global tabs
    tab_window.deiconify()
    tabStr = "Model " + str(i)
    i += 1
    tabs.add(tabStr)
    tabs.tab(tabStr).grid_columnconfigure(0, weight=1)
    text_label = ctk.CTkLabel(tabs.tab(tabStr), text=s, font=ctk.CTkFont(family='Helvetica', size=12))
    text_label.grid(pady=5, padx=5)
    tabs.grid(column=1,row=1,rowspan=3)


def printer(x): #for testing
    print(f_path.get())

def paramFrame_show():
    if x.get() != 4:
        w = 80
        Nu = ctk.CTkEntry(parametersFrame,width=w, textvariable=nu).grid(row=2, column=1, sticky="w", padx=10)
        Nu_label = ctk.CTkLabel(parametersFrame, text="N° inputs :").grid(row=2, column=0, sticky="w", padx=10)

        A = ctk.CTkEntry(parametersFrame,width=w, textvariable=na).grid(row=3, column=1, sticky="w", padx=10)
        A_label = ctk.CTkLabel(parametersFrame, text="Na:    ").grid(row=3, column=0, sticky="w", padx=10)

        B = ctk.CTkEntry(parametersFrame,width=w,textvariable=nb).grid(row=4, column=1, sticky="w", padx=10)
        B_label = ctk.CTkLabel(parametersFrame, text="Nb: ").grid(row=4, column=0, sticky="w", padx=10)

        C_label = ctk.CTkLabel(parametersFrame,text="Nc: ").grid(row=5, column=0, sticky="w", padx=10)

        K = ctk.CTkEntry(parametersFrame,width=w,textvariable=nk).grid(row=6, column=1, sticky="w", padx=10)
        K_label = ctk.CTkLabel(parametersFrame, text="Nk: ").grid(row=6, column=0, sticky="w", padx=10)

        if x.get() == 2:
            C = ctk.CTkEntry(parametersFrame,width=w,textvariable=nc, state=NORMAL).grid(row=5, column=1, sticky="w", padx=10,)
        else:
            C = ctk.CTkEntry(parametersFrame,width=w,textvariable=nc, state=DISABLED).grid(row=5, column=1, sticky="w", padx=10,)
    else: # TODO
        # C = Entry(parametersFrameLabel, textvariable=nc, state=ttk.DISABLED).grid(row=3, column=1, sticky="w", padx=10,)
        # C_label.grid(row=3, column=0, sticky="w", padx=10)
        # A_label = Label(parametersFrameLabel, text="Outra: ").grid(row=1, column=0, sticky="w", padx=10)
        pass

#calls pysid functions and define the model
def ident(x,na,nb,nc,nk,u,y):
    ny = y.shape[1]
    nu = u.shape[1]
    # na = ones((ny,ny),dtype=int)*na
    # nb = ones((ny,nu),dtype=int)*nb
    # nc = ones((ny,1),dtype=int)*nc
    # nk = ones((ny,nu),dtype=int)*nk

    if x == 1:
        m = arx(na,nb,nk,u,y)
    elif x == 2:
        m = els(na,nb,nc,nk,u,y,th=0.005,n_max=200) #TODO option to change this
    elif x == 3:
        m = rls(na,nb,nk,u,y)
    elif x == 4:
        pass #VRFT
    return m


def action(x,na,nb,nc,nk,nu,f):
    print(f)
    if f != "":
        if f.endswith('.csv') or f.endswith('.txt'):
            data = load_data(f,delim=",",skip_rows=0) # TODO : change settings option
            ny = data.shape[1]-nu
            u = data[:,:nu]
            y = data[:,nu:ny+nu]
            m = ident(x,na,nb,nc,nk,u,y)
            # show_model(m)
            s = m.gen_model_string()
            response_tab(s,na)
        else:
            warning_window = ctk.CTkToplevel(root)
            warning_window.title("Error")
            warning_window.bell()
            warning_window.geometry("150x150")
            s = "The file must be a .csv or .txt"
            text_label = ctk.CTkLabel(warning_window, text=s, font=ctk.CTkFont(family='Helvetica', size=15))
            text_label.grid(pady=5, padx=5)
    else:
        warning_window = ctk.CTkToplevel(root)
        warning_window.title("Error")
        warning_window.bell()
        warning_window.geometry("170x70")
        s = "Choose a file first"
        text_label = ctk.CTkLabel(warning_window, text=s, font=ctk.CTkFont(family='Helvetica', size=12))
        text_label.grid(pady=5, padx=5)

# for the file associate part
file_frame = ctk.CTkFrame(root) #frame for file name
file_frame.grid(row=0, column=0, sticky="w", padx=10)

label_frame = LabelFrame(file_frame,text="Chosen file",font=ctk.CTkFont(family='Helvetica', size=11)) #text for file name frame
label_frame.grid(row=0, column=0, sticky="w", padx=10)

file_label = ctk.CTkLabel(file_frame, text="No file chosen") #text for file name on start
file_label.grid(row=0, column=0, sticky="w", padx=10)

# Define a function to choose a file and update the file label
f_path = StringVar(root,"") #variable to extract the name from the function
data = []
def choose_file():
    filetypes = (
        ('Valid files', '*.txt *.csv'),
        ('All files', '*.*')
    )
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    if file_path:
        file_name = file_path.split("/")[-1]
        file_label.configure(text=file_name)
        f_path.set(file_path)

# Create a button to choose a file
file_button = ctk.CTkButton(file_frame, text="Choose File", width=10, height=25, command=choose_file)
file_button.grid(row=0, column=1, sticky="w", pady=10, padx = 5)
file_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)

#for the rabio buttons
radioB_frame = ctk.CTkFrame(root) #frame for the rabio buttons
radioB_frame.grid(row=2, column=0, sticky="sw", padx=10, pady=5)
radioBLabel = LabelFrame(radioB_frame,text="Action",font=ctk.CTkFont(family='Helvetica', size=11)) #label of the frame
radioBLabel.grid(row=0, column=0, sticky="w",pady=5,padx=5)


# x é a variavel que dira qual radioButton está selecionado
# o valor "value" na declaração do radioButton é armazenado em x
x = IntVar(radioB_frame,1)

#creaton of the buttons
rb_ls  = ctk.CTkRadioButton(radioB_frame, text='Least Squares', variable=x, value=1,command=paramFrame_show)
rb_els = ctk.CTkRadioButton(radioB_frame, text='Extended Least Squares', variable=x, value=2,command=paramFrame_show)
rb_rls = ctk.CTkRadioButton(radioB_frame, text='Recursive Least Squares', variable=x, value=3,command=paramFrame_show)
rb_Con = ctk.CTkRadioButton(radioB_frame, text='Controller with VRFT', variable=x, value=4,command=paramFrame_show)

#placement
rb_ls.grid( row=0, column=0, sticky="w", padx=10, pady=2)
rb_els.grid(row=1, column=0, sticky="w", padx=10, pady=2)
rb_rls.grid(row=2, column=0, sticky="w", padx=10, pady=2)
rb_Con.grid(row=3, column=0, sticky="w", padx=10, pady=2)


# button = ttk.Button(root, text="Printer", command=lambda: printer(x))
# button.grid(row=10, column=0, sticky="w", padx=10)# Pack the button widget into the window

#parametrs frame 
parametersFrame = ctk.CTkFrame(root,width=20)
parametersFrame.grid(row=3, column=0, sticky="w",pady=5,padx=10)
parametersLabel = ctk.CTkLabel(master=parametersFrame,text="Parameters",font=ctk.CTkFont(family='Helvetica', size=15))
parametersLabel.grid(row=0, column=0, sticky="w",padx=10)

advOptionsButton = ctk.CTkButton(parametersFrame,command=advOptionsWindow, text = "Adv. Options",width=10,height=15)
advOptionsButton.grid(row=7,column=0,sticky="w,",padx=5, pady=5)

# img = tk.PhotoImage(file = "question3.png") # "?" image for the button
infoButtonParamters = ctk.CTkButton(parametersFrame,text="?",
                                    width=20,height=15,
                                    font=ctk.CTkFont(family='Helvetica', size=15),command=info_window_parameters) #,image=img,
infoButtonParamters.grid(row=0, column=1,sticky="e",padx=10)

goButton = ctk.CTkButton(parametersFrame,text="Go!",width=10,height=15,
                         command=lambda: action(x.get(),na.get(),nb.get(),nc.get(),nk.get(),nu.get(),f_path.get()))
goButton.grid(row=7, column=1, sticky="e", padx=12, pady=5)

na = IntVar(root,2)
nb = IntVar(root,1)
nc = IntVar(root,1)
nk = IntVar(root,1)
ny = IntVar(root,1)
nu = IntVar(root,1)

paramFrame_show() #so that the parametrs frame appears from the start

root.protocol("WM_DELETE_WINDOW", root.destroy)
root.mainloop()