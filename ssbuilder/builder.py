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
from copy import deepcopy
from importlib.resources import files

# import plot functions here 
from .single_normal_curve import NormalCurveSlider
from .tradeoff_questions import TradeoffBar, TradeoffLine
from .instructions import InstructionQuestion

# add function handle and a reference name here to add new types
figure_classes = {'NormalCurveSlider': NormalCurveSlider,
                  'TradeoffBar': TradeoffBar,
                  'TradeoffLine': TradeoffLine,
                  'InstructionQuestion': InstructionQuestion}


def load_template_file(*args):
    '''
    load a template file from the package's template dir
    '''
    template_path = os.path.join(files(__package__), 'assets', *args)
    
    with open(template_path, 'r') as tmpt_f:
        template = tmpt_f.read()
    
    return(template)

instruction_template_log = ''' ---------------------------
Created: [{out_url}/{out_html_file}]({out_url}/{out_html_file})  
Forwards to: {next_question_url}  
Sends: {send_vars}  
'''

instruction_template_minimal = '''
[{out_url}/{out_html_file}]({out_url}/{out_html_file}) 
'''

instruction_template_forward = '''
- [ ] [{out_url}/{out_html_file}]({out_url}/{out_html_file}) 
Forwards to: {next_question_url} 
Sends: {send_vars}
'''

instructions_template = {'log': instruction_template_log,
                         'forward': instruction_template_forward,
                         'minimal': instruction_template_minimal,
                         'blank': ''}


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
                       next_question_url=None,
                       debug=False,
                       full_html=True,
                       footer_type='confirm_submit',
                       instructions_type='log',
                       forward_type = None):
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
    question_text : string, markdown formatted
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
    next_question_url : string
        question id or url for the qualtrics question
    pretty_url : boolean {False}
        if True make pages like `/IndentiCurve/name/` instead of `/IdentiCurve/name.html` 
    full_html : boolean {True}
        generate a full html page or if False, generate only a segment of the page (eg for combining or embedding)
    footer_type : string {'confirm_submit','next' }
        type of footer to use 'confirm_submit'  or 'next'
    -------
    
    Notes
    -----
    variables with _var_name + "id" will be passed to qualtrics
    '''
    if debug:
        click.echo('building page')
    # validate the question id done into something that can work
    question_id = question_id.replace('/', '').replace(' ', '-').lower()

    #     ensure file name is valid
    out_html_file = get_file_name(out_html_file=out_html_file, question_id =question_id)

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
            if debug:
                print(figure_values['num_digits'])
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

    if debug:
        click.echo(out_html_file)
        click.echo(pass_through_vars)
    # pass through vars
    pass_through_template_html = load_template_file('question_form_elements','pass_through_var.html')

    pass_through_template_js = load_template_file('question_form_elements', 'pass_through_parse.js')

    # sort the pass throughs to make built html more stable
    #     first sort by var name
    #     next sort by the part after the _ (which is typically ID)
    pass_through_vars_split = [ptv for ptv in pass_through_vars if '_' in ptv]
    pass_through_vars_single = [ptv for ptv in pass_through_vars if not('_' in ptv)]
    pass_through_vars_sorted = sorted(pass_through_vars_single) + sorted(sorted(pass_through_vars_split),key=lambda ptv: ptv.split('_')[1])

    pass_through_html = [pass_through_template_html.format(pass_var_name=ptvar)
                         for ptvar in pass_through_vars_sorted if not(ptvar == 'id')]
    question_form_elements = question_form_html + \
        '\n\n'.join([''] + pass_through_html)

    if debug:
        click.echo('working on js pass through')
        click.echo(pass_through_template_js)
        click.echo(pass_through_vars_sorted)
    
    pass_through_js_list = [pass_through_template_js.format(pass_var_name=ptvar)  for ptvar in pass_through_vars_sorted]
    pass_through_js =  '\n'.join([''] + pass_through_js_list)
    
    if debug:
        click.echo(pass_through_js)
        click.echo('js for parse ')
        click.echo(type(pass_through_js))




    #  load and fill footer_html based on confirm/submit or next 
    footer_vars = {
        'confirm_message': confirm_message,
        'skip_message': skip_message,
        'confirm_var_name': confirm_var_name,
        'skip_id': question_id + 'skip',
        'confirm_id': question_id+'confirm',
        'button_text': button_text}
    footer_file_name = f'footer_{footer_type}.html'
    footer_template = load_template_file('footer_html',footer_file_name)  
    # TODO make option for next? 
    footer_html = footer_template.format(**footer_vars)

    if debug:
        click.echo('footder done')

    
    # load and fill in logging js
    if figure is None:
        #  for the no plot question
        plot_logging_js = ''
        plot_html = markdown.markdown(question_text)
        question_text = 'intructions'
    else:
        logging_js = load_template_file('plot_logging_js',figure_meta.plot_logging_js )
        plot_logging_js = logging_js.format(**logging_vars)

        plot_html = figure.to_html(
            include_plotlyjs='cdn', full_html=False, div_id=question_id, auto_play=False)
    
    # combine all template variables for overall page
    page_info = {'page_title': page_title,
                 'next_question_url': next_question_url,
                 'question_form_elements': question_form_elements,
                 'pass_through_js': pass_through_js,
                 'question_text': markdown.markdown(question_text),
                 'plot_html': plot_html,
                 'footer_html':footer_html,
                 'plot_logging_js': plot_logging_js}
    if debug: 
        click.echo(page_info)
        
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
    send_vars = pass_through_vars_sorted + sorted(list(logging_vars.values()))
    settings_vars = {'send_vars':send_vars,
                     'out_html_file': out_html_file,
                     'next_question_url': next_question_url,
                     'out_url':out_url}
    
    if not(instructions_type) == 'log':
        # check if internal or external forward and update type
        instruction_by_fwd = {'internal':'minimal',
                              'external':instructions_type}
        instructions_type = instruction_by_fwd[forward_type]

    instructions = instructions_template[instructions_type].format(**settings_vars)
    return instructions

def set_pass_through(config_dict_list,
                     study_default_pt_vars=['id'], debug=False):
    '''
    set the pass_through_vars values 

    Parameters
    ----------
    config_dict_list : dictionary
        dictionary with parameters of the page builder as keys
    study_default_pt_vars : list
        list of variables that all questions pass through
    '''
    if debug:
        click.echo('pass through')
    
    # note in this function we rely on that dictionaries are not copied
    # set question_id as keys for better indexing
    conf_qid = {d['question_id']: d for d in config_dict_list}
    
    question_ids = [d['question_id'] for d in config_dict_list]

    q_traverse_order = []
    # iterate over list in order, produce traversal order
    for q_id in question_ids:
        # set default ptvars
        
        conf_qid[q_id]['pass_through_vars'] = study_default_pt_vars.copy()
        # if specifid, use that
        if 'next_question_url' in conf_qid[q_id]:
            
            # get next q target
            next_question = conf_qid[q_id]['next_question_url']

            # if this has not been seen yet
            if not (q_id in q_traverse_order):
                if next_question in q_traverse_order:
                    # if next q is in then 
                    nq_idx = q_traverse_order.index(next_question)
                    q_traverse_order.insert(nq_idx, q_id)
                else:
                    # put this question in the list
                    q_traverse_order.append(q_id)

            # check if its an id
            while next_question in question_ids and not(next_question in q_traverse_order):
                # append this
                q_traverse_order.append(next_question)
                #  traverse to the next
                next_question = conf_qid[next_question]['next_question_url']
        else:
            conf_qid[q_id]['next_question_url'] = 'end.html'

    # iterate over list, checking all, to handle skips or cases with none
    for q_id in q_traverse_order:
        # get next q target
        next_question = conf_qid[q_id]['next_question_url']

        if debug:
            if 'pass_through_vars' in conf_qid[q_id]:
                click.echo('preset ptv on')
                click.echo(q_id)
                click.echo(conf_qid[q_id]['pass_through_vars'])

        # check if its an id, an internal forward
        if next_question in question_ids:
            if debug:
                click.echo(q_id)
                click.echo('forwards to ')
                click.echo(next_question)
            # extract pass through vars and confirm if needed
            if conf_qid[q_id]['logging_vars']:
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
                    if debug:
                        click.echo(q_id)
                        click.echo('adding cur vars to pass on next q')
                    
                    cur_q_vars += conf_qid[q_id]['pass_through_vars']
                # add append or create passthrough vars key
                if 'pass_through_vars' in conf_qid[next_question]:
                    if debug:
                        click.echo('append ptv ')
                        click.echo(study_default_pt_vars)
                        click.echo(cur_q_vars)
                        click.echo(next_question)
                    # appnd
                    next_pass_through = conf_qid[next_question]['pass_through_vars'] + cur_q_vars
                else: 
                    if debug:
                        click.echo('set ptv ')
                        click.echo(study_default_pt_vars)
                        click.echo(cur_q_vars)
                        click.echo(next_question)
                    # setup
                    next_pass_through = study_default_pt_vars + cur_q_vars

                # remove duplicates
                conf_qid[next_question]['pass_through_vars'] = list(set(next_pass_through))
            
            # set true url to next question url (either specfied or question id)
            if 'out_html_file' in conf_qid[next_question].keys():
                conf_qid[q_id]['next_question_url'] = conf_qid[next_question]['out_html_file']
            else:
                conf_qid[q_id]['next_question_url'] = conf_qid[next_question]['question_id'].lower() + '.html'
            
            # set forward type
            conf_qid[q_id]['forward_type'] = 'internal'
        else:
            conf_qid[q_id]['forward_type'] = 'external'

        #     # if not forwarding, just set own pass through with study level
        #     conf_qid[q_id]['pass_through_vars'] = study_default_pt_vars 

    # return as list of dicts
    return list(conf_qid.values())


def get_file_name(question_dict = None, out_html_file=None, question_id = None):
    '''
    get the file name for a question from feild with processing or question id

    Parameters
    ----------
    question_dict : dictionary 
        all question informtation including both `out_file_html` and `question_id`
    out_html_file : string
        just the one parameter from settings, this will be used if provided, can be input
    in any case and with or without extension
    question_id : string
        the question id this will be used if `out_html_file` not provided

    Returns
    -------
    out_file_html : string
        all lowercase file name with the .html extension added / will be removed and spaces 
    replaced with -
    '''
    # if dictionary proved, pull out required parameters
    if question_dict:
        #  this is a required parameter, okay to error if missing
        question_id = question_dict['question_id']
        #  check if this is in and overwrite if provided, otherwise keep default None 
        if 'out_file_html' in question_dict.keys():
            out_html_file = question_dict['out_file_html']
    
    #  set base out_html_file
    if not (out_html_file):
        out_html_file = question_id.lower() + '.html'
    elif not (out_html_file[-5:] == '.html'):
        out_html_file += '.html'

    # clean up formatting
    # TODO: this is pretty minimal fixing based on seen-to-date problematic choices used; could be more robus
    out_html_file = out_html_file.replace('/', '').replace(' ', '-').lower()

    return out_html_file

def expand_shared_params(loaded_config,debug=False):
    question_template = loaded_config['shared']
    question_unique = loaded_config['unique']
    if debug:
        print('shared first:\n',question_template)

    # find nested parameters
    nested_parameters = [k for k,v in question_template.items() if type(v)==dict]
    

    # make copies of template for each real question
    full_config = [deepcopy(question_template) for q in question_unique]

    # update each question
    # full_config = []
    for q_i,c_i in zip(question_unique,full_config):
        # c_i = question_template.copy()
        
        for nested_param in nested_parameters:
            # update the nested and then remove the key
            if nested_param in q_i:
                c_i[nested_param] |= q_i[nested_param]
                q_i.pop(nested_param)
            
                

        # update remaining (not dict values)
        c_i |= q_i

    
    return full_config


@click.command()
@click.option('-f','--config-file')
@click.option('-p', '--out_rel_path')
@click.option('-r','--repo_name')
@click.option('-o','--gh_org')
@click.option('-d','--debug',is_flag=True)
@click.option('--fragment',is_flag=True)
@click.option('-a','--all_in_one',is_flag=True)
@click.option('-v','--study-pass-through-vars', multiple=True, default=['id'])
@click.option('-i','--instructions-type', default='forward',
              type=click.Choice(['log','forward','minimal','blank'],
                                case_sensitive=False))
              
def generate_from_configuration(config_file=None,repo_name=None,
                                gh_org=None,out_url=None,
                                debug=False, out_rel_path='',
                                fragment=False,all_in_one=False,
                                study_pass_through_vars = ['id'], 
                                instructions_type='log'):
    '''
    Generate html files from a configuration file

    Parameters
    ----------
    config_file : string or None
        file name, if none, configureation.yml assumed
    repo_name : string {None}
        name of the repo
    out_url : string {None}
        specify if not github with org/repo
    gh_org : string {None}
        name of the gh org or user that owns the repo to build the URL
    debug : bool
        print debuggin information or not
    out_rel_path : string
        relative path where to save the html files 
    fragment : bool
        generate a fragment or not
    all_in_one : bool
        merge files to a single htmlfile, this version will not work as as a survey
    '''
    if not(type(study_pass_through_vars) ==list):
        study_pass_through_vars = list(study_pass_through_vars)
    

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

    # ------------------------------------------------------------------------  
    #   process shared params if provided
    if type(loaded_config) == list:
         
        # pass as is
        full_config = loaded_config
    elif 'shared' in loaded_config.keys():
        full_config = expand_shared_params(loaded_config,debug)
    

    # ------------------------------------------------------------------------
    # parse for pass through vars for sequential questions
    
    parsed_config = set_pass_through(full_config,study_pass_through_vars, debug)

    # remove metadata, inplace
    #  could be saved, but if nested it's a dict and nontrival to print for now. 
    [q.pop('metadata',None) for q in parsed_config]

    # -------------- generate all of the files and save the instructions
    if not(os.path.isdir(out_rel_path)):
        os.makedirs(out_rel_path)
    
    instructions = [make_question_page(**q, out_url=out_url, out_rel_path=out_rel_path,
          debug=debug,full_html=not(fragment),instructions_type=instructions_type) 
        for q in parsed_config]
    #  save instructions
    with open(instruction_file, 'w') as f:
        f.write('\n'.join(instructions))
        f.write('\n\n ## Metadata')
        # f.write('\n'.join(metadata))

    # check if end.html is required 
    #  end.html is an option for the `next_question_url` parameter to send people to a landing
    # page instead of qualtrics
    next_url_list = [d['next_question_url'] for d in full_config]
    if 'end.html' in next_url_list:
        end_html = load_template_file('end.html')
        with open(os.path.join(out_rel_path,'end.html'),'w') as f:
            f.write(end_html)
         

    # merge if appropriate
    if all_in_one:
        # extract file names
        file_list = [get_file_name(question_dict=q) for q in parsed_config]
        page = load_template_file('page_header.html').format(study_name = repo_name)
        for file_name in file_list:
            with open(os.path.join(out_rel_path,file_name),'r') as f:
                page +=f.read()
        page += load_template_file('page_footer.html')

        with open(os.path.join(out_rel_path, 'aio.html'),'w') as f:
            f.write(page)

@click.command()
@click.option('-f','--config-file')
@click.option('-m','--metadata',multiple=True,default = None)
              
def question_csv(config_file=None,metadata=None,debug=False):
    '''
    '''
    # --------------  load and parse the configurations
    with open(config_file, 'r') as f:
        loaded_config = yaml.load(f, Loader=yaml.Loader)

    full_config = expand_shared_params(loaded_config,debug)

    base_attrs = ['question_id','question_text']
    if metadata:
        out_cols = base_attrs + list(metadata)
        data = [[q[a] for a in base_attrs] + [q['metadata'][ma] for ma in metadata] for q in full_config]
    else:
        out_cols = base_attrs
        data = [[q[a] for a in base_attrs] for q in full_config]

    df = pd.DataFrame(data =data, columns = out_cols)
    click.echo('Created DataFrame with shape ' + str(df.shape))

    csv_file_name = config_file.split('.')[0] + '.csv'
    df.to_csv(csv_file_name)
    click.echo('wrote out ' + csv_file_name )