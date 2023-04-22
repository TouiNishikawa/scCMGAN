from ctgan import CTGAN
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
import numpy as np


class scCMGAN:
    def __init__(self, persent = 40):
        """
        Args:
          persent: persent of cell marker gene
        """
        self.persent = persent
        self.base_model = CTGAN()

    def select_biomarker(self, train_df, ct):
        feats = [f for f in train_df.columns if f not in ['cellType']]
        train_x, train_y = train_df[feats], train_df['cellType']
        X = StandardScaler().fit_transform(train_x.values)
        y = train_y.values
        y = np.where(y == ct, 1, 0)

        clf = Ridge().fit(X, y)

        importance = np.abs(clf.coef_)
        K = int(train_df.shape[1] * self.persent / 100)
        unsorted_max_indices = np.argpartition(-importance, K)[:K]

        biomarkers = list(train_x.columns[unsorted_max_indices])
        return biomarkers

    def fit(self, train_df, ct, epochs):
         """
         Args:
          train_df: table data for training
          ct: cellType which you want to generate
          epochs: epochs of training
         """
         df_celtype = train_df[train_df["cellType"]==ct]
         biomarkers = scCMGAN.select_biomarker(self, train_df, ct)

         not_biomarkers = [f for f in df_celtype.columns if f not in biomarkers]
         df_biomarker, df_not_biomarker = df_celtype[biomarkers], df_celtype[not_biomarkers]
         self.df_not_biomarker = df_not_biomarker.drop(columns='cellType')
         self.base_model.fit(df_biomarker, epochs=epochs)
         self.cellType = ct
         self.average_not_biomaeker = self.df_not_biomarker.median(axis=0)

    def sample(self, num_rows):
        """
        Args:
          num_rows: number of generated data
        """
        synthetic_data_biomarker = self.base_model.sample(num_rows)
        synthetic_data_not_biomarker = pd.DataFrame(columns=self.df_not_biomarker.columns)
        for _ in range(num_rows):
            synthetic_data_not_biomarker = synthetic_data_not_biomarker.append(self.average_not_biomaeker, ignore_index=True)

        ct_df = pd.DataFrame([self.cellType for i in range(num_rows)], columns=["cellType"])

        synthetic_data = pd.concat([ct_df, synthetic_data_biomarker, synthetic_data_not_biomarker], axis=1)

        return synthetic_data

    def save(self, path):
        """
        Args:
          path: save path for model
        """
        with open(path, mode='wb') as f:
            pickle.dump(self, f)

    def load(path):
        """
        Args:
          path: path to the saved model
        """
        with open(path, mode='rb') as f:
            model = pickle.load(f)
        return model
