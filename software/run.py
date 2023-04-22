import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)
import win32gui, win32con
import eel
import pandas as pd
import numpy as np
import os
import umap
import dec_tgan

homedirectory = os.getcwd()

class Dataset:
    def __init__(self, path):
        self.path=path
        self.celltypes = pd.read_csv(path, header=None, skiprows=lambda x: x != 0).iloc[0,1:]
        self.celltypelist=list(self.celltypes.unique())
        self.matrix = pd.read_csv(path, header=None, skiprows=1, index_col=0).T
        self.matrix_per_celltypes = {}
        for celltype in self.celltypelist:
            self.matrix_per_celltypes[celltype]=self.matrix[self.celltypes==celltype]

dataset = None

@eel.expose
def selectFile(filtertext, multiselect):
    try:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
        if multiselect:
            result = win32gui.GetOpenFileNameW(
                hwndOwner=hWnd,
                Filter=filtertext,
                Title="Select Files",
                Flags=win32con.OFN_ALLOWMULTISELECT|win32con.OFN_EXPLORER)
        else:
            result = win32gui.GetOpenFileNameW(
                hwndOwner=hWnd,
                Filter=filtertext,
                Title="Select File",
                Flags=win32con.OFN_EXPLORER)
        return result[0]
    except:
        return ""

@eel.expose
def selectSaveFile(filtertext):
    try:
        hWnd = ctypes.windll.user32.GetForegroundWindow()
        result = win32gui.GetSaveFileNameW(
                hwndOwner=hWnd,
                Filter=filtertext,
                Title="Save As",
                Flags=win32con.OFN_FILEMUSTEXIST|win32con.OFN_OVERWRITEPROMPT)
        return result[0]
    except:
        return ""

@eel.expose
def setDatabase(path):
    global dataset
    dataset = Dataset(path)
    num_cells = []
    for celltype in dataset.celltypelist:
        num_cells.append(len(dataset.matrix_per_celltypes[celltype]))
    return [dataset.celltypelist, num_cells, dataset.celltypes.to_numpy().tolist()]

@eel.expose
def runUmap():
    if dataset != None:
        reducer = umap.UMAP(n_components=2, random_state=0, n_neighbors=10)
        x_embedded = reducer.fit_transform(dataset.matrix)
        return x_embedded.tolist()
    return None

lastrun = None

@eel.expose
def startGAN(ct, a, b, c):
    global lastrun
    os.chdir(homedirectory)
    if dataset != None:
        lastrun = [ct, a, b, c]
        dec_tgan.dectgan(dataset.matrix_per_celltypes[ct], a, b, c)

@eel.expose
def assessGAN():
    if(lastrun != None):
        count = []
        mtr = dataset.matrix_per_celltypes[lastrun[0]].copy()
        count.append(len(mtr))

        for i in range(lastrun[1], lastrun[2] + 1, lastrun[3]):
            mtr = pd.concat([mtr, pd.read_csv("./synthetic_data1000_epoch" +  str(i) + ".csv", header=0)])
            count.append(len(mtr))

        reducer = umap.UMAP(n_components=2, random_state=0, n_neighbors=10)
        x_embedded = reducer.fit_transform(mtr)
        return [lastrun, count, x_embedded.tolist()]

eel.init("web")
eel.start('main.html', size=(1440, 810))
