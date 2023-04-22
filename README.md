# scCMGAN
![画像2](https://user-images.githubusercontent.com/40726615/211593936-1fa5e05b-d6b3-49d2-93b1-dc28912231ac.png)

# Sample data
Download the sample of single RNA sequence data from "example" folder. (１)

# Installation
Install our liblary by this code. 
 
```bash
pip install  git+https://github.com/TouiNishikawa/scCMGAN.git
```
 
# Usage
Please see the "Usage_notebook"
## load data
```bash
# Path to table data
df = pd.read_csv('./Example/Example_train.csv', header=None) 

# Name of dataset
data_set = "Example"

df.iloc[0, 0] = "cellType"
df = df.T
df.columns = df.iloc[0]
df = df.drop(df.index[[0]])

cellType = ["cell_1",
            "cell_2",
            "cell_3"]
```

## Training, saving, loading and generating
```bash
from scCMGAN import scCMGAN
# generate model
model = scCMGAN(persent = 40)

# finetuning model
model.fit(df, "cell_1", epochs=40)

# save model
model.save("saved_model.pkl")

# load model
model = scCMGAN.load("saved_model.pkl")

# generate data
synthetic_data = model.sample(10)
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
