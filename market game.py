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
        rand_start_date = np.random.randint(0, len(df) - 755)
        self.random_year_data = df[rand_start_date:rand_start_date + 755].reset_index()

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
            if (buy>0 and abs(buy) < (self.cash * 2 + (self.shares * self.closing_price()))):
                self.cash -= buy
                self.shares += int(action_shares)
        except:
            pass

    def sell(self, action_shares):
        # No short selling
        try:
            sell=self.closing_price()*int(action_shares)
            if (sell>0 and self.shares >= int(action_shares)):
                self.cash += sell
                self.shares -= int(action_shares)
        except:
            pass

    def balances(self):
        cash = round(self.cash,2)
        shares = self.shares
        price = self.closing_price()
        equity = round(cash+(shares*price),2)
        days = 756 - mg.days_elapsed
        bh_equity = round((10000 / self.sample_data_hidden["Close"][503]) * float(self.sample_data_hidden["Close"][self.days_elapsed-1]),2)
        alpha = round(equity - bh_equity,2)
        alpha_pct = round((equity - bh_equity)/bh_equity,2)

        return f'Cash: {cash} | Shares {shares} | Price {price}' \
               f'\n Equity {equity} | Days Remaining {days}' \
               f'\n Benchmark Equity {bh_equity} | Alpha {alpha} | A% {alpha_pct}' \
               f'\n\n Enter share quantity to Buy & Sell' \
               f'\n Trade an unknown stock | Time frame = 1 year' \
               f'\n Max Leverage = 2x | No Short Selling' \
               f'\n Benchmark Equity = Buy at T-0 & Hold' \
               f'\n Ticker & Date Range revealed at the end'

    def latest_graph(self, days=0):
        try:
            if days > 0:
                self.days_elapsed += int(days)
                if self.days_elapsed >= 756:
                    self.days_elapsed = 756
        except:
            self.days_elapsed += 0

        if self.days_elapsed < 756:
            return self._generate_visual_hidden()
        if self.days_elapsed >= 756:
            return self._finished_game()

    def show_chart(self):
        if self.days_elapsed < 756:
            self._generate_visual_hidden().show()
        if self.days_elapsed >= 756:
            self._finished_game().show()



if __name__ == "__main__":
    # Start Game
    mg = market_game()

    root = tk.Tk()
    root.title('Market Game')
    root.geometry('380x180')
    root.iconbitmap('stonks.ico')

    # Update Cash & Holdings
    def reconfig_bal(days_delta=0):
        mg.latest_graph(days_delta)
        b=mg.balances()
        bal_label.config(text=b)

    # Display chart
    button_px=3
    button_py=3
    button = tk.Button(root, text='View Chart', command=mg.show_chart)
    button_1d = tk.Button(root, text='+1 day', command=lambda: reconfig_bal(1))
    button_5d = tk.Button(root, text='+5 days', command=lambda: reconfig_bal(5))
    button_20d = tk.Button(root, text='+20 days', command=lambda: reconfig_bal(20))
    button_max = tk.Button(root, text='Skip to final', command=lambda: reconfig_bal(252))
    button.grid(row=0, column=0, padx=button_px, pady=button_py)
    button_1d.grid(row=1, column=0, padx=button_px, pady=button_py)
    button_5d.grid(row=2, column=0, padx=button_px, pady=button_py)
    button_20d.grid(row=3, column=0, padx=button_px, pady=button_py)
    button_max.grid(row=4, column=0, padx=button_px, pady=button_py)

    # Update Cash & Holdings
    def reconfig_bal_buy():
        mg.buy(entry_shares.get())
        b=mg.balances()
        bal_label.config(text=b)

    def reconfig_bal_sell():
        mg.sell(entry_shares.get())
        b=mg.balances()
        bal_label.config(text=b)

    # Buying/Selling shares
    button_px=3
    button_py=3
    entry_shares = tk.Entry(root, width=10, borderwidth=5)
    button_buy = tk.Button(root, text='Buy Shares', command=reconfig_bal_buy)
    button_sell = tk.Button(root, text='Sell Shares', command=reconfig_bal_sell)
    entry_shares.grid(row=0, column=1, padx=button_px, pady=button_py)
    button_buy.grid(row=0, column=2, padx=button_px, pady=button_py)
    button_sell.grid(row=0, column=3, padx=button_px, pady=button_py)

    # Cash & Holdings
    b=mg.balances()
    bal_label = tk.Label(root, text=b)
    bal_label.grid(row=1, column=1, padx=button_px, pady=button_py, columnspan = 3, rowspan=4)

    root.mainloop()
