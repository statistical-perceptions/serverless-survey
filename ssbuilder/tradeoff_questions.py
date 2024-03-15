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

    def generate_figure(self,pretty_data_file,
                         slider_column='model_number', slider_label='Model',
                        x_col='metric', x_value1='accuracy', x_value1_hover='accurate',
                        x_value2='false_positive_rate', x_value2_hover='false positives',
                        y_col='percent', y_min=None, y_max=None, num_digits=1,
                        color_col='group', color_hover= 'people',
                        disable_zoom=True, default_selection=10):
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
        x_col : string
            name of column to use for the x axis 
        y_col : string
            name of column to use for the  y axis 
        x_value1 : same as the values of `x_col` in the data file
            first,second value to filter (left metric)
        x_value2 : same as the values of `x_col` in the data file
            first,second value to filter ( right metric)
        x_value1_hover, x_value2_hover : string
            noun versions to use in the hovertext
        y_min,y_max : numerical
            minimum and maximum values to fix the plot axies, if none, allow plotly to decide
        num_digits : num digits to display 
        color_col: string 
            name of colum to use for the colring of the bars 
        color_hover:
            hover text to use for groups created by color
        disable_zoom : bool
            disable the zoom on the generated plot
        default_selection :int
            model that is selected when laoding

        Returns
        -------
        fig : plotly figure object
            figure object based on parameters

        '''
        df = pd.read_csv(pretty_data_file)

        mask1 = df[x_col] == x_value1
        mask2 = df[x_col] == x_value2
        masked_df = df[mask1 | mask2].copy()
        masked_df['x_col_hover'] = masked_df[x_col].replace({x_value1: x_value1_hover,
                                                            x_value2: x_value2_hover})
        masked_df['group_hover'] = color_hover

        # create the bar
        fig = px.bar(masked_df, x=x_col, y=y_col, animation_frame=slider_column,  color=color_col,
                    barmode='group', custom_data=[slider_column, color_col, 'x_col_hover','group_hover'])
        
        # update hover text
        hover_template = (slider_label + ' %{customdata[0]} <br> %{y:.'+str(num_digits)
                          +'f}% %{customdata[2]} <br>' +
                        ' for %{customdata[1]} %{customdata[3]}<extra></extra>')
        fig.update_traces(hovertemplate=hover_template)

        # make the slider locatoin easier to access in the js for logging
        for frame in fig.frames:
            for bar in frame.data:
                bar.hovertemplate = hover_template
                bar.meta = {'slider_loc': bar.customdata[0][0]}

        fig["layout"].pop("updatemenus")  # optional, drop animation buttons
        fig.update_xaxes(fixedrange=disable_zoom)
        fig.update_yaxes(fixedrange=disable_zoom)

        # infer height from data if not provided
        if type(y_min)== type(None):
            y_min = masked_df[y_col].min()

        if type(y_max) == type(None):

            y_max = masked_df[y_col].max()
            
        fig.update_yaxes(range=[y_min, y_max])

        # FIXME: this could be better
        fig._layout_obj.sliders[0].active = default_selection
        
        return fig


class TradeoffLine():

    def __init__(self, logging_vars={'location_var_name': 'model_number', }):
        self.plot_logging_js = 'plot_log_tradeoff_line.js'
        self.question_form_elements = 'form_tradeoff.html'
        self.logging_vars = logging_vars


    def generate_figure(self,pretty_data_file, slider_label='Model', trace_col='metric',
                        x_col='model_number', trace_value1='accuracy', trace1_hover='accurate',
                        trace_value2='false_positive_rate', trace2_hover='false positives',
                        y_col='percent', y_min=None, y_max=None, num_digits=2,
                        color_col='group', color_hover='people', anchor_name='selected model',
                        disable_zoom=True, default_selection=10):
            '''
           
            make the lineplot
            
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
                name of colum to use for the colring of the lines
            color_hover : string
                noun to use for groups
            disable_zoom : bool
                disable the zoom on the generated plot
            anchor_name : string
                name for vertical bar
            default_selection :int
                model that is selected when laoding

            Returns
            -------
            fig : plotly figure object
            figure object based on parameters

            '''
            df = pd.read_csv(pretty_data_file)

            mask1 = df[trace_col] == trace_value1
            mask2 = df[trace_col] == trace_value2
            masked_df = df[mask1 | mask2].copy()
            masked_df['trace_col_hover'] = masked_df[trace_col].replace({trace_value1: trace1_hover,
                                                                    trace_value2: trace2_hover})
            masked_df['color_hover'] = color_hover
            # Create figure with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # create lines with custom data that can be used in the hover text
            line_traces = px.line(masked_df, x=x_col, y=y_col, line_dash=trace_col, color=color_col,
                                hover_name=trace_col, hover_data=[color_col],
                                  custom_data=[color_col, 'trace_col_hover', 'color_hover']).data
            
            # addthe line data as traces to teh figure on the secondary y axis (to allow different sets)
            for l_trace in line_traces:
                fig.add_trace(l_trace, secondary_y=True, )

            # the extra being empty suppresses the text outside the main box
            fig.update_traces(hovertemplate=("Model %{x} <br> %{y:."+str(num_digits) +
                             "f}% %{customdata[1]} for %{customdata[0]} %{customdata[2]}<extra></extra>"))
            
            # infer height from data 
            if type(y_min)== type(None):
                y_min = masked_df[y_col].min()

            if type(y_max) == type(None):

                y_max = masked_df[y_col].max()

            # set number of points in vertical line to make more hover-able locations
            N_points = 100
            # Add vertical lines one for each alpha
            for anchor_loc, df_i in masked_df.groupby(x_col):
                # get the metrics for this model out
                metric_df = df_i[[y_col,trace_col,color_col,'color_hover']].rename(columns={'trace_col_hover':trace_col})
                # make renaming dictionary
                pivot_cols = {g:' '.join([g,color_hover]) for g in metric_df[color_col].unique()}
                # pivot, reset index to flatten heading from mulitindex and rename columns
                metric_pivot = metric_df.pivot(index=trace_col,columns=color_col, values=y_col).reset_index().rename(
                                columns = pivot_cols)
                # cast to string with float formatting and replace newlines with html breaks
                metric_tbl = metric_pivot.to_string(index=False,
                                                     float_format=lambda f:str(np.round(f,num_digits))).replace('\n','<br>')
                # add vertical line of a number of points, 
                #  store meta data so that the cloation can be picked out with js in the page
                fig.add_trace(
                    go.Scatter(
                        visible=False,
                        line=dict(color="#666666", width=6),
                        name= anchor_name, 
                        meta ={'location':str(anchor_loc)},
                        x= [anchor_loc]*N_points,
                        y=np.linspace(y_min, y_max, num=N_points),
                        hovertemplate="<b>Model %{x}</b> <br><br>" + metric_tbl + '<extra></extra>'), 
                    secondary_y=False)

            # Make 10th trace visible
            fig.data[default_selection].visible = True

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
                active=default_selection,
                currentvalue={"prefix": slider_label + ":"},
                pad={"t": 50},
                steps=steps
            )]

            fig.update_layout(
                sliders=sliders,
                legend_title_text=', '.join([color_col, trace_col]).title()
            )

            x_min=masked_df[x_col].min()
            x_max=masked_df[x_col].max()
            fig.update_xaxes(fixedrange = disable_zoom, 
                             range = [x_min, x_max])
            fig.update_yaxes(fixedrange=disable_zoom,
                             range=[y_min, y_max])
            return fig
