from tqdm import tqdm as tq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from detailed_vola import plotting
from volatility_index_utils import *
class TopTen():

    def __init__(self):
        self.LOCATION='./data.csv'
        self.data = pd.read_csv(self.LOCATION, 
        index_col='date',
        parse_dates=['date']
        )
        self.CompaniesNames=self.data['Name'].unique()
        self.CompanyWiseData={}
        self.ATRWEEKLY={}
        self.ATRANNUALLY={}
        self.p = plotting()
        # print(self.CompaniesNames)

    def CompanyNames(self):
        # print(self.CompaniesNames)
        for i in tq(self.CompaniesNames):
            self.CompanyWiseData[i] = self.data[self.data['Name']==i]    
        # self.FindTop()
        # self.FindBottomTen()
        self.TopAndBottom()
    def TopAndBottom(self):
        for i in tq(self.CompaniesNames):
            self.ATRWEEKLY[i] = average_true_range(
                self.CompanyWiseData[i]['high'],
                self.CompanyWiseData[i]['low'],
                self.CompanyWiseData[i]['close'],
                n=7
            ).mean()
            self.ATRANNUALLY[i] = average_true_range(
                self.CompanyWiseData[i]['high'],
                self.CompanyWiseData[i]['low'],
                self.CompanyWiseData[i]['close'],
                n=265
            ).mean()
        self.WeeklySorted = sorted(self.ATRWEEKLY.items(),
                                    key = lambda x:x[1])
        self.AnnualySorted = sorted(self.ATRANNUALLY.items(),
                                    key = lambda x:x[1])
        # print(f"top ten Weekly volatile companies are {self.WeeklySorted[:10] }")
        # print(f"top ten Weekly least volatile companies are {self.WeeklySorted[-10:] }")
        # print(f"top ten Anually volatile companies are {self.AnnualySorted[:10] }")
        # print(f"top ten Anually least volatile companies are {self.AnnualySorted[-10:] }")
        topwL_name,topwL_value = self.namesAndValue(self.WeeklySorted[:10])
        topaL_name,topaL_value = self.namesAndValue(self.AnnualySorted[:10])
        topw_name,topw_value = self.namesAndValue(self.WeeklySorted[-10:])
        topa_name,topa_value = self.namesAndValue(self.AnnualySorted[-10:])
        

        self.plotting([topa_name, topa_value,
                        topw_name, topw_value,
                        topaL_name, topaL_value,
                        topwL_name, topwL_value])
        print(topa_name)
        self.p.plotting(self.CompanyWiseData[topa_name[0]])
        self.p.plotting(self.CompanyWiseData[topaL_name[0]])



    def namesAndValue(self,val):
        names = [i[0] for i in val]
        values = [i[1] for i in val]
        return names,values

    def plotting(self, data):

        fig = plt.figure(figsize=(20,10))
        # ax1 = plt.subplot2grid((8,2),(0,0), rowspan=3, colspan=10)

        # ax2 = plt.subplot2grid((8,2), (0,4), rowspan=3, colspan=10,sharex=ax1)
        # plt.title('')
        ax1 = fig.add_subplot(221)
        ax3 = fig.add_subplot(222)
        ax2 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224) 
        ax3.title.set_text('TOP 10 MOST VOLATILE STOCKS WEEKLY')
        ax4.title.set_text('TOP 10 MOST VOLATILE STOCKS ANNUALY')
        ax1.title.set_text('TOP 10 LEAST VOLATILE STOCKS WEEKLY')
        ax2.title.set_text('TOP 10 LEAST VOLATILE STOCKS ANNUALY')
        

        ax1.bar(data[0], data[1])
        # ax1.xaxis('Date')
        ax2.bar(data[2], data[3])
        ax3.bar(data[4],data[5])
        ax4.bar(data[6],data[7])

        plt.show()



if __name__ == "__main__":
    tt = TopTen()
    tt.CompanyNames()
    # p = plotting()
    # p.plotting(tt.CompanyWiseData['AAL'])