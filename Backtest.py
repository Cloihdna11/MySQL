import pymysql
import pandas as pd
import numpy as np
import matplotlib as plt
from datetime import datetime
import dateutil.parser
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

pd.options.display.width = 0

#StartDate = datetime.date(2020, 6, 26)
#EndDate = datetime.date(2020, 7, 8)
MaxLegs = 4


us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())

def Run():
    StratDF = importStratDF()
    HistoricalDF = importHistoricalDF()
    TradeTable=PopulateTradeTable(StratDF,HistoricalDF)

def blackandscholes():
    return None

def importStratDF(Strategy_ID=4):

    dbcon = pymysql.connect('localhost', 'root', 'Nyc10016', 'karya')

    #selected_idx = input("Enter Index? ")

    #cursor = dbcon.cursor()
    
    try:
        SQL_Query = pd.read_sql_query(
            '''Select
            `Index`,
            Strategy_ID,
            Legs,
            StrategyName,
            OptionType,
            QuantityinDollars,
            TargetMoneyness,
            Maturity,
            cast(UnwindTime as unsigned integer) as UnwindTime,
            Underlying, Data
            from karya.strategy_list''', dbcon)

        StratDF = pd.DataFrame(SQL_Query, columns=['Index', 'Strategy_ID', 'Legs', 'StrategyName', 'OptionType', 'QuantityinDollars', 'TargetMoneyness', 'Maturity', 'UnwindTime', 'Underlying', 'Data'])
       # where Index=@selected_idx
        #cursor.execute(SQL_Query)
        #data = cursor.fetchone(selected_idx)  
        #print(data)
        query_str = "Strategy_ID== @Strategy_ID"    
        StratDF = StratDF.query(query_str, inplace=False)
        return StratDF
        print(StratDF)
    except Exception as e:
        print(e)
        print(StratDF)
        return StratDF
    
    dbcon.close()

def importHistoricalDF():
    
     dbcon = pymysql.connect('localhost', 'root', 'Nyc10016', 'karya')
     try:
        SQL_Query = pd.read_sql_query(      
        '''SELECT `ID`, Underlying, str_to_date(Date, '%m / %d / %Y') as Date, convert(`Underlying Price`, float4) UnderlyingPrice , convert(`30DAY_IMPVOL_90.0%MNY_DF`, float4) `30DAY_IMPVOL_90.0%MNY_DF`,
          convert(`30DAY_IMPVOL_95.0%MNY_DF`, float4) `30DAY_IMPVOL_95.0%MNY_DF`,convert(`30DAY_IMPVOL_100.0%MNY_DF`, float4) `30DAY_IMPVOL_100.0%MNY_DF`,
          convert(`30DAY_IMPVOL_105.0%MNY_DF`, float4) `30DAY_IMPVOL_105.0%MNY_DF`,convert(`30DAY_IMPVOL_110.0%MNY_DF`, float4) `30DAY_IMPVOL_110.0%MNY_DF`,
          convert(`3MTH_IMPVOL_90.0%MNY_DF`, float4) `3MTH_IMPVOL_90.0%MNY_DF`, convert(`3MTH_IMPVOL_95.0%MNY_DF`, float4) `3MTH_IMPVOL_95.0%MNY_DF`, 
          convert(`3MTH_IMPVOL_100.0%MNY_DF`, float4) `3MTH_IMPVOL_100.0%MNY_DF`, convert(`3MTH_IMPVOL_105.0%MNY_DF`, float4) `3MTH_IMPVOL_105.0%MNY_DF`,
          convert(`3MTH_IMPVOL_110.0%MNY_DF`, float4) `3MTH_IMPVOL_110.0%MNY_DF`, convert(`BEST_DIV_YLD`, float4) BEST_DIV_YLD, 
          convert(`EQY_DVD_YLD_IND_NET`, float4) EQY_DVD_YLD_IND_NET, convert(`BDVD_PROJ_DIV_AMT`, float4) BDVD_PROJ_DIV_AMT
          FROM karya.`historical_vol`''', dbcon)
        dbcon.close()
        HistoricalDF = pd.DataFrame(SQL_Query, columns = ['ID','Underlying','Date', 'UnderlyingPrice', '30DAY_IMPVOL_90.0%MNY_DF','30DAY_IMPVOL_95.0%MNY_DF','30DAY_IMPVOL_100.0%MNY_DF','30DAY_IMPVOL_105.0%MNY_DF','30DAY_IMPVOL_110.0%MNY_DF','3MTH_IMPVOL_90.0%MNY_DF','3MTH_IMPVOL_95.0%MNY_DF','3MTH_IMPVOL_100.0%MNY_DF','3MTH_IMPVOL_105.0%MNY_DF','3MTH_IMPVOL_110.0%MNY_DF','BEST_DIV_YLD','EQY_DVD_YLD_IND_NET','BDVD_PROJ_DIV_AMT'])        
        HistoricalDF.rename(columns  = {'UnderlyingPrice': 'UnderlyingPrice',
                                        '30DAY_IMPVOL_90.0%MNY_DF' : 'Vol_30_90',
                                        '30DAY_IMPVOL_95.0%MNY_DF' : 'Vol_30_95',
                                        '30DAY_IMPVOL_100.0%MNY_DF' : 'Vol_30_100',
                                        '30DAY_IMPVOL_105.0%MNY_DF' : 'Vol_30_105',
                                        '30DAY_IMPVOL_110.0%MNY_DF' : 'Vol_30_110',
                                        '3MTH_IMPVOL_90.0%MNY_DF' : 'Vol_90_90',
                                        '3MTH_IMPVOL_95.0%MNY_DF' : 'Vol_90_95'
                                         }, inplace = True)
        HistoricalDF.rename(columns  = {
                                       '3MTH_IMPVOL_100.0%MNY_DF' : 'Vol_90_100',
                                        '3MTH_IMPVOL_105.0%MNY_DF' : 'Vol_90_105',
                                        '3MTH_IMPVOL_110.0%MNY_DF' : 'Vol_90_110'
                                        }, inplace = True)
        print(HistoricalDF)
        return HistoricalDF
     except Exception as err: 
        exception_type = type(err).__name__
        print(exception_type)
        print(HistoricalDF)
        return HistoricalDF
     

def GetMaturityDate(trade_date, maturity_days):
    base = datetime.datetime(1900, 1, 1)
    date_time_obj = datetime.datetime.strptime(trade_date, '%m/%d/%Y')
    delta = date_time_obj - base + datetime.timedelta(days=maturity_days)
    maturity_date = base + delta
    return maturity_date

def spline_vol(strike, time, surface, times):
    spline_time = []
    spline_vol = []
 
    for t1, t2 in sorted(times.items(), key=lambda x: x[1]):
        strikes = [surface[t1]['C10_strike'], surface[t1]['C25_strike'], surface[t1]['ATM_strike'],
                   surface[t1]['P25_strike'], surface[t1]['P10_strike']]
        vols = [surface[t1]['C10_vol'], surface[t1]['C25_vol'], surface[t1]['ATM_vol'],
                surface[t1]['P25_vol'], surface[t1]['P10_vol']]
        if strikes == sorted(strikes):
            spline_time.append(t2)
            spline_vol.append(np.interp(strike, strikes, vols))
        elif strikes[::-1] == sorted(strikes):
            spline_time.append(t2)
            spline_vol.append(np.interp(strike, strikes[::-1], vols[::-1]))
        else:
            raise ValueError('Vol surface for not monotonic at {}'.format(t1))
    
    return np.interp(time, spline_time, spline_vol)

def GetVolSurface():
    #surface = {}
    #TimeList = ['2W', '1M', '2M', '3M', '6M', '1Y', '2Y']
    #VolList = ['C10_vol', 'C25_vol', 'ATM_vol', 'P25_vol', 'P10_vol']
    #MoneynessList = ['C10_strike', 'C25_strike', 'ATM_strike', 'P25_strike', 'P10_strike']

    #for time in TimeList:
    #    surface[time] =  {'C10_vol': 10.667499999999999, 'C25_vol': 10.35, 'ATM_vol': 10.3525, 'P25_vol': 10.91, 'P10_vol': 11.6825,
    #                  'C10_strike': 90, 'C25_strike': 95, 'ATM_strike':100, 'P25_strike': 105, 'P10_strike':110}

    surface = {'1M': {'C10_vol': 10.48, 'C25_vol': 10.41625, 'ATM_vol': 10.7675, 'P25_vol': 11.76875, 'P10_vol': 12.91,
                      'C10_strike': 90, 'C25_strike': 95, 'ATM_strike': 100, 'P25_strike': 105, 'P10_strike':110},
               '3M': {'C10_vol': 10.56, 'C25_vol': 10.655000000000001, 'ATM_vol': 11.2575, 'P25_vol': 12.675, 'P10_vol': 14.260000000000002,
                      'C10_strike':90, 'C25_strike': 95, 'ATM_strike': 100, 'P25_strike': 105, 'P10_strike':110},
               }

    return surface

def daterange(d1, d2):
    return (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days + 1))

def populate_trade_table_row(tradedate,stratrow,HistoricalDF):
    Underlying=stratrow['Underlying']
    query_str = "Underlying==@Underlying & Date==@tradedate"
    
    historicalDfRow = HistoricalDF.query(query_str, inplace=False)
    historicalSrRow=historicalDfRow.iloc[0]
    


    trade_row={'Date': tradedate,
                'Leg': stratrow['Legs'],
                'Strategy_Name': stratrow['StrategyName'],
                'OptionType': stratrow['OptionType'],
                'QuantityinDollars': stratrow['QuantityinDollars'],
                'TargetMoneyness': stratrow['TargetMoneyness'],
                'Maturity': stratrow['Maturity'],
                'UnwindTime': stratrow['UnwindTime'],
                'Underlying': stratrow['Underlying'], 
                'UnderlyingPrice': historicalSrRow.loc['UnderlyingPrice']
               }
    
    print(trade_row)
    print("\n")

    return trade_row

  #return={
                    #'Date':trade_date,
                    #'Leg': stratrow['Legs'],
                    #'StrategyName': stratrow['StrategyName'],
                    #'OptionType': stratrow['OptionType'],
                    #'QuantityinDollars': stratrow['QuantityinDollars'],
                    #'TargetMoneyness': stratrow['TargetMoneyness'],
                    #'Maturity': stratrow['Maturity'],
                    #'UnwindTime': stratrow['UnwindTime'],
                    #'UnderlyingPrice': historicalDfRow.loc['UnderlyingPrice'],
                    #'Timeseries' : {}
                    #}
def PopulateTradeTable(StratDF, HistoricalDF):
    DateList=HistoricalDF.Date.unique()
    DateList.sort()

    counter = 0
    TradeTable=[]
    try:
         for tradedate in DateList:
            for j, stratrow in StratDF.iterrows():


                counter+=1
                if counter >=10: break
                trade_row=populate_trade_table_row(tradedate,stratrow,HistoricalDF)
                TradeTable.append(trade_row)
                
                print(" ".join(str(key) + " " + " " + str(value) for key, value in trade_row.items()))

    except Exception as err: 
            exception_type = type(err).__name__
            print(exception_type)
    print(TradeTable)
    return TradeTable

#def PopulateTradeTable_BAD(StratDF, HistoricalDF):

#    tradeTableDF = pd.DataFrame(columns=['TradeID','Ticker', 'Index',	'Strategy',	'Legs',	'StrategyName','Underlying','OptionType',	'TargetMoneyness','Maturity','UnwindTime','QuantityinDollars',	'QuantityinShares','TradeDate',	'UnderlyingID',	'UnderlyingPrice',	'Strike',	'r','q', 'MaturityDate', 	'Moneyness',	'MaturityDay', 'Vol', 'OptionPrice'])

#    DateList=HistoricalDF.Date.unique()
#    DateList.sort()
#    counter = 0
#    TradeTable=[]
#    try:
#        date_delta = EndDate- StartDate
#        for tradedate in DateList:
#            for j, stratrow in StratDF.iterrows():
#                counter+=1
#                if counter >=10: break
#                new_trade = StratDF.loc[j]
#                print(new_trade) 
#                print('Check', new_trade==stratrow)
#                underlying = new_trade['Underlying']
#                print(underlying)
#                query_str = "Underlying=='SPX Index' & Date==@tradedate"
#                print(query_str)
#                historicalDfRow = HistoricalDF.query(query_str, inplace=False)
#                if historicalDfRow is None:
#                    continue
#                print(len(historicalDfRow))
#                # initialize important variables => please factor out to own function
#                leg= stratrow.loc['Legs']
#                UnderlyingPrice = historicalDfRow['UnderlyingPrice'].iloc[0]
#                print(UnderlyingPrice)
#                strike = np.round(UnderlyingPrice*stratrow['TargetMoneyness']/100,0)
#                print(strike)
#                moneyness = strike/UnderlyingPrice*100
#                print(UnderlyingPrice)
#                maturitydate = GetMaturityDate(tradedate,stratrow['Maturity'])
#                print(maturitydate)
#                time_to_maturity = stratrow['Maturity']/365
#                print(time_to_maturity)
#                times = {'1M': 1 / 12, '3M': 3 / 12}
#                surface = GetVolSurface()
#                print('strike=',strike)
#                print("----")
#                print('time_to_maturity=',time_to_maturity)
#                print("----")
#                print('surface',surface)
#                print("----")
#                print('times=',times)
#                print("----")
#                vol= spline_vol(moneyness, time_to_maturity, surface, times)
#                price= blackandscholes()
#                #Timeseries
#                unwind_time = stratrow['UnwindTime']
#                # sample datetime index
#                # ================================
#                start_unwind_date = datetime.datetime.strptime(tradedate,"%m/%d/%Y")
#                end_unwind_date=start_unwind_date + datetime.timedelta(days=5)

#                for evaldate in daterange (start_unwind_date,end_unwind_date):
#                    print(tradedate)
#                    query_str =  'Underlying==@underlying & Date==@tradedate'
#                    historicalDfRow = HistoricalDF.query(query_str, inplace=True)
#                    if historicalDfRow is None:
#                        continue
#                    historicalDfRow = historicalDfRow.iloc(0)
#                    surface = GetVolSurface()
#              ##    vol[evaldate]=blackandscholes()

#                NewTrade={
#                    'Date':tradedate,
#                    'Leg': stratrow['Legs'],
#                    'StrategyName': stratrow['StrategyName'],
#                    'OptionType': stratrow['OptionType'],
#                    'QuantityinDollars': stratrow['QuantityinDollars'],
#                    'TargetMoneyness': stratrow['TargetMoneyness'],
#                    'Maturity': stratrow['Maturity'],
#                    'UnwindTime': stratrow['UnwindTime'],
#                    'UnderlyingPrice': historicalDfRow.loc['UnderlyingPrice'],
#                    'Timeseries' : {}
#                    }
#                TradeTable.append(NewTrade)
#                    #'OptionPrice' : historicalDfRow['OptionPrice']
#                print("======")
#                print(TradeTable)
#                print("======")

            
   
if __name__== "__main__":
    try:
        Run()
    except Exception as err: 
        exception_type = type(err).__name__
        print(exception_type)
          
             

