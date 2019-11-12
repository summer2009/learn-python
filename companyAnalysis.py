import numpy as np
import pandas as pd

data=pd.read_csv('D:\\eastmoney\\业绩报表2012.csv')#读取csv文件
data[data['roeweighted'] == '-']=0
print(data[data['roeweighted'].astype('float') > 40.0])
