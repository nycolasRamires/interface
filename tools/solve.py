
from pysid.io.print import print_model
from pysid.identification.models import polymodel
from pysid.identification.pemethod import arx
from pysid.identification.recursive import rls, els
from pysid.io.csv_data import gen_data
from numpy.linalg import inv
from numpy import matmul,concatenate,ones,power, array, insert, zeros, polymul, add
from scipy.signal import TransferFunction
import vrft

_all__ = ['ls_interface','els_interface','rls_interface','vrft_interface']

def ls_interface(na,nb,nk,u,y,prec=3):
    """
    identifies a ARX model with least squares

    Parameters
    ----------
    na : int
        order of polynomial A
    nb : int
        order of polynomial D
    nk : int
        order of delay
    u : numpy array
        array of inputs.
    y : numpy array
        array of outputs.
    prec : int, optional
        number of significant algharisms for paramters. The default is 3.

    Returns
    -------
    m : pysid polymodel
        identified model

    """
    ny = y.shape[1]
    nu = u.shape[1]
    
    na = ones((ny,ny),dtype=int)*na
    nb = ones((ny,nu),dtype=int)*nb
    nk = ones((ny,nu),dtype=int)*nk
    
    m = arx(na,nb,nk,u,y)
    print_model(m,prec=prec)
    print(m.gen_model_string().split('\n')[0] ,end='')
    print(f' identificado com {u.shape[0]} amostras')
    print(f'para um total de {m.nparam} parâmetros',end='\n\n')
    return m


def els_interface(na,nb,nc,nk,u,y,th=0.005,n_max=500,prec=3):
    """
    identifies a model with extended least squares

    Parameters
    ----------
    Parameters
    ----------
    na : int
        order of polynomial A
    nb : int
        order of polynomial D
    nc : int
        order of polynomial C
    nk : int
        order of delay
    u : numpy array
        array of inputs.
    y : numpy array
        array of outputs.
    th : float, optional
        treshold for minimum diference in between iterations.The default is 0.005
    n_max : int, optional
        maximum number of iterations. The default is 500
    prec : int, optional
        number of significant algharisms for paramters. The default is 3.

    Returns
    -------
    m : pysid polymodel
        identified model

    """
    m = els(na, nb, nc, nk, u, y, th, n_max)
    print_model(m,prec=prec)

    # TODO : print(f'Cost function per sample: ...')
    # print("Infos de saída(matriz de covariancia) e tal")
    # print("Infos de regressão(n de amostras, sis mimo..)\n")
    return m

def rls_interface(na,nb,nk,u,y,prec=3):
    """
    identifies a model with recursive least squares

    Parameters
    ----------
    na : int
        order of polynomial A
    nb : int
        order of polynomial D
    nk : int
        order of delay
    u : numpy array
        array of inputs.
    y : numpy array
        array of outputs.
    prec : int, optional
        number of significant algharisms for paramters. The default is 3.

    Returns
    -------
    m : pysid polymodel
        identified model
    """
    m = rls(na,nb,nk,u,y)
    print_model(m,prec=prec)
    # TODO : print(f'Cost function per sample: ...')
    # print("Infos de saída(matriz de covariancia) e tal")
    # print("Infos de regressão(n de amostras, sis mimo..)\n")
    return m

def sign_str(n):
    if n >= 0:
        return '+'
    else:
        return '-'

def vrft_interface(u,y):
    """
    identifies the controller given the input and output of a G(z)
    The Routine also asks for desired transfer function and a choice between a
    P, PI, PD or PID structure for the controller.

    Parameters
    ----------
    u : ndarray
        Input sampled from the process in witch the controller will act
    y : ndarray
        Output sampled from the process in witch the controller will act

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    print('Enter the numerator of Td:',end='>> ')
    numTd = array([float(x) for x in (input().split(' '))])
    nnTd = len(numTd)
    print('Enter the denominator of Td:',end='>> ')
    denTd = array([float(x) for x in (input().split(' '))])
    ndTd = len(denTd)


    # if nnTd > ndTd: #pyvrft não permite, colocar uma condição na interface
    #     denTd = np.insert(denTd,0,np.zeros(nnTd-ndTd))

    if nnTd < ndTd: #precisa ter a mesma len para usar o polymul direito
        numTd = insert(numTd,0,zeros(ndTd-nnTd))

    # step ou convolve para ver resposta
    Td = TransferFunction(numTd, denTd, dt=1)

    nL = polymul(numTd,add(denTd,-numTd,None))
    dL = polymul(denTd,denTd)
    L = TransferFunction(nL, dL, dt=1) #td(1-td) -> convolve (conv matlab)
    p = 0 #Polo de alta frequência
    P = [TransferFunction([1.0], [1.0], dt=1)]
    I = [TransferFunction([1.0,0.0], [1.0,-1.0], dt=1)]
    D =  [TransferFunction([1.0,-1.0], [1.0,-1*p], dt=1)]

    print("Enter the controller structure:")
    print("1 - Proportional")
    print("2 - Proportional-integral")
    print("3 - Proportional-derivative")
    print("4 - Proportional-integral-derivative")
    #print("5 - Outro") #add mais opções pre prontas?
    c = int(input(">> "))
    if c==1:
        C = [P]
    elif c==2:
        C = [P,I]
    elif c==3:
        C = [P,D]
    elif c==4:
        C = [P,I,D]
    cont = vrft.design(u, y, y, Td, C, L)

    print("C[z] = ", end='\n    ')
    for i in range(len(C)):
        print(f'{(cont[i][0]):.3f}*', end='(')
        for j in range(len(C[i][0].num)):
            if j == len(C[i][0].num)-1:
                print(f'{abs(C[i][0].num[j])}',end='')
            else:
                print(f'{abs(C[i][0].num[j])}*z^{(len(C[i][0].num) -j -1)} {sign_str(C[i][0].num[j+1])}',end='')
        print(end=')' + '\t'*2)
    print(end='\n    ')
    for i in range(len(C)):
        if i == len(C)-1:
            print(f'{"-"*(6)}',end='' )
        else:
            print(f'{"-"*(6)}',end='\t'*2 + '+' + '\t'*2 )
    print(end='\n    ')
    for i in range(len(C)):
        for j in range(len(C[i][0].den)):
            if j == len(C[i][0].den)-1:
                print(f'{abs(C[i][0].den[j])}',end='')
            else:
                print(f'{abs(C[i][0].den[j])}*z^{(len(C[i][0].den) -j -1)} {sign_str(C[i][0].den[j+1])} ',end='')
        print(end='' + '\t'*4)
    return cont #Vetor bem bruto por enquanto
    # TODO: Step pra ver a T_obtida e a Td
    #       T = nC*nG/(dC*dG + nC*nG)