import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm as tq
from matplotlib import style
style.use('ggplot')

class pairTrading():

    def __init__(self):
        self.data = pd.read_csv('data.csv', 
                            index_col='date',
                             parse_dates=['date'])

    
    def sorter(self):
        mainData=self.setData()
        # self.viz(mainData)
        all_corr = self.topAndLeastCorelated(mainData)
        print(f'least 5 are \n{all_corr[0:5]}')
        print(f'top 5 are \n{all_corr[-5:]}')
    def viz(self,data):
        corr = data.corr().values
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        
        heatmap = ax.pcolor(corr, cmap=plt.cm.RdYlGn)
        fig.colorbar(heatmap)
        ax.set_xticks(np.arange(corr.shape[0])+ 0.5, minor=False)
        ax.set_yticks(np.arange(corr.shape[1])+ 0.5, minor=False)
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        
        cols_labels = data.corr().columns
        row_labels = data.corr().index
        
        ax.set_xticklabels(cols_labels)
        ax.set_yticklabels(row_labels)
        plt.xticks(rotation=90)
        heatmap.set_clim(-1,1)
        plt.tight_layout()
        plt.show()

    def get_redundant(self,data):
        p2d=set()
        cols = data.columns
        for i in range(0, data.shape[1]):
            for j in range(0, i+1):
                p2d.add((cols[i], cols[j]))
        return p2d

    def topAndLeastCorelated(self, data):
        corrVals = data.corr().unstack()
        labelsToDrop = self.get_redundant(data)
        corrVals = corrVals.drop(labels= labelsToDrop).sort_values()
        return corrVals

    def setData(self):
        main_df = pd.DataFrame()
        for i in tq(self.data['Name'].unique()):
            df = self.data[self.data['Name']==i]
            df.rename(columns = {'close':i}, inplace=True)
            df.drop(['open','high','Name','volume','low'], 1, inplace=True)
            
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')
        return main_df

if __name__ == "__main__":
    p = pairTrading()
    p.sorter()