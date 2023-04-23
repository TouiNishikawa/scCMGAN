# sc-CMGAN (stepwise Generative Adversarial Network based on Cell Markers for Single Cell genomics data)
![画像1](https://user-images.githubusercontent.com/40726615/233799014-9cb6d659-f40f-460d-b4ed-94743892efe8.png)


# Sample data
Use the sample of single RNA sequence data in "example" folder.

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
install some libraries
```bash
pip install ctgan
pip install eel
pip install pywin32
pip install umap-learn
```

In the directory "softaware", run the run.py file.
```bash
!git clone https://github.com/TouiNishikawa/scCMGAN.git
cd ./scCMGAN/software
py -3 run.py
```
![software](https://user-images.githubusercontent.com/40726615/233834332-df4f017a-9314-46d7-a128-3de26ec4491d.png)


# Reference
1. Baron, M. et al. A single-cell transcriptomic map of the human and mouse pancreas reveals inter- and intra-cell population structure. Cell Syst. 3, 346–360.e4 (2016).
2. Avila Cobos, Francisco, et al. "Benchmarking of cell type deconvolution pipelines for transcriptomics data." Nature communications 11.1 (2020): 1-14.
3. Xu, Lei, et al. "Modeling tabular data using conditional gan." Advances in Neural Information Processing Systems 32 (2019).
