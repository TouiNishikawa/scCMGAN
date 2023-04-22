# dectgan
![画像2](https://user-images.githubusercontent.com/40726615/211593936-1fa5e05b-d6b3-49d2-93b1-dc28912231ac.png)

# Sample data
Download the sample of single RNA sequence data from "example" folder. (１)

# Installation
Install our liblary by this code. 
 
```bash
pip install  git+https://github.com/TouiNishikawa/dectgan.git
```
 
# Usage
training (from epoch:50 to epoch 250, per 50 epoch, celltype to augment: ductal, num of data to generate) 
```bash
import dectgan
dectgan.train('./baron_train_1_2.csv', 50, 251, 50, "ductal", 1000)
```

After training, you can adjust the data by this code. (for deconvolution)
```bash
dectgan.train2train_aug('./baron_train_1_2.csv','./baron_pDataC_1_2.csv', 1000, 250)
```

# Software
In the directory "softaware", run the run.py file.
```bash
Python run.py
```
![画像3](https://user-images.githubusercontent.com/40726615/211597675-ae051a46-3443-4e0c-ae74-9670f6ec0996.png)

# Reference
1. Baron, M. et al. A single-cell transcriptomic map of the human and mouse pancreas reveals inter- and intra-cell population structure. Cell Syst. 3, 346–360.e4 (2016).
2. Avila Cobos, Francisco, et al. "Benchmarking of cell type deconvolution pipelines for transcriptomics data." Nature communications 11.1 (2020): 1-14.
