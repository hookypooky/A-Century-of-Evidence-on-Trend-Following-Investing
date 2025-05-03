## A Century of Evidence on Trend-Following Investing


### _What did I do?_

This is an implementation of a trend-following strategy from a [research paper](https://fairmodel.econ.yale.edu/ec439/hurst.pdf) written by AQR Capital. It was later published in the Journal 
of Portfolio Management. 

This is a long-short strategy. It divides the portfolio into three equal-weighted buckets. Each bucket represents a 
different momentum timeframe: 1-month, 3-month, and 12-month.

For each timeframe, if a security shows positive momentum, it is held long; if negative, it is shorted. 
The portfolio is rebalanced monthly and scaled to a 30% target volatility, using the past 3 years of returns to estimate volatility. 
The strategy was backtested on 38 securities.

### _Why did I do this?_

- I had doubts about whether momentum/trend-following actually worked. 
- I wanted to see how it would perform on the out of sample data period of ~8 years (from 2017-2025). 
- I was curious about the risks of shorting. It has always seemed risky to me, given the potential for unlimited losses. 
Are trend signals accurate and strong enough to justify taking short positions?
- I liked the idea of using three momentum timeframes. 
I thought the diversification across short- and long-term signals would make the strategy safer by reducing volatility and 
improving risk-adjusted returns.
- I've been interested in market-neutral strategies for a while (even though this one isn’t strictly market neutral). 
I believed they could reduce portfolio volatility and boost Sharpe Ratios—which, when targeting volatility, can improve CAGR.



