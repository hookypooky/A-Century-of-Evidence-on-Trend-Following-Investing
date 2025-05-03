# libraries

import pandas as pd
import numpy as np

# import file

fp = r"myfilepath"
monthly_returns = pd.read_csv(fp)

# functions to calculate stats

# calculate covariance matrix 

def covariance_matrix(data):
    
    # rolling data window to predict future volatility
    
    timeframe = 36                                   # calculate on past 3 years of dataframe
    window = data.drop(columns=['Date'])             # drop date column
    window = window.tail(timeframe)                  # take last x entries in df
    
    # calculate cov matrix
    
    cov_matrix = np.cov(window, rowvar=False)        # calculate cov matrix
    return cov_matrix                                # returns cov matrix
    
# calculate portfolio volatility

def port_vol(data, weights):

    cvm = covariance_matrix(data)
    
    portfolio_variance = np.dot(weights.T, np.dot(cvm, weights))
    portfolio_volatility = np.sqrt(portfolio_variance) * np.sqrt(12)

    return portfolio_volatility

# other functions

# take long or short positions in each of the 38 securities

def long_or_short(data, timeframe):
    
    data = data.tail(timeframe)                       # take last x entries of data
    data = data.drop(columns=["Date"])                # drop date column
    
    returns_window_1 = data + 1                       # add 1 to returns
    security_crs = returns_window_1.product()         # np array of cumulative product
    
    result = np.where(security_crs > 1, 0.01, -0.01)  # returns array of where momentum is pos/neg
    
    return result
    
# calculate annual vol of each security (in last 3 years), returned as np array 

def a_vol(data, timeframe):
    
    data = data.tail(timeframe)                       # take timeframe
    data = data.drop(columns=["Date"])                # drop date col
    
    return np.std(data, axis=0) * np.sqrt(12)         # calculate annual vol of each security in portfolio over last 3 years
    
# assign weights to each of the 38 to hit the same target vol

def weights(lsa, avol):
    
    return np.divide(lsa, avol)                       # divide array of l/s positions by annual volatility for each security (scale each security position by annual volatility)

# scale weights so it sums to same amount (ensures all momentum buckets are equal weighted)

def scale_weights(weights):
    
    n = 1/3                                           # want weights to sum to 1/3
    total = np.sum(weights)                           
    
    return weights * (n/total)

# generate momentum weights, returns weights for all 38 securities as np array depending on specified window

def momentum_strategy(data, window):
    
    lsa = long_or_short(data, window)                 # determine whether to take long or short positions in each security
    avol = a_vol(data, 36)                            # calculate annual volatilities of each security as np array
    
    unscaled_weights = weights(lsa, avol)             # scale the weights so they sum to 1/3
    
    return scale_weights(unscaled_weights)

# generate 1m weight

def one_month_strategy(data):
    
    window = 1
    return momentum_strategy(data, window)            

# generate 3m weight

def three_month_strategy(data):
    
    window = 3
    return momentum_strategy(data, window)            

# generate 12m weight

def twelve_month_strategy(data):
    
    window = 12
    return momentum_strategy(data, window)

# weights for portfolio

def get_weights(data):
    
    # weights for the different buckets
    
    one_month = one_month_strategy(data) 
    three_month = three_month_strategy(data) 
    twelve_month = twelve_month_strategy(data) 
    
    weights = np.add(one_month, three_month, twelve_month)
    
    # scale for target vol of 0.3
    
    tv = 0.3
    pv = port_vol(data, weights) 
    multiplier = tv/pv
    
    final_weights = weights * multiplier
    return final_weights
    
# saves pd dataframe of weights to an excel file

def save_weights(df, filename):
    df.to_excel(filename, index=False)
    
# returns empty df to store weights given a return dataset

def new_df(data):
    
    columns = data.columns.values.tolist()
    column_names = list(filter(lambda x: x != 'Date', columns))                                         # remove date column
    new_column_names = [s.append(" weight") for s in column_names]                               # rename columns
    
    df = pd.DataFrame(columns=new_column_names)
    
    return df

# for every new month, we want to calculate a new set of weights for each of the 38 securities (loop through dataset)

# returns a pd df of weights 
    
def generate_weights(data):
    
    # variables
    
    n = len(data)         # no. of entries of data in dataset 
    m = 36                # start 3 years into dataset (3 years cov matrix to calculate expected volatility)
    row_num = 0           # to append weights to dataframe
    
    # set up empty df to store weights
    
    empty_df = new_df(data)
    
    # loop
    
    while m <= n:
        
        data_window = data.head(m)                                             # take the first m entries of data only
        this_month_weights = get_weights(data_window)                          # generate weights on the first m entries of data
        this_month_weights = this_month_weights.to_numpy()                     # convert weights to np array
        
        # add weights to pd df
        
        empty_df.loc[row_num] = this_month_weights                             # append weights to weight dataframe
        
        # adjust variables 
        
        row_num += 1
        m += 1
    
    return empty_df

pd_df_wts = generate_weights(monthly_returns)

# print(type(pd_df_wts))
# print(type(monthly_returns))

# adjust both dfs to prepare for backtesting
    
    
# backtest

def backtest(returns, weights):
    
    # adjust both dfs to prepare for backtesting
    
    weights_window = weights.iloc[:-1,:]                     # remove last row of weights df, since that is weights for next month
    
    returns_window = returns.tail(len(weights_window))       # take relevant return window
    returns_window = returns_window.drop(columns=["Date"])   # drop Date column
    
    # adjust indexes and columns
    
    weights_window.index = returns_window.index
    
    
    # calculate port returns
    
    portfolio_returns = (returns_window * weights_window.values).sum(axis=1)
    
    portfolio_plus1 = (1 + portfolio_returns)
    
    cumulative_returns = portfolio_plus1.cumprod()
    
    
    # save_weights(portfolio_returns, 'port.xlsx')
    
    print(portfolio_returns)
    print(portfolio_plus1)
    print(type(portfolio_plus1))
    print(cumulative_returns)
    
    
    
    
    
    total_periods = len(portfolio_returns)
    annualized_return = (cumulative_returns.iloc[-1] ** (12 / total_periods)) - 1
    annualized_volatility = portfolio_returns.std() * (12 ** 0.5)
    
    print(f"Annualized Return: {annualized_return:.2%}")
    print(f"Annualized Volatility: {annualized_volatility:.2%}")

    


    # return print(portfolio_returns)
    
    
    
backtest(monthly_returns, pd_df_wts)
    

# save_weights(pd_df_wts, 'trend-following weights.xlsx')
