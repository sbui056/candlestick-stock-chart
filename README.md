# candlestick-stock-chart

Interative candlestick stock chart implemented using:
- Tkinter (for GUI prompting user input)
- Yahoo Finance (yfinance to pull stock data, providing data in a (Date, Open, High, Low, Close, Adj Close, Volume) table format in which we pulled (Open, High, Low, Close, Volume) to generate the candlestick subplot and then the volume subplot)
- Plotly (interactive graphing libary to generate the candlestick subplot + moving averages as a scatter and volume as bar subplot)
