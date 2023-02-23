import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import norm
import click
import yaml

import pkg_resources as pkgrs

# import plot functions here 
from single_normal_curve import NormalCurveSlider

# add function handle and a reference name here to add new types
figure_classes = {'NormalCurveSlider': NormalCurveSlider}

def load_template_file(*args):
    template_rel = os.path.join('assets', *args)
    template_path = pkgrs.resource_filename(__name__, template_rel)
    with open(template_path, 'r') as tmpt_f:
        template = tmpt_f.read()
    
    return(template)


settings_message_template = ''' ---------------------------
Created: [{out_html_file}](docs/{out_html_file})
Forwards to: {next_question_url}.
Sends: {send_vars}
'''

def make_question_page(question_id, figure_type='normal_curve_slider', figure_values=None,
                       page_title='Normal Curve Question',
                       question_text='Move the slider',
                       confirm_message='Confirm my answer',
                       skip_message='Prefer not to answer',
                       button_text='Submit',
                       out_html_file=None,
                       logging_vars=None,
                       confirm_var_name=None,
                       var_name_suffix=True,
                       pretty_url=False,
                       pass_through_vars = ['id'],
                       next_question_url='https://uri.co1.qualtrics.com/jfe/form/SV_3rU4XfDtiVN8HMW'):
    '''
    generate html file
    
    Parameters
    ----------
    question_id : string {required}
        name for the question internally
    figure : string
         string name of valid plot type in ssbuilder
    figure_values : dictionary
        parameters to pass to plotting function
    page_title : string
        what to show in the tab title default = 'Normal Curve Question',
    question_text : string
        the text of the questions
    confirm_message : text
        prompt for confirmation
    skip_message : text 
        prompt for skipping
    button_text : string
        text on button
    out_html_file : string
        name fo the html file, that will be in the url for the participant 
        if not passed will add ".html" to the questionid
    logging_vars : dictionary
        dictionary of names for the variable types the specific question requires 
    confirm_var_name : string {'confirm'}
        name for the variable, if not passed will be question_id + 'confirm'  +question_id
    var_name_suffix : boolean {True}
        if true, add question_id to the passed values for all _var_names. Default is True,
        can be changed to False if you specify the variable names directly
    pass_through_vars : list of strings ['id']
        list of variables to pass through from previous to next
    next_question : string
        question id or url for the qualtrics question
    pretty_url : boolean {False}
        if True make pages like `/IndentiCurve/name/` instead of `/IdentiCurve/name.html` 
        
    Notes
    -----
    variables with _var_name + "id" will be passed to qualtrics
    '''
    # validate the question id done into something that can work
    question_id = question_id.replace('/', '').replace(' ', '-').lower()

    #     ensure file name is valid
    if not (out_html_file):
        out_html_file = question_id + '.html'
    elif not (out_html_file[-5:] == '.html'):
        out_html_file += '.html'

    out_html_file = out_html_file.replace('/', '').replace(' ', '-').lower()

    # fix defaults

    if not (confirm_var_name):
        confirm_var_name = 'confirm'

    if var_name_suffix:
        confirm_var_name += '_' + question_id
        logging_vars = {k: v + '_' + question_id for k,
                        v in logging_vars.items()}

    # process figure related
    if type (figure) == str:
        # set logging vars into or get from figure obj
        if not (logging_vars):
            figure_meta = figure_classes[figure_type]()
            logging_vars = figure.logging_vars
        else:
            figure_meta = figure_classes[figure_type](logging_vars)

        # generate figure
        if not (figure_values):
            figure = figure_meta.generate_figure()
        else:
            figure = figure_meta.generate_figure(**figure_values)
        
        

    # current question form elements
    question_form_template = load_template_file('question_form_elements',
                                    figure_meta.question_form_elements)
    question_form_html = question_form_template.format(**logging_vars)

    # pass through vars
    pass_through_template = load_template_file('question_form_elements','pass_through_var.html')
    pass_through_html = [pass_through_template.format(pass_var_name= ptvar)
                                     for ptvar in pass_through_vars]
    question_form_elements = question_form_html + '\n\n'.join(['',pass_through_html])

    #  load and fill footer_html based on confirm/submit or next 
    footer_vars = {
        'confirm_message': confirm_message,
        'skip_message': skip_message,
        'confirm_var_name': confirm_var_name,
        'skip_id': question_id + 'skip',
        'confirm_id': question_id+'confirm',
        'button_text': button_text}
    footer_template = load_template_file() # TODO where is this set
    footer_html = footer_template.format(**footer_vars)

    # logging js
    logging_js = load_template_file('plot_logging_js',figure_meta.plot_logging_js)
    plot_logging_js = logging_js.format(**logging_vars)


    #  fill in contents to page.thml
    # get figure html
    plot_html = figure.to_html(
        include_plotlyjs='cdn', full_html=False, div_id=question_id)

    # combine all template variables
    page_info = {'page_title': page_title,
                 'next_question_url': next_question_url,
                 'question_form_elements': question_form_elements,
                 'question_text': question_text,
                 'plot_html': plot_html,
                 'footer_html':footer_html,
                 'plot_logging_js': plot_logging_js}
    page_template = load_template_file('page.html')
    page_html = page_template.format(**page_info)

    # format the final path
    if pretty_url:
        subdir = out_html_file[:-5]
        out_html_file = os.path.join('docs', subdir, 'index.html')
    else:
        out_html_file = os.path.join('docs', out_html_file)

    # Write the pate
    with open(out_html_file, 'w') as f:
        f.write(page_html)

    # this is for the user
    #    notebook exmaples print it as markdown
    #    config generator captures into a file
    settings_vars = {'send_vars':pass_through_vars +logging_vars,
                     'out_html_file': out_html_file}
    return settings_message_template.format(**page_isettings_varsnfo)

def set_pass_through(config_dict_list):
    '''
    set the pass_through_vars values 
    '''
    # se question_id as index 
    conf_qid = {d['question_id']: d for d in config_dict_list}
    
    question_ids = [d['question_id'] for d in config_dict_list]

    # iterate over list, checking all, to handle skips or cases with none
    for conf_dt in  config_dict_list:
        # get next q target
        next_question = conf_dt['next_question_url']

        # check if its and id
        if next_question in question_ids:
            # pass through vars and confirm
            cur_question_vars = list(conf_dt['figure_vars'].values())
            cur_confirm = conf_dt['confirm_var_name']
            cur_q_vars = [cur_confirm] + cur_question_vars
            if 'pass_through_vars' in conf_qid[next_question]:
                conf_qid[next_question]['pass_through_vars'] += cur_q_vars
            else: 
                conf_qid[next_question]['pass_through_vars'] = ['id'] + cur_q_vars

    # return as list of dicts
    return list(conf_qid.values)


@click.command()
@click.option('--config-file')
def generate_from_configuration(config_file=None):
    '''
    Generate html files from a configuration file

    Parameters
    ----------
    config_file : string or None
        file name, if none, configureation.yml assumed
    
    
    '''
    # set file names
    if not (config_file):
        config_file = 'configuration.yml'
        instruction_file = 'instructions.md'
    else:
        instruction_file = config_file[:-4] + '-instructions.md'

    # load and parse the configurations
    with open(config_file, 'r') as f:
        loaded_config = yaml.load(f, Loader=yaml.Loader)
    
    # parse for pass through vars for sequential questions
    parsed_config = set_pass_through(loaded_config)
    # generate all of the files and save the instructions
    instructions = [make_question_page(**q) for q in parsed_config]
    #  save instructions
    with open(instruction_file, 'w') as f:
        f.write('\n'.join(instructions))
