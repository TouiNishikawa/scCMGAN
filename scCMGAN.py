import pandas as pd
from ctgan import CTGAN
import time

def train(df_path, epoch_start, epoch_end, epoch_term, ct, data_num):
    df = pd.read_csv(df_path, header=None)
    ctgan = CTGAN()
    df.iloc[0, 0] = "cellType"
    df = df.T
    df.columns = df.iloc[0]
    df = df.drop(df.index[[0]])
    df_celtype = df[df["cellType"]==ct]

    for i in range(epoch_start, epoch_end, epoch_term):
        print(int(i) + "/" +str(epoch_end))
        discrete_columns = [
            "cellType"
        ]
        if i!= 50:
            ctgan = CTGAN().load('./model_ctgan_epoch' + str(i-50) +'.pkl')
        ctgan.fit(df_celtype, discrete_columns, epochs=epoch_term)
        ctgan.save('./model_ctgan_epoch' + str(i) +'.pkl')

        synthetic_data = ctgan.sample(data_num)
        synthetic_data.to_csv("./synthetic_data" + str(data_num) + "_epoch" +  str(i) + ".csv", index= False)


def train2train_aug(train_data_path, pheno_data_path, num_data, epoch):
    df = pd.read_csv(train_data_path, header=None)
    df.iloc[0, 0] = "cellType"
    df = df.T
    df.columns = df.iloc[0]
    df = df.drop(df.index[[0]])

    synthetic_data = pd.read_csv('./synthetic_data' + str(num_data) + '_epoch' +  str(epoch) + '.csv')

    # 縦横反転、整数変換
    df_concat_multi = pd.concat([df, synthetic_data])
    df_concat_multi_T = df_concat_multi.T
    df_concat_multi_T[1:] = df_concat_multi_T[1:].round().astype(int)

    # 行名の調整
    df = pd.read_csv(train_data_path, header=None)
    gene_pd = df[0]
    df_concat_multi_T.set_axis(gene_pd, inplace=True)

    # 列名の調整
    sh=df_concat_multi_T.shape
    df_concat_multi_T.columns=range(sh[1])
    df_concat_multi_T.columns = df_concat_multi_T.iloc[0]
    df_concat_multi_T = df_concat_multi_T.drop(df_concat_multi_T.index[[0]])

    # 負のデータの削除
    df_concat_multi_T = df_concat_multi_T.clip(lower=0)

    # 出力
    df_concat_multi_T.to_csv('baron_train1_2_aug_data' + str(num_data) + '_epoch' +  str(epoch) + '.csv', header=True, index=True)
    print('"baron_train1_2_aug_data' + str(num_data) + '_epoch' +  str(epoch) + '.csv"'+ 'was exported.')

    # データ生成分のpheno data
    df_p = pd.read_csv(pheno_data_path)
    indiv = ["indiv5"]
    indiv *= df_concat_multi_T.shape[1] - df.shape[1]+1
    df_p_new = pd.DataFrame(
        data={'cellID': list(range(1,num_data+1)),
            'cellType': synthetic_data["cellType"],
            'sampleID': indiv}
    )

    # 結合
    df_p_concat = pd.concat([df_p, df_p_new])
    df_p_concat = df_p_concat.drop(df_p_concat.columns[[0]], axis=1)
    df_p_concat[""] = list(range(1,df_p_concat.shape[0]+1))
    df_p_concat = df_p_concat.reindex(columns=['', 'cellID', 'cellType',	'sampleID'])

    df_p_concat.to_csv('./baron_pDataC_1_2_aug_data' + str(num_data) + '_epoch' +  str(epoch) + '.csv', header=True, index=False)
    print('"baron_pDataC_1_2_aug_data' + str(num_data) + '_epoch' +  str(epoch) + '.csv"'+ 'was exported.')
