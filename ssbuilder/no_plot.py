# note: placed this in a new file for isolation sake

class NoPlot:
    # a plot class that returns nothing
    def __init__(self, logging_vars=None):
        self.plot_logging_js = 'plot_log_no_plot.js'
        self.question_form_elements = 'form_np.html'
        self.logging_vars = {} if logging_vars is None else logging_vars

    def generate_figure(self, **kwargs):
        return None