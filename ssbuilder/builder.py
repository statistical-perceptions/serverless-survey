import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import norm
import click
import yaml
import markdown

import pkg_resources as pkgrs

# import plot functions here 
from .single_normal_curve import NormalCurveSlider
from .tradeoff_questions import TradeoffBar, TradeoffLine

# add function handle and a reference name here to add new types
figure_classes = {'NormalCurveSlider': NormalCurveSlider,
                  'TradeoffBar': TradeoffBar,
                  'TradeoffLine': TradeoffLine}

def load_template_file(*args):
    template_rel = os.path.join('assets', *args)
    template_path = pkgrs.resource_filename(__name__, template_rel)
    with open(template_path, 'r') as tmpt_f:
        template = tmpt_f.read()
    
    return(template)


settings_message_template = ''' ---------------------------
Created: [{out_url}/{out_html_file}]({out_url}/{out_html_file})  
Forwards to: {next_question_url}  
Sends: {send_vars}  
'''


def make_question_page(question_id, figure_type='NormalCurveSlider', figure_values=None,
                       page_title='Normal Curve Question',
                       question_text='Move the slider',
                       confirm_message='Confirm my answer',
                       skip_message='Prefer not to answer',
                       button_text='Submit',
                       out_html_file=None,
                       out_rel_path = None,
                       logging_vars=None,
                       confirm_var_name=None,
                       var_name_suffix=True,
                       pretty_url=False,
                       pass_through_vars = ['id'],
                       out_url = None,
                       next_question_url='https://uri.co1.qualtrics.com/jfe/form/SV_3rU4XfDtiVN8HMW',
                       debug=False,
                       full_html=True):
    '''
    generate html file
    
    Parameters
    ----------
    question_id : string {required}
        name for the question internally
    figure_type : string
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
    out_rel_path : string or file buffer
        where to write the files. 
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
    full_html : boolean {True}
        generate a full html page or if False, generate only a segment of the page (eg for combining or embedding)
    
    Returns
    -------
    
    Notes
    -----
    variables with _var_name + "id" will be passed to qualtrics
    '''
    # validate the question id done into something that can work
    question_id = question_id.replace('/', '').replace(' ', '-').lower()

    #     ensure file name is valid
    if not (out_html_file):
        out_html_file = question_id.lower() + '.html'
    elif not (out_html_file[-5:] == '.html'):
        out_html_file += '.html'

    out_html_file = out_html_file.replace('/', '').replace(' ', '-').lower()

    # fix defaults

    if not (confirm_var_name):
        confirm_var_name = 'confirm'


    # process figure related
    if type(figure_type) == str:
        # set logging vars into or get from figure obj
        if not (logging_vars):
            figure_meta = figure_classes[figure_type]()
            logging_vars = figure_meta.logging_vars
        else:
            figure_meta = figure_classes[figure_type](logging_vars)

        # generate figure
        if not (figure_values):
            figure = figure_meta.generate_figure()
        else:
            figure = figure_meta.generate_figure(**figure_values)

    if var_name_suffix:
        confirm_var_name += '_' + question_id
        logging_vars = {k: v + '_' + question_id for k,
                        v in logging_vars.items()}
    logging_vars['question_id'] = question_id
        

    # current question form elements
    question_form_template = load_template_file('question_form_elements',
                                    figure_meta.question_form_elements)
    question_form_html = question_form_template.format(**logging_vars)

    # pass through vars
    pass_through_template = load_template_file('question_form_elements','pass_through_var.html')
    
    pass_through_html = [pass_through_template.format(pass_var_name= ptvar)
                                     for ptvar in pass_through_vars if not(ptvar=='id')]
    question_form_elements = question_form_html + '\n\n'.join([''] + pass_through_html)

    #  load and fill footer_html based on confirm/submit or next 
    footer_vars = {
        'confirm_message': confirm_message,
        'skip_message': skip_message,
        'confirm_var_name': confirm_var_name,
        'skip_id': question_id + 'skip',
        'confirm_id': question_id+'confirm',
        'button_text': button_text}
    footer_template = load_template_file('footer_html','footer_confirm_submit.html')  
    # TODO make option for next? 
    footer_html = footer_template.format(**footer_vars)

    # logging js
    logging_js = load_template_file('plot_logging_js',figure_meta.plot_logging_js )
    plot_logging_js = logging_js.format(**logging_vars)


    #  fill in contents to page.thml
    # get figure html
    plot_html = figure.to_html(
        include_plotlyjs='cdn', full_html=False, div_id=question_id, auto_play=False)

    # combine all template variables
    page_info = {'page_title': page_title,
                 'next_question_url': next_question_url,
                 'question_form_elements': question_form_elements,
                 'question_text': markdown.markdown(question_text),
                 'plot_html': plot_html,
                 'footer_html':footer_html,
                 'plot_logging_js': plot_logging_js}
    
    if full_html:
        page_template = load_template_file('page.html')
    else:
        page_template = load_template_file('fragment.html')
        page_info['page_title'] = out_html_file[:-5]

    page_html = page_template.format(**page_info)

    # format the final path
    if pretty_url:
        subdir = out_html_file[:-5]
        out_html_file = os.path.join(subdir, 'index.html')
    else:
        out_html_file = os.path.join(out_html_file)

    # prepend out directory if provded
    if out_rel_path:
        out_path = os.path.join(out_rel_path, out_html_file)
    else:
        out_path = out_html_file

    # Write the page
    with open(out_path, 'w') as f:
        f.write(page_html)

    # this is for the user
    #    notebook exmaples print it as markdown
    #    config generator captures into a file
    settings_vars = {'send_vars':pass_through_vars +list(logging_vars.values()),
                     'out_html_file': out_html_file,
                     'next_question_url': next_question_url,
                     'out_url':out_url}
    return settings_message_template.format(**settings_vars)

def set_pass_through(config_dict_list):
    '''
    set the pass_through_vars values 

    Parameters
    ----------
    config_dict_list : dictionary
        dictionary with parameters of the page builder as keys
    '''
    # set question_id as keys for better indexing
    conf_qid = {d['question_id']: d for d in config_dict_list}
    
    question_ids = [d['question_id'] for d in config_dict_list]

    q_traverse_order = []
    # iterate over list in order, produce traversal order
    for q_id in question_ids:

        # get next q target
        next_question = conf_qid[q_id]['next_question_url']

        # if this has not bee seen yet
        if not (q_id in q_traverse_order):
            if next_question in q_traverse_order:
                # if next q is in then 
                nq_idx = q_traverse_order.index(next_question)
                q_traverse_order.insert(nq_idx, q_id)
            else:
                # put this question in the list
                q_traverse_order.append(q_id)
                


        # check if its and id
        while next_question in question_ids and not(next_question in q_traverse_order):
            # append this
            q_traverse_order.append(next_question)
            #  traverse to the next
            next_question = conf_qid[next_question]['next_question_url']

    # iterate over list, checking all, to handle skips or cases with none
    for q_id in q_traverse_order:
        # get next q target
        next_question = conf_qid[q_id]['next_question_url']

        # check if its an id
        if next_question in question_ids:
            # extract pass through vars and confirm
            cur_question_vars = list(conf_qid[q_id]['logging_vars'].values())
            cur_confirm = conf_qid[q_id]['confirm_var_name']
            # var_name_suffix is defaulted to True in the make page, so same behavior here
            #  if not passed at all or manually set to true
            if not ('var_name_suffix' in conf_qid[q_id].keys()) or conf_qid[q_id]['var_name_suffix']:
                cur_confirm += '_' + conf_qid[q_id]['question_id'].lower()
                cur_question_vars = [qv + '_' + conf_qid[q_id]['question_id'].lower()
                                     for qv in cur_question_vars]
            cur_q_vars = [cur_confirm] + cur_question_vars
            # append current pass throughs if they exist
            if 'pass_through_vars' in conf_qid[q_id]:
                cur_q_vars += conf_qid[q_id]['pass_through_vars'][1:]
            # add append or create passthrough vars key
            if 'pass_through_vars' in conf_qid[next_question]:
                conf_qid[next_question]['pass_through_vars'] += cur_q_vars
            else: 
                conf_qid[next_question]['pass_through_vars'] = ['id'] + cur_q_vars
            # set true url 
            if 'out_html_file' in conf_qid[next_question].keys():
                conf_qid[q_id]['next_question_url'] = conf_qid[next_question]['out_html_file']
            else:
                conf_qid[q_id]['next_question_url'] = conf_qid[next_question]['question_id'].lower() + '.html'

    # return as list of dicts
    return list(conf_qid.values())

def link_question(q_config_dict):
    '''
    take a single config dictionary and update
    '''
    # TODO: not recursive, but needs to traverse, then order, then update in order, propagting through to the end

def get_file_name(question_dict):
    '''
    get the file name for a question from its dictionary
    '''
    if not('out_html_file' in question_dict.keys()):
        out_html_file = question_dict['question_id'].lower() + '.html'
    elif not (question_dict['out_html_file'][-5:] == '.html'):
        out_html_file = question_dict['out_html_file']+ '.html'
    
    return out_html_file

@click.command()
@click.option('-f','--config-file')
@click.option('-p', '--out_rel_path')
@click.option('-r','--repo_name')
@click.option('-o','--gh_org')
@click.option('-d','--debug',is_flag=True)
@click.option('--fragment',is_flag=True)
@click.option('-a','--all_in_one',is_flag=True)
              
def generate_from_configuration(config_file=None,repo_name=None,
                                gh_org=None,out_url=None,
                                debug=False, out_rel_path='',
                                fragment=False,all_in_one=False):
    '''
    Generate html files from a configuration file

    Parameters
    ----------
    config_file : string or None
        file name, if none, configureation.yml assumed
    repo_name : string {None}
        name of the repo
    gh_org : string {None}
        name of the gh org or user that owns the repo to build the URL
    debug : bool
        print debuggin information or not
    fragment : bool
        generate a fragment or not
    all_in_one : bool
        merge files to a single htmlfile
    '''
    # create url from repo and org if not passed
    if not(out_url):
        out_url = ''
        if gh_org:
            out_url = 'https://' +gh_org + '.github.io/'

        if repo_name:
            out_url += repo_name 
    
    if all_in_one:
        fragment=True

    # set file names
    if not (config_file):
        config_file = 'configuration.yml'
        instruction_file = 'instructions.md'
    else:
        instruction_file = config_file[:-4] + '-instructions.md'

    # --------------  load and parse the configurations
    with open(config_file, 'r') as f:
        loaded_config = yaml.load(f, Loader=yaml.Loader)

    if 'shared' in loaded_config.keys():
        question_template = loaded_config['shared']
        question_unique = loaded_config['unique']

        # find nested parameters
        nested_parameters = [k for k,v in question_template.items() if type(v)==dict]

        # make copies of template for each real question
        full_config = [question_template.copy() for q in question_unique]

        # update each nested var
        for fc_i,q_i in zip(full_config,question_unique):
            # update the nested values first
            for nest_param in nested_parameters:
                if nest_param in q_i:
                    fc_i[nest_param].update(q_i[nest_param])
                    # remove from q after new values are inserted
                    del q_i[nest_param]
            
            # update  remaining parameters
            fc_i.update(q_i)
    else: 
        full_config = loaded_config
    
    # parse for pass through vars for sequential questions
    parsed_config = set_pass_through(full_config)



    # -------------- generate all of the files and save the instructions
    instructions = [make_question_page(
        **q, out_url=out_url, out_rel_path=out_rel_path, debug=debug,full_html=not(fragment)) for q in parsed_config]
    #  save instructions
    with open(instruction_file, 'w') as f:
        f.write('\n'.join(instructions))

    # merge if appropriate
    if all_in_one:
        # extract file names
        file_list = [get_file_name(q) for q in parsed_config]
        page = load_template_file('page_header.html').format(study_name = repo_name)
        for file_name in file_list:
            with open(os.path.join(out_rel_path,file_name),'r') as f:
                page +=f.read()
        page += load_template_file('page_footer.html')

        with open(os.path.join(out_rel_path, repo_name+'-aio.html'),'w') as f:
            f.write(page)
