import os
from datetime import datetime
import pandas as pd
import optopsy as op

##Source: https://github.com/michaelchu/optopsy##
   
    # set console width to autodetect data size
      
pd.options.display.width = 0

def filepath():
    curr_file = os.path.abspath(os.path.dirname(__file__))
   
    return os.path.join(curr_file, "data", "SPX_20151001_to_20151030.csv")

def run_strategy():
    data = pd.read_csv(
        filepath(), parse_dates=["expiration", "quotedate"], infer_datetime_format=True
    )
       
    # manually rename the data header columns to the standard column names as defined above
  
    data.rename(
        columns={
            'underlying': 'underlying_symbol',
            'underlying_last': 'underlying_price',
            'type': 'option_type',
            'quotedate': 'quote_date'
        },
 
        inplace=True)

    results = (
        data.start_date(datetime(2015, 10, 1))
            .end_date(datetime(2015, 10, 30))
            .entry_dte(31)
            .delta(0.50)
            .calls()
            .pipe(op.long_call)
            .pipe(op.backtest, data)
            .exit_dte(7)
    )
    print("Total trades: " + str(results.total_trades()))
    print("Total profit: " + str(results.total_profit()))
    #print(data)
    print(results)
   

if __name__ == "__main__":
    run_strategy()
