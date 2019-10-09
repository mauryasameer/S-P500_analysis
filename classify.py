import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import pandas as pd
from tqdm import tqdm as tq
from sklearn import svm, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from matplotlib import style
style.use('ggplot')

class classification():

    def __init__(self):
        self.data = pd.read_csv('data.csv', 
                        index_col='date',
                        parse_dates=['date'])
        self.ticker = 'ACN'

    def driver(self):
        mainData = self.setData(self.data)
        # tickers, data = self.preprocessing(mainData)
        # X, Y, df = self.fsets(self.ticker,mainData)
        self.ml_test(self.ticker, mainData)
    def setData(self,data):
        main_df = pd.DataFrame()
        for i in tq(data['Name'].unique()):
            df = data[data['Name']==i]
            df.rename(columns = {'close':i}, inplace=True)
            df.drop(['open','high','Name','volume','low'], 1, inplace=True)
            
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')
        return main_df

    def preprocessing(self, ticker, data):
        '''
        ticker: the company for the analysis
        data: the whole data
        '''
        days = 7
        tickers = data.columns.values.tolist()
        data.fillna(0, inplace=True)
        for i in range(1, days+1):
            data['{}_{}d'.format(ticker,i)] = (data[ticker].shift(-i)- data[ticker])/data[ticker]
        data.fillna(0, inplace=True)
        return tickers, data
            
    def buy_hold(self, *args):
        cols = [c for c in args]
        req = 0.02
        for col in cols:
            if col>req:
                return 1
            if col< -req:
                return -1
        return 0

    def fsets(self, ticker, data):
        tickers, df = self.preprocessing(ticker, data)
    #     print(tickers)
        df[f'{ticker}_target'] = list(map(self.buy_hold,*[df[f'{ticker}_{i}d'] for i in range(1,8)]))
        vals = df[f'{ticker}_target'].values.tolist()
        str_vals = [str(i) for i in vals]
        print(f'Data Spread:', Counter(str_vals))
        df.fillna(0, inplace = True)
        df = df.replace([np.inf, -np.inf], np.nan)
        df.dropna(inplace=True)
        
        df_vals = df[[ticker for ticker in tickers]].pct_change()
        df_vals = df_vals.replace([np.inf, -np.inf],0)
        df_vals.fillna(0,inplace = True)
        
        X = df_vals.values
        Y = df[f'{ticker}_target'].values
        
        return X,Y, df

    def ml_test(self, ticker, data):
        X, Y, df = self.fsets(ticker, data)
        x_train, x_test, y_train, y_test = train_test_split(X, Y,
                                                         test_size=0.25)
        clf = neighbors.KNeighborsClassifier()

        clf2 = VotingClassifier([
                    ('lsvc', svm.LinearSVC()),
                    ('knn', neighbors.KNeighborsClassifier()),
                    ('rf', RandomForestClassifier())
        ])

        clf.fit(x_train, y_train)
        confi = clf.score(x_test, y_test)

        clf2.fit(x_train, y_train)
        confi2 = clf2.score(x_test, y_test)

        print(f'Accuracy:{confi}')
        print(f'Accuracy For 2nd Classifier:{confi2}')
        prediction = clf.predict(x_test)        
        prediction2 = clf2.predict(x_test)
        print('Prediction Values', Counter(prediction))
        print(f'Prediction Values For 2nd:{Counter(prediction2)}')
if __name__ == "__main__":
    c = classification()
    c.driver()