
from pysid.io.print import print_model
from pysid.identification.models import polymodel
from pysid.identification.pemethod import arx
from pysid.identification.recursive import rls, els
from pysid.io.csv_data import gen_data
from numpy.linalg import inv
from numpy import matmul,concatenate,ones,power

_all__ = ['ls_interface','els_interface','rls_interface']

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
