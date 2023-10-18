import click
import os
import pandas as pd

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


@click.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option('-m', '--merge-on', default=['id'], multiple=True, 
              help='columns to merge on, if multiple pass each one with the option')
@click.option('-h', '--header', default=0,
              help='row number to use as the header, starting from 0')
@click.option('-s', '--skip-row', multiple=True, type=int, default=[1,2],
              help='row numbers to skip, counting from 0, passed 1 value to each flag. default [1,2]')
@click.option('-o','--out-name',default=None,
              help='file name to save new csv to, if not passed, folder name is used')
@click.option('-v','--verbose',is_flag=True,
              help = 'show details of process for debugging purposes')
@click.option('-c','--complete-only',is_flag=True,
              help='flag to keep only rows that exist in all files (if passed, uses inner merge, otherwise outer)')
def cmd_merge_dir_csvs(folder, merge_on, out_name, header,
                        verbose, skip_row, complete_only):
    '''
    merge all csvs in a folder into a single CSV file, with new columns ordered by 
    what source file they came from alphabetically
    '''
    merge_dir_csvs(folder, merge_on, out_name, header,
                   verbose, skip_row, complete_only)

def merge_dir_csvs(folder,merge_on='id',out_name=None, header=0, 
                   verbose=False, skip_row =None,complete_only=False):
    '''
    merge all csvs in a folder into a single CSV file, with new columns ordered by 
    what source file they came from alphabetically

    Parameters
    ----------
    folder : string
        folder name
    merge_on : string or list of strings
        column shared across all files, default id
    out_name : string
        name to use the file, if not provided uses folder.csv
    header : int
        row to treat as the header (or anything that can be passed to pd.read_csv header)
    skip_row : int
        rows to skip, as a list (passed one at a time using multiple uses of the flag)
    verbose : bool
        print extra information out for debugging
    complete_only : bool
        if True use an inner merge, if not use outer merge
    '''
    

    # parse compelte only into merge type
    if complete_only:
        merge_type = 'inner'
    else:
        merge_type = 'outer'
    
    # get all fo the files, sort alphabetically
    file_list= sorted([file for file in os.listdir(folder) if file[-4:]=='.csv'])
    if verbose:
        click.echo('found files: ' + str(len(file_list)) )
        click.echo('\n'.join(file_list))

    # load all of the datafiles, applying the same skip and header to each file
    # drop any rows that have no value for the merge column
    #  drop any duplicate values for the merge columns
    data_frame_list = [pd.read_csv(os.path.join(folder, file),
                                       header=header, 
                                       skiprows=lambda x: x in skip_row
                                       ).dropna(subset=merge_on).drop_duplicates(subset=merge_on)
                           for file in file_list]
    
    if verbose:
        click.echo('loaded files: ' + str(len(data_frame_list)))
    
        

    #ensure the merge_on column exists in all files
    # unique_ids = []
    for df,source_file in zip(data_frame_list,file_list):
        #  check each merge column
        for merge_col in merge_on:
            if not(merge_col in df.columns):
                click.echo(source_file + 'does not have column ' + merge_col)
                # will errror out later, but this allows full list or problems to be printed
    
    if verbose:
        click.echo('all have the merge column')

    # merge the first two
    #   use source data file as suffix for all columns that repeat
    out_df = pd.merge(data_frame_list[0], data_frame_list[1], how=merge_type,
                      suffixes=('_'+file_list[0][:-4],'_'+file_list[1][:-4]),
                      on=merge_on)
    
    if verbose:
        click.echo(
            'first pair (' + file_list[0] + ', ' + file_list[1] + ') merged')
    
    # if more, keep merging
    if len(file_list) >2:
        for next_df,source_file in zip(data_frame_list[2:],file_list[2:]):
            # note the size before merging for debugging
            if verbose:
                r,c = next_df.shape
                msg = 'adding {source_file} ({r},{c})'
                click.echo(msg.format( source_file=source_file,r=r,c=c))

            # merge the previous with the new one, 
            #  first suffix blank because it's many sub-frames that have already been merged
            out_df = pd.merge(out_df, next_df, on = merge_on, how=merge_type,
                              suffixes=('', '_'+source_file[:-4]))
            
            #  describe total size if successful in debug mode
            if verbose:
                r,c = out_df.shape
                added_msg = 'added {source_file} total size is now ({r},{c})'
                click.echo(added_msg.format(source_file=source_file, r=r, c=c))
    
    
    # note that staring to save
    if verbose:
        click.echo('all merged, saving next')

    
    # formate file name for saving use provided name if provided or folder name otherwise 
    if out_name:    
        if not(out_name[-4:] == '.csv'):
            out_name += '.csv'
    else:
        out_name = folder.strip('/')+'.csv'

    # save
    out_df.to_csv(out_name)

    # report success, always
    done_msg = 'wrote out ({r},{c}) to {out_name}'
    r,c =out_df.shape
    click.echo(done_msg.format(out_name=out_name,r=r,c=c))
    # return out_df