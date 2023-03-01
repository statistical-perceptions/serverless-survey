import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import norm



class NormalCurveSlider():
    def __init__(self,logging_vars={'location_var_name': 'loc',
                               'overlap_var_name': 'ov'}):
        self.plot_logging_js = 'plot_log_normal_curve.js'
        self.question_form_elements = 'form_normal_curve.html'
        self.logging_vars =logging_vars

    def generate_figure(self,static_name='other group', static_color="#CE00D1", 
                            static_mean=80,static_curve_width=10,
                            dynamic_name='your group', dynamic_color="#00CED1", 
                            dynamic_starting_mean=10, dynamic_curve_width=10,
                            num_slider_locs=101,min_slider_value = None, max_slider_value=None,
                            overlap_decimals=2, mean_decimals=None, xaxis_title=''):
        '''
        Generate a normal curve question object on a default scale of 
        
        Parameters
        ----------
        static_name : string
            legend text for static curve
        static_color : hex including # 
            hex code for the color to use for static curve, including a # sign as the first character
        static_mean : number
            location of the static curve
        static_curve_width : number
            width of curve, as the scipy.norm scale
        dynamic_name : string
            legend text for dynamic curve
        dynamic_color : hex including #
            hex code for the color to use for dynamic curve, including a # sign as the first character
        dynamic_starting_mean : number
            the location where the slider starts
        curve_width : number
            width of curves 
        num_slider_locs : integer 
            number of slilder locations
        min_slider_value : number
            the minimum value for the slider
        max_slider_value : number
            the maximum value for the slider
        overlap_decimals : integer 
            number of place values to round the % overlap value to for both display and reporting,
            positive to the right of the decimal, negative for left of decimal (eg -2 rounds to nearest 100)
        mean_decimals : integer 
            number of place values to round the mean (position) value to for both display and reporting
            positive to the right of the decimal, negative for left of decimal (eg -2 rounds to nearest 100)
        xaxis_title : string 
            text label for the x axis
        Notes: 
        ------
        curve is drawn with scipy.norm 
        '''
        # fill in min/max if needed
        # None evaluates to False
        if not(min_slider_value) :
            min_slider_value = 0
        
        if not(max_slider_value):
            max_slider_value = num_slider_locs
        # compute the slider step size
        slider_step = (max_slider_value-min_slider_value)/num_slider_locs
        
        # update mean decimals base on step size  if not passed
        if not(mean_decimals):
            # if the step size is an integer, round the mean to integers, otherwise 2 places 
            if slider_step.is_integer():
                mean_decimals = 0
            else:   
                mean_decimals = 2

        # set x value
        shared_x = np.arange(min_slider_value, max_slider_value, slider_step)

        # convert the means to indices 


        # convenience function for nomal curve
        curve_func = lambda mu,cw: norm.pdf(shared_x,loc=mu,scale=cw)
        # compute the curves, first fixted then a list of the dynamic
        fixed_curve = curve_func(static_mean,static_curve_width)
        dynamic_curves = [curve_func(mu,dynamic_curve_width) for mu in shared_x]
        # comput overlap by ~ integrating the minimum value over the window size for each dynamic with the static
        overlap_raw = [np.sum(np.min([fixed_curve,cur_curve],axis=0)) for cur_curve in dynamic_curves]
        # compute to a % of the area under the fixed curve and scale 
        overlap = [np.round(ov/sum(fixed_curve)*100,overlap_decimals) for ov in overlap_raw]

        # Create figure

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
                go.Scatter(
                    visible=True,
                    line=dict(color=static_color, width=6),
                    name= static_name,
                    x= shared_x,
                    y= fixed_curve),
            secondary_y=True)

        # norm.cdf(b, loc=mean, scale=sd)

        # Add traces, one for each slider step
        for curve,ov in zip(dynamic_curves,overlap):
            mean = np.round(np.argmax(curve),mean_decimals)
            fig.add_trace(
                go.Scatter(
                    visible=False,
                    line=dict(color=dynamic_color, width=6),
                    name= dynamic_name, 
                    meta ={'overlap':str(ov),'location':str(mean)},
                    x= shared_x,
                    y= curve),)

        # Make 10th trace visible
        fig.data[dynamic_starting_mean].visible = True

        # Create and add slider
        steps = []
        for i in range(1,len(fig.data)):
        #     overlap = 
            step = dict(
                method="update",
                label=np.round(shared_x[i-1],mean_decimals),
                args=[{"visible": [True] + [False] * len(fig.data)},
                    {"title": str(overlap[i-1]) + "% overlap"}],  # layout attribute
            )
            step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        sliders = [dict(
            active=dynamic_starting_mean,
            currentvalue={"prefix": dynamic_name + " mean: "},
            pad={"t": 50},
            steps=steps
        )]

        fig.update_layout(
            sliders=sliders,
            xaxis_title=xaxis_title
        )

        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)
        # if hide_y_ticks:
        #     fig.update_layout(
        #         xaxis = dict(
        #             tickmode='array',
        #             ticktext=['One, 'Three', 'Five', 'Seven', 'Nine', 'Eleven']'
        #     )
        #     )

        return fig
