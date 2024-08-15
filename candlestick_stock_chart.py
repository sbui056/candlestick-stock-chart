import datetime as dt
import yfinance as yf
import plotly.graph_objects as go
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog

def submit():
    """Handle submission of data"""
    global stockTicker, startDate, endDate
    stockTicker = stockTicker_entry.get().upper()
    startDate_str = start_input.get()
    endDate_str = end_input.get()
    
    if not stockTicker or not startDate_str or not endDate_str:
        messagebox.showerror("Error", "All fields are required.")
        return
    
    try:
        startDate = parse_date(startDate_str)
        endDate = parse_date(endDate_str)
        if startDate > endDate:
            raise ValueError("Start date cannot be after end date.")
    except ValueError as ve:
        messagebox.showerror("Error", f"Invalid date or date range: {ve}")
        return
    
    # Close GUI and proceed with data fetching
    root.quit()

def parse_date(date_string):
    """Parse date string to datetime object."""
    return dt.datetime.strptime(date_string, '%Y-%m-%d')

# Create the main root window
root = tk.Tk()
root.title("Stock Data Input")
root.geometry("800x400")
root.configure(background="purple")

# Add labels and entry fields
tk.Label(root, text="Enter a stock ticker:", font=('Comic Sans MS', 14), bg="purple", fg="white").pack(pady=10, padx=10)
stockTicker_entry = tk.Entry(root, font=('Comic Sans MS', 14), borderwidth=2, relief='groove', width=35)
stockTicker_entry.pack(pady=10, padx=10)

tk.Label(root, text="Enter the start date (YYYY-MM-DD):", font=('Comic Sans MS', 14), bg="purple", fg="white").pack(pady=10, padx=10)
start_input = tk.Entry(root, font=('Comic Sans MS', 14), borderwidth=2, relief='groove', width=35)
start_input.pack(pady=10, padx=10)

tk.Label(root, text="Enter the end date (YYYY-MM-DD):", font=('Comic Sans MS', 14), bg="purple", fg="white").pack(pady=10, padx=10)
end_input = tk.Entry(root, font=('Comic Sans MS', 14), borderwidth=2, relief='groove', width=35)
end_input.pack(pady=10, padx=10)

# Add submit button
submit_button = tk.Button(root, text="Submit", command=submit, font=('Comic Sans MS', 14))
submit_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()

# Load data for the specific stock
try:
    df = yf.download(stockTicker, start=startDate, end=endDate)
    if df.empty:
        raise ValueError("No data found for the given stock ticker and date range.")
except Exception as e:
    messagebox.showerror("Error", f"Error downloading data: {e}")
    exit(1)

# Ensure working with a copy and reorder the 4 crucial columns
df = df.copy()  # Ensure you're working with a copy of the DataFrame
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)

# Plot using Plotly for interactivity
fig = go.Figure(data=[go.Candlestick(x=df.index,
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']),
                      go.Scatter(x=df.index, y=df['close'].rolling(window=20).mean(), line=dict(color='blue', width=1.5), name='20-day MA'),
                      go.Scatter(x=df.index, y=df['close'].rolling(window=50).mean(), line=dict(color='orange', width=1.5), name='50-day MA')])

fig.update_layout(title=f'{stockTicker} Interactive Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
fig.show()
