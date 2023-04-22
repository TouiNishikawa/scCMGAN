from ctgan import CTGAN

def dectgan(df_celtype, epoch_start, epoch_end, epoch_term):
    ctgan = CTGAN()
    for i in range(epoch_start, epoch_end + 1, epoch_term):
        if i != epoch_start:
            ctgan = CTGAN().load('./model_ctgan_epoch' + str(i-epoch_term) +'.pkl')
        
        ctgan.fit(df_celtype, epochs=epoch_term)
        ctgan.save('./model_ctgan_epoch' + str(i) +'.pkl')

        synthetic_data = ctgan.sample(1000)
        synthetic_data.to_csv("./synthetic_data1000_epoch" +  str(i) + ".csv", index= False)
        
        synthetic_data = ctgan.sample(2000)
        synthetic_data.to_csv("./synthetic_data2000_epoch" +  str(i) + ".csv", index= False)
        
        synthetic_data = ctgan.sample(3000)
        synthetic_data.to_csv("./synthetic_data3000_epoch" +  str(i) + ".csv", index= False)
        
        synthetic_data = ctgan.sample(4000)
        synthetic_data.to_csv("./synthetic_data4000_epoch" +  str(i) + ".csv", index= False)

