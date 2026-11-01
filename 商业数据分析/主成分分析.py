import pandas as pd
import numpy as np

raw_data = pd.read_csv("Loan_aply.csv",encoding='gbk')
raw_data.head()
data = raw_data.loc[ :,'X1':]
data.corr(method='pearson')
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)
pca = PCA(n_components=5)
pca.fit(scaled_data)

# 输出主成分可解释变异
print('Explained variance: \n', pca.explained_variance_)  
# 输出可解释变异的比例
print('Explained variance ratio:\n', pca.explained_variance_ratio_) 
# 打印主成分向量
print('Principal Components: \n', pca.components_)
scaled_data[0]
raw_data[['ID']].join(pd.DataFrame(pca.transform(scaled_data)))
print('PCA_score of "ID=1":  %.4f'
      %np.dot(scaled_data[0], pca.components_[0]))
pca.set_params(n_components=1)
pca.fit(scaled_data)
data_pca = raw_data.join(
    pd.DataFrame(pca.transform(scaled_data), columns=['PCAScore']))

data_pca.head()
