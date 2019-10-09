import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from volatility_index_utils import *
style.use('ggplot')


class plotting():
    
    def __init__(self):
        pass
    def plotting(self, data):
        
        data=self.add_vola_params(data)
        # print(nd.head())
        fig = plt.figure(figsize=(20,10))

        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        ax1.title.set_text(data['Name'][0])
        ax1.plot(data.index, data['close'])
        ax1.plot(data.index, data['average_true_range'])
        ax1.plot(data.index, data['donchian_channel_hband'])
        ax1.plot(data.index, data['donchian_channel_lband'])
        ax1.plot(data.index, data['bollinger_lband'])
        ax1.plot(data.index, data['bollinger_hband'])
        ax1.legend()
        ax2.plot(data.index, data['volume'])
        plt.legend()
        plt.show()
    def add_vola_params(self,data):
        
        bolingerMav = bollinger_mavg(data['close'],n=7)
        bolingerUB = bollinger_hband(data['close'], n=7)
        bolingerLB = bollinger_lband(data['close'], n=7)
        ATR = average_true_range(data['high'], data['low'],
                                 data['close'], n=7)
        dc_hb = donchian_channel_hband(data['close'], n=7)
        dc_lb = donchian_channel_lband(data['close'], n=7)
        
        analysisTypes={'donchian_channel_hband':dc_hb, 
                       'donchian_channel_lband':dc_lb, 
                       'average_true_range':ATR, 
                        'bollinger_hband':bolingerUB,
                       'bollinger_lband':bolingerLB, 
                       'bollinger_mavg':bolingerMav}
        for i in analysisTypes:
            data[i] = analysisTypes[i]
            
            
        
        return data
    
    
if __name__ == "__main__":
    p = plotting()
    LOCATION='./data.csv'
    data = pd.read_csv(LOCATION, 
        index_col='date',
        parse_dates=['date']
        )
    p.plotting(data[data['Name']=='AAL'])