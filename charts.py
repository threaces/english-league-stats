import plotly.express as px
import plotly.graph_objects as go
from constant_variables import PIE_CHART_WIDTH, PIE_CHART_HEIGHT 

class Figure:

    def __init__(self, data, chart_type, chart_config):
        self.data = data
        self.chart_type = chart_type
        self.chart_config = chart_config

    def get_figure(self):
        if self.chart_type == 'pie':
            fig = px.pie(self.data, values=self.chart_config['Values'], names=self.chart_config['Labels'], color=self.chart_config['Labels'], color_discrete_sequence=self.chart_config["colors"])

            fig.update_traces(marker={'line': {'color':'#000000', 'width':3}}, textfont_size=14)
            fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0,0,0,0)')
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            fig.update_layout(width=PIE_CHART_WIDTH, height=PIE_CHART_HEIGHT)
            fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font={'color':'#F4EBEB', 'size':12}))
        elif self.chart_type == 'scatter':
            fig = px.scatter(self.data, x=self.chart_config['x'], y=self.chart_config['y'], color=self.chart_config['pos'], height=1080, symbol=self.chart_config['pos'], size=self.chart_config['x'])
            fig.update_traces(dict(line=dict(width=4.5, color='DarkSlateGrey')))
            fig.update_layout(plot_bgcolor='rgba(255, 255, 255, 0)', paper_bgcolor='rgba(255,255,255,0)')
            fig.update_layout(font_family='Courier New', font_color='#F4EBEB', font_size=14)
        elif self.chart_type == 'bar':
            fig = px.bar(self.data, x=self.chart_config['x'], y=self.chart_config['y'], orientation='h', height=800)
            fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0,0,0,0)')
            fig.update_layout(font_family='Courier New', font_color='#F4EBEB', font_size=14)    
        elif self.chart_type == 'table':
            headerColor = 'green'
            rowEvenColor = '#504E4E'
            rowOddColor = '#504E4E'

            fig = go.Figure(data=[go.Table(
                header=dict(
                    values=self.chart_config['index'],
                    line_color='#F4EBEB',
                    fill_color=headerColor,
                    align=['left','center'],
                    font=dict(color='#F4EBEB', size=18, family='Courier New')
            ), cells=dict(
                values=[
                self.chart_config['Player Names'],
                self.chart_config['Goals'],
                self.chart_config['Assists'],
                self.chart_config['Canadian Clasification']],
                line_color='#F4EBEB',
                # 2-D list of colors for alternating rows
                fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
                align = ['left', 'center'],
                font = dict(color = '#F4EBEB', size = 14, family = 'Courier New'))
            )])

            fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0,0,0,0)')

        return fig