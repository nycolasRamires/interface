"""
Created on Tue Apr 18 11:04:14 2023

@author: dioge
"""
from tkinter import filedialog, DISABLED, NORMAL, StringVar, IntVar, LabelFrame, W, DoubleVar
from pysid.identification.pemethod import arx
from pysid.identification.recursive import els
from pysid.io.print import print_matrix, print_model
# from pysid.identification.recursive import els,rls
from pysid.io.csv_data import load_data
import customtkinter as ctk
import time
from io import StringIO
import sys


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout

ctk.set_appearance_mode("Dark") #dark, System or light
ctk.set_default_color_theme("blue")
# Main window
root = ctk.CTk() # Create the main window


# TODO : get pysid version
root.title(f'Pysid(v0.1)') # window title 
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
#root.resizable(False,False)
root.geometry('240x470+%d+%d' % (ws/2-200,hs/2-180)) #window size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

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

configs = [0.005,200]
th = DoubleVar(root,0.005)
n_max =IntVar(root,200)
def advOptionsWindow():
    sub_window = ctk.CTkToplevel(root)
    sub_window.wm_title("Advence Options")
    sub_window.focus_set()

    advOp_frame = ctk.CTkFrame(sub_window)
    advOp_frame.grid(row=0, column=0, sticky="w", padx=10,pady=5)

    #button for infos in the window
    file_config_save_button = ctk.CTkButton(sub_window, text="Save", width=10, height=10, command=sub_window.destroy)
    file_config_save_button.grid(row=5, column=0, sticky="e", pady=5, padx = 10)

    th_entry = ctk.CTkEntry(advOp_frame,width=80, textvariable=th).grid(row=3, column=1, sticky="w", padx=10)
    th_label = ctk.CTkLabel(advOp_frame, text="Treshold :    ").grid(row=3, column=0, sticky="w", padx=10)

    n_max_entry = ctk.CTkEntry(advOp_frame,width=80,textvariable=nb).grid(row=4, column=1, sticky="w", padx=10)
    n_max_label = ctk.CTkLabel(advOp_frame, text="Max number of repetitions : ").grid(row=4, column=0, sticky="w", padx=10)


def info_window_parameters():
    # Create the sub-window
    sub_window = ctk.CTkToplevel(root)
    sub_window.focus_set()
    # sub_window.grab_set()
    s = [  " Na : Quantidade de amostras passadas da saída que influenciam a saída atual, ordem do denominador",
           " Nb : Quantidade de amostras passadas da entrada que influenciam a saída atual",
           "  Nk : Quantidade de amostras necessárias para a entrada influenciar a saída",
           "  Nc : Quantidade de amostras passadas do ruído de medição que influenciam a saída atual"
           ]

    # Set the sub-window title
    sub_window.title("Informations")
    sub_window.geometry("630x300")

    for i in range(len(s)):
        text_label = ctk.CTkLabel(sub_window, text=s[i], anchor=W)
        text_label.pack(pady=5, padx=5)

# def on_window_resize(event):
#     global width
#     global height
#     if event.widget.widgetName == "toplevel":
#         if (width != event.width) and (height != event.height):
#             window_width, window_height = event.width,event.height
#             width = event.width
#             height = event.height
#             for w in root.winfo_children():
#                 w.destroy()
#             root.update()
#             root.update_idletasks()

def save_model(m_list):
    #add
    #   TIME that was saved
    #   file from witch it was idented
    #   number of inputs and outputs
    #   coulouns that were used for u and y
    #   a name
    m = m_list[0]
    file = m_list[1]
    s = ''
    s += time.strftime("Modelo salvo em  %d/%m/%Y %H:%M",time.localtime()) + "\n"
    s += f"Modelo gerado pelos dados em {file}, com {m.nu} entrada(s) e {m.ny} saída(s) \n\n"
    
    
    temp = m.A[0][0]
    s += m.gen_model_string()
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file_content = s
                file.write(file_content)
                print(f"File saved as: {file_path}")
        except Exception as e:
            print(f"Error: {str(e)}")
    print(m.gen_model_string())

tab_window = ctk.CTkToplevel(root)
tab_window.withdraw()
#tab_window.resizable(False,False)
tabs = ctk.CTkTabview(tab_window, width=200)
i = 0
models = {}
def response_tab(s,m):
    global i
    global tab_window
    global tabs
    global models
    try: #if the user has closed the window, launchs again
        tab_window.deiconify()
    except:
        tab_window = ctk.CTkToplevel(root)
        #tab_window.resizable(False,False)
        tabs = ctk.CTkTabview(tab_window, width=200)
        i = 0
        models = {}

    tabStr = str(na.get()) + '|' + str(nb.get()) +'  '+ m.name
    models[tabStr] = [m,f_path.get()]
    i += 1
    tabs.add(tabStr)
    tabs.tab(tabStr).grid_columnconfigure(0, weight=1)
    text_label = ctk.CTkLabel(tabs.tab(tabStr), text=s, font=ctk.CTkFont(family='Terminal', size=16))
    text_label.grid(pady=10, padx=10)
    tabs.grid(column=1,row=1,rowspan=4)
    tabs.set(tabStr)

    save_button = ctk.CTkButton(tab_window, text="Save curren model", width=10, height=25, 
                                command=lambda : save_model(models[tabs.get()]))
    save_button.grid(row=5, column=1, sticky="e", pady = 5, padx = 5)

def create_string(m):
    # t = poly_to_str(m.A)
    # print(t[0])
    with Capturing() as output:
        print_model(m,only_polynomials=True)
    s = ""
    for i in output:
        s += i + "\n"
    print(m.costfunction)
    if isinstance(m.costfunction, float):
        s += "Cost function: " + f"{m.costfunction:.4f}" + "\n\n"
    else: # TODO: remove when costfunction of els is corrected
        s += "Cost function: " + f"{m.costfunction[0,0]:.4f}" + "\n\n"
    if m.nparam < 6:
        with Capturing() as output:
            print_matrix(m.P, prec=3)
        mat = ""
        for i in output:
            print(i)
        for i in output:
            mat += i + "\n"
        s += "Accuracy:\n\n" + mat #print_matrix2(m.P,prec = 3)
    else:
        s += "Var of each parameter:\n\n"
        for i in range(1,len(m.A[0,0])):
            s += f"a{i} = {m.P[i-1][i-1]}\n\n"
        for i in range(1,len(m.B[0,0])):
            s += f"b{i} = {m.P[i+len(m.A[0,0])-2][i+len(m.A[0,0])-2]}\n\n"
        if not isinstance(m.C,type(None)):
            for i in range(1,len(m.C[0,0])):
                s += f"c{i} = {m.P[i+len(m.A[0,0])+len(m.B[0,0])-3][i+len(m.A[0,0])+len(m.B[0,0])-3]}\n\n"
    return s

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
        #m = rls(na,nb,nk,u,y)
        pass
    elif x == 4:
        pass #VRFT
    return m


def action(x,na,nb,nc,nk,nu,f):
    if f != "":
        if f.endswith('.csv') or f.endswith('.txt'):
            if input_columnsV.get() != '-1':
                try:
                    temp = (list(input_columnsV.get().split(',')))
                    idxsu = [int(x) for x in temp]
                    n_columns = data.shape[1]
                    if len(idxsu) > n_columns-1:
                        raise RuntimeError(f"Not enough columns \n Current file has {n_columns} columns")
                    idxsy = [x for x in range(n_columns) if x not in idxsu]
                    u = data.take(idxsu,axis=1)
                    y = data.take(idxsy,axis=1)
                except RuntimeError as e:
                    s = str(e)
                except Exception:
                    s = "Input columns format error \n See model in 'relevant information'"
                finally:
                    warning_window = ctk.CTkToplevel(root)
                    warning_window.title("Error")
                    warning_window.bell()
                    warning_window.geometry("260x70")
                    text_label = ctk.CTkLabel(warning_window, text=s, font=ctk.CTkFont(family='Helvetica', size=12))
                    text_label.grid(pady=5, padx=5)
            else:
                ny = data.shape[1]-nu
                u = data[:,:nu]
                y = data[:,nu:ny+nu]
                m = ident(x,na,nb,nc,nk,u,y)
                s = create_string(m)
                response_tab(s,m)
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
        text_label.grid(pady=5, padx=5, sticky='ew')

# for the file associate part
file_frame = ctk.CTkFrame(root) #frame for file name
file_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)

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
    global data
    if file_path:
        file_name = file_path.split("/")[-1]
        file_label.configure(text=file_name)
        f_path.set(file_path)
        f = f_path.get()
        if f.endswith('.csv') or f.endswith('.txt'):
            data = load_data(f,delim=sepV.get(),skip_rows=skip_rowV.get()) # TODO : change skip_rows
            #TODO : Create sign or window tealing that data was/not loaded
        else:
            warning_window = ctk.CTkToplevel(root)
            warning_window.title("Error")
            warning_window.bell()
            warning_window.geometry("300x75")
            s = "The file must be a .csv or .txt"
            text_label = ctk.CTkLabel(warning_window, text=s, font=ctk.CTkFont(family='Helvetica', size=15))
            text_label.grid(pady=5, padx=5)


def config_file():
    sub_window = ctk.CTkToplevel(root)
    sub_window.wm_title("File configuration")
    sub_window.focus_set()

    def config_file_info():
        info_window = ctk.CTkToplevel(sub_window)
        info_window.focus_set()
        s = [  "To choose the collumns in the file that \n represent the input, use the 'input colouns' field ",
             "The format of the field should be integers with comas in between. i.e.: 1,3",
             "The 'skip rows' field it is used to the count for the header of the csv file",
             "To use the first 'N° input' collumns as input, use the value -1",]

        # Set the sub-window title
        info_window.title("Informations")
        info_window.geometry("630x300")

        for i in range(len(s)):
            text_label = ctk.CTkLabel(info_window, text=s[i], anchor=W)
            text_label.pack(pady=5, padx=5)

    #button for infos in the window
    file_config_info_button = ctk.CTkButton(sub_window, text="Instructions", width=10, height=10, command=config_file_info)
    file_config_info_button.grid(row=6, column=0, sticky="e", pady=5, padx = 5)

    #button for 'saving'
    file_config_save_button = ctk.CTkButton(sub_window, text="Save", width=10, height=10, command=sub_window.destroy)
    file_config_save_button.grid(row=6, column=0, sticky="w", pady=5, padx = 5)

    fconfig_frame = ctk.CTkFrame(sub_window) #frame for file name
    fconfig_frame.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    sep = ctk.CTkEntry(fconfig_frame,width=80, textvariable=sepV).grid(row=3, column=1, sticky="w", padx=10)
    sep_label = ctk.CTkLabel(fconfig_frame, text="Separator:    ").grid(row=3, column=0, sticky="w", padx=10)

    skip_rows = ctk.CTkEntry(fconfig_frame,width=80,textvariable=skip_rowV).grid(row=4, column=1, sticky="w", padx=10)
    skip_rows_label = ctk.CTkLabel(fconfig_frame, text="Skip rows: ").grid(row=4, column=0, sticky="w", padx=10)
    
    input_columns = ctk.CTkEntry(fconfig_frame,width=80,textvariable=input_columnsV).grid(row=5, column=1, sticky="w", padx=10)
    columns_label = ctk.CTkLabel(fconfig_frame, text="Input columns: ").grid(row=5, column=0, sticky="w", padx=10)


# Create a button to choose a file
file_button = ctk.CTkButton(file_frame, text="Choose File", width=10, height=25, command=choose_file)
file_button.grid(row=0, column=1, sticky="w", pady=5, padx = 5)
file_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)

#create button to open window of file configs
file_config_button = ctk.CTkButton(file_frame, text="File Options", width=10, height=25, command=config_file)
file_config_button.grid(row=1, column=1, sticky="w", pady=5, padx = 5)
# file_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)

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
parametersFrame = ctk.CTkFrame(root,width=200)
parametersFrame.grid(row=3, column=0, sticky="NSEW",pady=5,padx=10)
parametersLabel = ctk.CTkLabel(master=parametersFrame,text="Parameters",font=ctk.CTkFont(family='Helvetica', size=15))
parametersLabel.grid(row=0, column=0, sticky="w",padx=10)

advOptionsButton = ctk.CTkButton(radioB_frame,command=advOptionsWindow, text = "Adv. Options",width=10,height=15)
advOptionsButton.grid(row=7,column=0,sticky="e",padx=5, pady=5)

# img = tk.PhotoImage(file = "question3.png") # "?" image for the button
infoButtonParamters = ctk.CTkButton(parametersFrame,text="?",
                                    width=20,height=15,
                                    font=ctk.CTkFont(family='Helvetica', size=15),command=info_window_parameters) #,image=img,
infoButtonParamters.grid(row=0, column=1,sticky="e",padx=10)

goButton = ctk.CTkButton(parametersFrame,text="Go",width=10,height=15,
                         command=lambda: action(x.get(),na.get(),nb.get(),nc.get(),nk.get(),nu.get(),f_path.get()))
goButton.grid(row=7, column=1, sticky="e", padx=12, pady=5)


na = IntVar(root,2)
nb = IntVar(root,1)
nc = IntVar(root,1)
nk = IntVar(root,1)
# ny = IntVar(root,1)
nu = IntVar(root,1)

skip_rowV = IntVar(root, 1)
sepV = StringVar(root,",")
input_columnsV = StringVar(root,'-1') # -1
#root.bind("<Configure>", on_window_resize)

paramFrame_show() #so that the parametrs frame appears from the start

root.protocol("WM_DELETE_WINDOW", root.destroy)
root.mainloop()