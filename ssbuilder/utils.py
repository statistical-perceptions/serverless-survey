import click

def md_params(function):
    '''
    return a markdown list of the parameters from an object with numpydoc style docstring
    
    Parameters
    ----------
    function : object
        function (or other) object iwth a numpydoc docstring. Must have parameters and returns listed
    
    Returns
    -------
    mdparams : string
        a bulleted list with var names in code
    '''
    ds_lines = [l.strip() for l in function.__doc__.split('\n')]
    param_start = ds_lines.index('Parameters') +2
    param_end = ds_lines.index('Returns')

    param_lines = ds_lines[param_start:param_end]



    varify = lambda s: '`' + s + '`'
    process_line = {True: lambda l: '- ' + ' '.join([varify(l.split(' ')[0])]+ l.split( )[1:]),
                   False: lambda l: '  ' + l}
    [process_line[' : ' in l ](l) for l in param_lines]
    return '\n'.join([process_line[' : ' in l ](l) for l in param_lines])


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-o','--vars-only', is_flag=True,default=False)
@click.option('-i','--id-length',type=int,default=10)
@click.option('-v','--value-length',type=int,default=3)
@click.option('-b','--exclude-base', is_flag=True,)
def check_query_length(filename,vars_only=False, 
                        id_length=10,
                        value_length=3,
                        exclude_base=False):
    """
    Check the length in characters of the string to be passed, 
    not including values and print warnings to terminal 

    Parameters
    ----------
    filename : str
        The path to the instruction file to check
    vars_only : bool {False}
        if True return length of the variables and joiners only, no prefix or assumed value lengths
    id_len : int {10}
        length of unique identifier in characters
    value_length  : int {3}
        average length in characters of values passed, other than id
    include_base : bool {True}
        include the base of the forward address or not (False if vars_only=True)


    """
    est_chars = calculate_query_length(filename,vars_only, 
                        id_length, value_length,exclude_base)

    if est_chars > 2000:
        click.echo('You have ' + str(est_chars) + ' estimated characters and the recommended limit is 2000')
    else: 
        click.echo('your estimated message length is probably safe at ' + str(est_chars))

    




def calculate_query_length(filename,vars_only=False, 
                        id_length=10,
                        value_length=3,
                        exclude_base=False):
    """
    Check the length in characters of the string to be passed, not including values

    Parameters
    ----------
    filename : str
        The path to the instruction file to check
    vars_only : bool {False}
        if True return length of the variables and joiners only, no prefix or assumed value lengths
    id_len : int {10}
        length of unique identifier in characters
    value_length  : int {3}
        average length in characters of values passed, other than id
    include_base : bool {True}
        include the base of the forward address or not (False if vars_only=True)


    Returns
    -------
    est_chars : int
        estiminated character length (loose lower bound of true)


    """
    est_chars =0
    with open(filename, 'r') as f:
        file_lines = f.readlines()

    send_strings = [s for s in file_lines if 'Sends: [' in s]

    # create template message
    if vars_only:
        message_template = '&='
        id_length=0
        include_base = False
    else:
        message_template = '&=' + 'x'*value_length

    # use template to find longest length
    format_message = lambda s: s[8:-2].replace("'",'').replace(', ',message_template)
    message_lengths = [len(format_message(s)) for s in send_strings]
    longest_msg_length = max(message_lengths)
    est_chars += longest_msg_length
    
    if not(exclude_base):
        # find in file to get forward url
        longest_send_idx = message_lengths.index(longest_msg_length)
        longest_raw_text = send_strings[longest_send_idx]
        longest_file_idx = file_lines.index(longest_raw_text)
        fwd_url = file_lines[longest_file_idx -1].replace('Forwards to: ','')
        if not('http' in fwd_url):
            cur_created = file_lines[longest_file_idx -2]
            cur_url_start = cur_created.index('[')+1
            cur_url_end = cur_created.index(']')
            # extract url from "created:" line
            cur_url = cur_created[cur_url_start:cur_url_end]
            # keep only the base and to reconstruct the fwd url
            fwd_url = '/'.join(cur_url.split('/')[:-1]) + '/' + fwd_url
        
        # add length of full url
        est_chars += len(fwd_url)
        

    if id_length:
        # using len for transparency
        prefix_length = len('?id=') + id_length
        est_chars += prefix_length

    return est_chars