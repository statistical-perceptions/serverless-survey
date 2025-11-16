# note: placed this in a new file for isolation sake

class InstructionQuestion:
    # a plot class that returns nothing
    def __init__(self, logging_vars=None):
        self.plot_logging_js = 'plot_log_instructions.js'
        self.question_form_elements = 'form_instructions.html'
        self.logging_vars = {} if logging_vars is None else logging_vars

    def generate_figure(self, **kwargs):
        return None
    

