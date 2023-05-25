"""
Module for the functions that do the prints and make the comunication with the user
"""
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tools.plot import plot
from tools import solve
from pysid.io.csv_data import *

def initial_menu():
    """
    prints the first option menu and returns a valid command
    Returns
    -------
    TYPE int
        Value representing the chosen option

    """
    print(f'Pysid(v0.1) - System Identification')
    print("Choose an option:")
    print("1 - Least Squares Solution (LS)")
    print("2 - Extended Least Squares Solution (ELS)")
    print("3 - Recursive Least Squares Solution (RLS)")
    print("4 - Design Controler by Virtual Reference Feedback Tuning")
    print("5 - Relevant Information")
    print("6 - Settings")
    print("0 - Exit")

    cmd = int(input(">> "))
    if cmd >= 0 and cmd <= 5:
        return cmd
    else:
        print("*** Comando Inválido ***\n")
        return initial_menu()

def print_infos():
    """
    prints informations about the use of the interface

    Returns
    -------
    None.

    """
    print("- The default separator is comma.")
    print("- In .csv files, the order of the columns should be inputs(u), outputs(y).")
    print("- The orders of the polynomials should be integers.")
    print("- Use .csv or .txt files.")
    print("- The Least Squares Solution (LS) and Recursive Least Squares Solution (RLS) \n should give very similar results, differing only in implementation.")
    print("\n--------------\n")


def print_config_menu(config):
    """
    Prints the current configuration and the options to change it
    Returns the corresponding value to the configuration that will be changed
    Parameters
    ----------
    config : list
        list with the current configs

    Returns
    -------
    TYPE int
        value that represents the config that will be changed

    """
    # numero de alg sig
    # numero de treshold 
    # numero max de repetições
    # separador padrão do csv
    # numero de linhas a serem ignoradas no csv
    print("Choose a configuration option:")
    print("1 - Change default csv separator\nCurrent: ", config[0])
    print("2 - Number of lines to be ignored (header size)\nCurrent: ", config[1])
    print("3 - Number of significant digits to be displayed in the results\nCurrent: ", config[2])
    print("4 - Maximum number of iterations (Only for ELS)\nCurrent: ", config[3])
    print("5 - Minimum difference between the sum of two consecutive quadratic errors required to assume convergence (in %) (Only for ELS)\nCurrent: ", config[4])
    print("0 - Exit")
    cmd = int(input(">> "))
    if cmd >= 0 and cmd <= 5:
        return cmd
    else:
        print("*** Comando Inválido ***\n")
        return print_config_menu()

def change_config(cmd,config):
    """
    changes an element in the config list based on cmd

    Parameters
    ----------
    cmd : int
        config that will be changed.
    config : list
        list of configs.

    Returns
    -------
    config : list
        the config list already changed.

    """
    if cmd == 1:
        print("Enter the new separator:")
        config[cmd-1] = input("\n>> ")
    elif cmd == 2:
        print("Enter the number of data lines to be ignored (by the header):")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 3:
        print("Enter the number of significant digits to be displayed in the results:")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 4:
        print("Enter the maximum number of iterations to be performed (Only for ELS):") 
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 5:
        print("Enter the minimum difference between the sum of two consecutive quadratic errors required to assume convergence (in %) (Only for ELS):")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 0:
        pass
    print("\n *** Settings saved successfully *** \n")

    return config
def sep_data(nu,ny,data):
    """
    separates the data array in two arrays, corresponding to input and output

    Parameters
    ----------
    nu : int
        number of inputs.
    ny : int
        number of outputs.
    data : numpy array
        inputs and outputs.

    Returns
    -------
    u : numpy array
        array with input data.
    y : numpy array
        array with output data.

    """
    u = data[:,:nu]
    y = data[:,nu:ny+nu]
    return u,y

def get_order_polys(cmd):
    """
    gets from the user the the order of the polynomial based on the
    chosen method

    Parameters
    ----------
    cmd : int 
        cmd based on chosen method (ls, els or rls)

    Returns
    -------
    na : int
        order of polynomial A
    nb : int
        order of polynomial D
    nc : int
        order of polynomial C
    nk : int
        order of delay

    """
    na = int(input("Ordem de A(q):\n>> "))
    nb = int(input("Ordem de B(q):\n>> "))
    if(cmd == 2):
        nc = int(input("Ordem de C(q):\n>> "))
    else:
        nc = 0
    nk = int(input("nk:\n>> "))
    return na,nb,nc,nk

def main():
    cmd = -1
    # sep, linhas ignorar, alg sig, max iterac, dif erro
    try:
        with open('config.txt','r') as f:
            config = f.readline()
            config = config.split('-')
            for i in range(4):
                config[i+1] = config[i+1]
            config = config[:-1]

    except:
        config = [",",1,4,100,0.05]
    filename = None
    repeat_file = False
    while(cmd != 0):
        cmd = initial_menu()
        if cmd <= 3 and cmd != 0:
            #Abrir o seletor de arquivos
            if not repeat_file:
                file = False
                input("Press ENTER to choose a file ")
                root = tk.Tk()
                filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
                root.destroy()
                if filename is not None:
                    if filename.endswith('.csv') or filename.endswith('.txt'):
                        data = load_data(filename,delim=config[0],skip_rows=int(config[1]))
                        nu = int(input(" Enter how many input columns there are in the sampling:\n>> "))
                        if nu > data.shape[1]-1:
                            print("*** Invalid value, there are no columns related to output***\n")
                        else:
                            file = True #ok, tudo certo com o file
                            ny = data.shape[1]-nu
                            u,y = sep_data(nu,ny,data)
            if file:
                na, nb, nc, nk = get_order_polys(cmd)
                if   cmd == 1:
                    m = solve.ls_interface(na,nb,nk,u,y,prec=int(config[2]))
                    if nu == 1 and ny == 1:
                        p = input("Do you want to plot the data? [Y/N]\n>> ")
                        if p == 'y' or p == 'Y':
                            plot.plot(m,u,y)
                elif cmd == 2:
                    m = solve.els_interface(na,nb,nc,nk,u,y,float(config[4])/100,int(config[3]),int(config[2]))
                    if nu == 1 and ny == 1:
                        p = input("Do you want to plot the data? [Y/N]\n>> ")
                        if p == 'y' or p == 'Y':
                            plot.plot(m,u,y)
                elif cmd == 3:
                    solve.rls_interface(na,nb,nk,u,y,int(config[2]))
                elif cmd == 4:
                    if shape(u)[1] == 1 and shape(y)[1] == 1:
                        solve.vrft_interface(u,y)
                    else:
                        print("VRFT interface is not ready for not siso systems")
                print("\n-------------------\n")
                repeat = input("Continue with the previously entered data? [Y/N]\n>> ")
                if repeat == 'Y' or repeat == 'y':
                    repeat_file = True
                else:
                    repeat_file = False
        elif cmd == 5:
            print_infos()
        elif cmd == 6:
           config = change_config(print_config_menu(config),config)
           with open('config.txt','w') as f:
               for item in config:
                   f.write(str(item)+"-")
           # print(config)

if __name__ == '__main__' :
    main()