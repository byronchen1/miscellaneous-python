import json
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import plotly.graph_objects as go
import tkinter as tk


class market_game:
    def __init__(self):
        # list of tickers
        tickers = json.loads(open('tsx_tickers.json').read())

        # random ticker
        rand_ticker = np.random.randint(0, len(tickers))

        # any date after 2000
        start = '2000-01-01'
        end = pd.datetime.today().strftime("%Y-%m-%d")
        df = web.DataReader(tickers[rand_ticker], 'yahoo', start, end)
        df['Ticker'] = tickers[rand_ticker]

        # 252 = 1 year data, 252*2 = 504, 252*3= 756
        rand_start_date = np.random.randint(0, len(df) - 756)
        self.random_year_data = df[rand_start_date:rand_start_date + 756].reset_index()

        # display
        sample_data_hidden = self.random_year_data[['High', 'Low', 'Open', 'Close', 'Volume']]
        self.sample_data_hidden = sample_data_hidden.apply(lambda x: round(x, 2))
        self.sample_data_hidden['Volume_str'] = sample_data_hidden['Volume'].apply(
            lambda x: str(round(x / 1000000, 2)) + ' MM')
        self.days_elapsed = 504

        # starting holdings
        self.cash = 10000
        self.shares = 0

    def _generate_visual_hidden(self):
        # show 2 years of data
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=[i for i in range(self.days_elapsed)],
            y=self.sample_data_hidden['Close'][:self.days_elapsed],
            mode='lines+markers',
            text='Open: ' + self.sample_data_hidden['Open'][:self.days_elapsed].astype(str) + '<br>' + \
                 'Close: ' + self.sample_data_hidden['Close'][:self.days_elapsed].astype(str) + '<br>' + \
                 'High: ' + self.sample_data_hidden['High'][:self.days_elapsed].astype(str) + '<br>' + \
                 'Low: ' + self.sample_data_hidden['Low'][:self.days_elapsed].astype(str) + '<br>' + \
                 'Volume: ' + self.sample_data_hidden['Volume_str'][:self.days_elapsed].astype(str) + '<br>' + \
                 'Elapsed Days: ' + pd.Series([i for i in range(self.days_elapsed)]).astype(str) + '<br>'
        ))

        fig.update_layout(
            title={
                'text': 'Unknown Company performance' + '<br>' + \
                        f'{756 - self.days_elapsed} trading days remaining',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },

            yaxis_title='Price',
            xaxis_title='Days elapsed'
        )

        return fig

    def _finished_game(self):
        # show 2 years of data
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.random_year_data['Date'],
            y=self.random_year_data['Close'],
            mode='lines+markers'
        ))

        fig.update_layout(
            title={
                'text': f'Ticker: {self.random_year_data["Ticker"][0]}',
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },

            yaxis_title='Price',
            xaxis_title='Date'
        )

        return fig

    def closing_price(self):
        return float(self.sample_data_hidden['Close'][self.days_elapsed-1])

    def buy(self, action_shares):
        # Leverage at most 2x equity
        try:
            buy=self.closing_price()*int(action_shares)
            if abs(buy) < (self.cash * 2 + (self.shares * self.closing_price())):
                self.cash -= buy
                self.shares += int(action_shares)
        except:
            pass

    def sell(self, action_shares):
        # No short selling
        try:
            sell=self.closing_price()*int(action_shares)
            if self.shares >= int(action_shares):
                self.cash += sell
                self.shares -= int(action_shares)
        except:
            pass

    def balances(self):
        return f'Cash: {round(self.cash,2)} | Shares {self.shares} | Price {self.closing_price()}'

    def latest_graph(self, days=0):
        try:
            if days > 0:
                self.days_elapsed += int(days)
                if self.days_elapsed >= 756:
                    self.days_elapsed = 756
        except:
            self.days_elapsed += 0

        if self.days_elapsed < 756:
            #return self._generate_visual_hidden()
            self._generate_visual_hidden().show()
        if self.days_elapsed >= 756:
            #return self._finished_game()
            self._finished_game().show()



if __name__ == "__main__":
    # Start Game
    mg = market_game()

    root = tk.Tk()
    root.title('Market Game')
    root.geometry('380x170')
    root.iconbitmap('stonks.ico')

    # Display chart
    button_px=3
    button_py=3
    button = tk.Button(root, text='Show Chart', command=mg.latest_graph)
    button_5d = tk.Button(root, text='+5 days', command=lambda: mg.latest_graph(5))
    button_20d = tk.Button(root, text='+20 days', command=lambda: mg.latest_graph(20))
    button_80d = tk.Button(root, text='+80 days', command=lambda: mg.latest_graph(80))
    button_max = tk.Button(root, text='Skip to final', command=lambda: mg.latest_graph(252))
    button.grid(row=0, column=0, padx=button_px, pady=button_py)
    button_5d.grid(row=1, column=0, padx=button_px, pady=button_py)
    button_20d.grid(row=2, column=0, padx=button_px, pady=button_py)
    button_80d.grid(row=3, column=0, padx=button_px, pady=button_py)
    button_max.grid(row=4, column=0, padx=button_px, pady=button_py)

    # Buying/Selling shares
    button_px=3
    button_py=3
    shares_label = tk.Label(root, text='Enter shares')
    entry_shares = tk.Entry(root, width=10, borderwidth=5)
    button_buy = tk.Button(root, text='Buy', command=lambda: mg.buy(entry_shares.get()))
    button_sell = tk.Button(root, text='Sell', command=lambda: mg.sell(entry_shares.get()))
    shares_label.grid(row=0, column=1, padx=button_px, pady=button_py)
    entry_shares.grid(row=1, column=1, padx=button_px, pady=button_py)
    button_buy.grid(row=1, column=2, padx=button_px, pady=button_py)
    button_sell.grid(row=1, column=3, padx=button_px, pady=button_py)

    # Cash & Holdings
    b=mg.balances()
    bal_label = tk.Label(root, text=b)
    bal_label.grid(row=3, column=1, padx=button_px, pady=button_py)

    # Update Cash & Holdings
    def reconfig_bal():
        b=mg.balances()
        bal_label.config(text=b)

    update_bal_label = tk.Button(root, text = "Update Balances", command = reconfig_bal )
    update_bal_label.grid(row=2, column=1, padx=button_px, pady=button_py)

    # Leverage Rules
    rules_label = tk.Label(root, text='Max Leverage = 2x | No Short Selling')
    rules_label.grid(row=4, column=1, padx=button_px, pady=button_py)

    root.mainloop()
