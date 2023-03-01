import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import norm


class TradeoffBar():
    def __init__(self, logging_vars={'location_var_name': 'model_number', }):
        self.plot_logging_js = 'plot_log_tradeoff_bar.js'
        self.question_form_elements = 'form_tradeoff.html'
        self.logging_vars = logging_vars

    def generate_figure(self,pretty_data_file, slider_column='model_number', slider_label='Model',
                        x_col='metric', x_value1='accuracy', x_value1_hover='accurate',
                        x_value2='false_positive_rate', x_value2_hover='false positives',
                        y_col='percent', y_min=None, y_max=None, num_digits=1,
                        color_col='group',
                        disable_zoom=True):
        '''
        make the barplot
        
        Parameters
        ----------
        pretty_data_file : string
            file name of a tidy (tall) dataset with pretty content. that is any data transformations
            should occur on the data (eg scaling .7523943 to 75.23943 and expanding column names)
            column names can still rely on python conventions, before display the `_` will be converted to space
        slider_column : string
            name of column to use for the slider
        slider_label : string
            name to display when labeling the slider postion values (and in hovertext)
        x_col,y_col : string
            name of column to use for the xor y axis 
        x_value1,x_value2 : same as the values of `x_col` in the data file
            first,second value to filter (left, right metric)
        x_value1_hover, x_value2_hover : string
            noun versions to use in the hovertext
        y_min,y_max : numerical
            minimum and maximum values to fix the plot axies, if none, allow plotly to decide
        num_digits : num digits to display 
        color_col: string 
            name of colum to use for the colring of the bars 
        disable_zoom : bool
            disable the zoom on the generated plot
        '''
        df = pd.read_csv(pretty_data_file)

        mask1 = df[x_col] == x_value1
        mask2 = df[x_col] == x_value2
        masked_df = df[mask1 | mask2].copy()
        masked_df['x_col_hover'] = masked_df[x_col].replace({x_value1: x_value1_hover,
                                                            x_value2: x_value2_hover})

        fig = px.bar(masked_df, x=x_col, y=y_col, animation_frame=slider_column,  color=color_col,
                    barmode='group', custom_data=[slider_column, color_col, 'x_col_hover']
                    )
        hover_template = (slider_label + ' %{customdata[0]} <br> %{y:.'+str(num_digits)
                          +'f}% %{customdata[2]} <br>' +
                        ' for %{customdata[1]} people<extra></extra>')
        fig.update_traces(hovertemplate=hover_template)

        for frame in fig.frames:
            for bar in frame.data:
                bar.hovertemplate = hover_template
                bar.meta = {'slider_loc': bar.customdata[0][0]}

        fig["layout"].pop("updatemenus")  # optional, drop animation buttons
        fig.update_xaxes(fixedrange=disable_zoom)
        fig.update_yaxes(fixedrange=disable_zoom)
        fig.update_yaxes(range=[y_min, y_max])
        
        return fig


class TradeoffLine():

    def __init__(self, logging_vars={'location_var_name': 'model_number', }):
        self.plot_logging_js = 'plot_log_tradeoff_line.js'
        self.question_form_elements = 'form_tradeoff.html'
        self.logging_vars = logging_vars


    def generate_figure(self,pretty_data_file, slider_label='Model', trace_col='metric',
                        x_col='model_number', trace_value1='accuracy', trace1_hover='accurate',
                        trace_value2='false_positive_rate', trace2_hover='false positives',
                        y_col='percent', y_min=None, y_max=None, num_digits=1,
                        color_col='group', anchor_name='selected model',
                        disable_zoom=True):
            '''
            make the barplot
            
            Parameters
            ----------
            pretty_data_file : string
                file name of a tidy (tall) dataset with pretty content. that is any data transformations
                should occur on the data (eg scaling .7523943 to 75.23943 and expanding column names)
                column names can still rely on python conventions, before display the `_` will be converted to space
            slider_column : string
                name of column to use for the slider
            slider_label : string
                name to display when labeling the slider postion values (and in hovertext)
            x_col,y_col : string
                name of column to use for the xor y axis 
            trace_value1,trace_value2 : same as the values of `x_col` in the data file
                first,second value to filter (left, right metric)
            trace1_hover, trace2_hover : string
                noun versions to use in the hovertext
            y_min,y_max : numerical
                minimum and maximum values to fix the plot axies, if none, allow plotly to decide
            num_digits : num digits to display 
            color_col: string 
                name of colum to use for the colring of the bars 
            disable_zoom : bool
                disable the zoom on the generated plot
            anchor_name : name for vertical bar
            '''
            df = pd.read_csv(pretty_data_file)

            mask1 = df[trace_col] == trace_value1
            mask2 = df[trace_col] == trace_value2
            masked_df = df[mask1 | mask2].copy()
            masked_df['trace_col_hover'] = masked_df[x_col].replace({trace_value1: trace1_hover,
                                                                    trace_value2: trace2_hover})
            # Create figure with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            line_traces = px.line(masked_df, x=x_col, y=y_col, line_dash=trace_col, color=color_col,
                                hover_name=trace_col, hover_data=[color_col],
                                custom_data=[color_col, 'trace_col_hover']).data

            for l_trace in line_traces:
                fig.add_trace(l_trace, secondary_y=True, )

            fig.update_traces(hovertemplate=("Model %{x} <br> %{customdata[1]:."+str(num_digits) +
                                            "f}% %{hovertext} for %{customdata[0]}"))
            
            # infer height from data 
            if type(y_min)== type(None):
                y_min = masked_df[y_col].min()

            if type(y_min) == type(None):
                y_min = masked_df[y_col].min()

            # Add vertical lines one for each alpha
            for anchor_loc in masked_df[x_col].unique():
                fig.add_trace(
                    go.Scatter(
                        visible=False,
                        line=dict(color="#666666", width=6),
                        name=anchor_name,
                        meta={'location': str(anchor_loc)},
                        x=[anchor_loc, anchor_loc],
                        hovertemplate="Model %{x} ",
                        y=[y_min, y_max]), secondary_y=False)

            # Make 10th trace visible
            fig.data[10].visible = True

            # Create and add slider
            steps = []
            offset = len(line_traces)
            for i in range(offset, len(fig.data)):
                #     overlap =
                step = dict(
                    method="update",
                    label=i-offset,
                    args=[{"visible": [True]*offset + [False] * len(fig.data)},
                        ],  # layout attribute {"title": "model"}
                )
                step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
                steps.append(step)

            sliders = [dict(
                active=10,
                currentvalue={"prefix": slider_label + ":"},
                pad={"t": 50},
                steps=steps
            )]

            fig.update_layout(
                sliders=sliders
            )

            fig.update_xaxes(fixedrange=disable_zoom)
            fig.update_yaxes(fixedrange=disable_zoom)
            fig.update_yaxes(range=[y_min, y_max])
            return fig
