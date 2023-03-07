"""
Module for the functions that do the prints and make the comunication with the user
"""
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tools.plot import plot
from tools.solve import *
from pysid.io.csv_data import *


def initial_menu():
    """
    prints the first option menu and returns a valid command
    Returns
    -------
    TYPE int
        Value representing the chosen option

    """
    print(f'Pysid(v0.1) - Identificação de sistemas')
    print("Escolha uma opção:")
    print("1 - Solução de minímos quadrados (MQ)")
    print("2 - Solução de minímos quadrados estendido (EMQ)")
    print("3 - Solução de minímos quadrados recursivo (RMQ)")
    print("4 - Informações relevantes")
    print("5 - Configurações")
    print("0 - Sair")
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
    print("- O seprador default é a vírgula.")
    print("- No .csv a ordem das colunas deve ser entradas(u), saídas(y)")
    print("- As ordens dos polinomios devem ser inteiros")
    print("- Utilize arquivos .csv ou .txt")
    print("- O minimos quadrados(MQ) e o minimos quadrados recursivo(MQR) devem dar resultados\n muito próximos, variam apenas na implementação")
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
    print("Escolha uma opção de configuração:")
    print("1 - Alterar separador padrão do csv\nAtual: ", config[0])
    print("2 - Quantidade de linha de dados a serem ignorados(pelo cabeçalho)\nAtual: ", config[1])
    print("3 - Numero de algarismos significativos a serem mostrados nos resultados\nAtual: ", config[2])
    print("4 - Numero máximo de reptições(Apenas para MQE)\nAtual: ", config[3])
    print("5 - Diferença miníma entre a soma quadratica de dois erros consecutivos necessaria para assumir-se que houve convergencia(em %)(Apenas para MQE)\nAtual: ", config[4])
    print("0 - Sair")
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
        print("Informe o novo separador:")
        config[cmd-1] = input("\n>> ")
    elif cmd == 2:
        print("Informe a quantidade de linha de dados a serem ignorados(pelo cabeçalho):")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 3:
        print("Informe o numero de algarismos significativos a serem mostrados nos resultados:")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 4:
        print("Informe o numero máximo de reptições a serem feitas(Apenas para MQE):") 
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 5:
        print("Informe a diferença miníma entre a soma quadratica de dois erros consecutivos necessaria para assumir-se que houve convergencia(em %):")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 0:
        pass
    print("\n *** Configurações salvas *** \n")

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
                input("Precione ENTER para escolher um arquivo ")
                filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
                if filename is not None:
                    if filename.endswith('.csv') or filename.endswith('.txt'):
                        data = load_data(filename,delim=config[0],skip_rows=int(config[1]))
                        nu = int(input("Informe quantas colunas de entradas há na amostragem:\n>> "))
                        if nu > data.shape[1]-1:
                            print("***Valor inválido, não há colunas referentes a saída***\n")
                        else:
                            file = True #ok, tudo certo com o file
                            ny = data.shape[1]-nu
                            u,y = sep_data(nu,ny,data)
            if file:
                na, nb, nc, nk = get_order_polys(cmd)
                if   cmd == 1:
                    m = solve.ls_interface(na,nb,nk,u,y,prec=int(config[2]))
                    if nu == 1 and ny == 1:
                        p = input("Deseja plotar os dados?[Y/N]\n>> ")
                        if p == 'y' or p == 'Y':
                            plot.plot(m,u,y)
                elif cmd == 2:
                    m = solve.els_interface(na,nb,nc,nk,u,y,float(config[4])/100,int(config[3]),int(config[2]))
                    if nu == 1 and ny == 1:
                        p = input("Deseja plotar os dados?[Y/N]\n>> ")
                        if p == 'y' or p == 'Y':
                            plot.plot(m,u,y)
                elif cmd == 3:
                    solve.rls_interface(na,nb,nk,u,y,int(config[2]))

                print("\n-------------------\n")
                repeat = input("Deseja usar os mesmos dados?[Y/N]\n>> ")
                if repeat == 'Y' or repeat == 'y':
                    repeat_file = True
                else:
                    repeat_file = False    
        elif cmd == 4:
            print_infos()
        elif cmd == 5:
           config = change_config(print_config_menu(config),config)
           with open('config.txt','w') as f:
               for item in config:
                   f.write(str(item)+"-")
           # print(config)

if __name__ == '__main__' : main()