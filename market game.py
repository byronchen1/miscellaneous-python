import json
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import plotly.graph_objects as go


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
        return self.sample_data_hidden['Close'][:self.days_elapsed]

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



if __name__ == "__main__":
    mg = market_game()

    continue_playing = True
    while continue_playing:
        try:
            days_to_increment=input('Forward number of days?  Enter Q to quit game \n')
            chart = mg.latest_graph(int(days_to_increment))
            chart.show()
        except:
            continue_playing = False
