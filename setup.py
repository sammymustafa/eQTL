import matplotlib.pyplot as plt
import esm
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
import math
from Bio.PDB import PDBParser, PDBList
from sklearn.decomposition import PCA

# Pretrained model loading
esm6_model, esm6_alphabet = esm.pretrained.esm2_t6_8M_UR50D()
esm6_model.eval()

esm150_model, esm150_alphabet = esm.pretrained.esm2_t30_150M_UR50D()
esm150_model.eval()

# Amino Acid Name Mapping
AA_NAME_MAP = {
    'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
    'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
    'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 'TER':'*',
    'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M', 'XAA':'X'
