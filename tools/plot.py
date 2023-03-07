# -*- coding: utf-8 -*-
from pysid.identification.models import polymodel
from pysid.io.csv_data import gen_data
import matplotlib.pyplot as plt

__all__ = ['plot']

def plot(model,u,y):
    """
    generate data based on the model and plots the result

    Parameters
    ----------
    model : pysid polymodel
        identified model
    u : numpy array
        array of inputs.
    y : numpy array
        array of outputs.

    Returns
    -------
    None.

    """
    # TODO : change lw based on number of samples
    y_m = gen_data(model.A[0,0], model.B[0,0], u.shape[0], u, 0)[:,1]
    plt.title("Saída Real / Saída Estimada", fontsize=20)
    plt.plot(range(len(u)),u,'.-',label='Entrada',lw=1.5)
    plt.plot(range(len(y)),y,'.-',label='Saída Real',lw=2)
    plt.plot(range(len(y_m)),y_m,'-*',label='Saída Estimada',lw=2)
    plt.grid()
    plt.legend(fontsize=10)
    plt.show()
    