import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)


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


def calculate_query_length(filename, vars_only=False,
                           id_length=10, value_length=3, exclude_base=False):
    """
    Check the length in characters of the string to be passed, not including values

    Parameters
    ----------
    filename : str
        The path to the instruction file to check
    vars_only : bool {False}
        if True return length of the variables and joiners only, no prefix or assumed value lengths
    id_length : int {10}
        length of unique identifier in characters
    value_length : int {3}
        average length in characters of values passed, other than id
    exclude_base : bool {False}
        exclude the base of the forward address from the count

    Returns
    -------
    est_chars : int
        estiminated character length (loose lower bound of true)
    """
    est_chars = 0
    with open(filename, 'r') as f:
        file_lines = f.readlines()

    send_strings = [s for s in file_lines if 'Sends: [' in s]

    # create template message
    if vars_only:
        message_template = '&='
        id_length = 0
    else:
        message_template = '&=' + 'x' * value_length

    # use template to find longest length
    format_message = lambda s: s[8:-2].replace("'",'').replace(', ', message_template)
    message_lengths = [len(format_message(s)) for s in send_strings]
    longest_msg_length = max(message_lengths)
    est_chars += longest_msg_length

    if not exclude_base:
        # find in file to get forward url
        longest_send_idx = message_lengths.index(longest_msg_length)
        longest_raw_text = send_strings[longest_send_idx]
        longest_file_idx = file_lines.index(longest_raw_text)
        fwd_url = file_lines[longest_file_idx - 1].replace('Forwards to: ', '')
        if 'http' not in fwd_url:
            cur_created = file_lines[longest_file_idx - 2]
            cur_url_start = cur_created.index('[') + 1
            cur_url_end = cur_created.index(']')
            cur_url = cur_created[cur_url_start:cur_url_end]
            fwd_url = '/'.join(cur_url.split('/')[:-1]) + '/' + fwd_url

        est_chars += len(fwd_url)

    if id_length:
        prefix_length = len('?id=') + id_length
        est_chars += prefix_length

    return est_chars


def merge_dir_csvs(folder, merge_on='id', out_name=None, header=0,
                   verbose=False, skip_row=(), complete_only=False):
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
    skip_row : list of int
        rows to skip, as a list (passed one at a time using multiple uses of the flag)
    verbose : bool
        print extra information out for debugging
    complete_only : bool
        if True use an inner merge, if not use outer merge

    Returns
    -------
    out_name : string
        path of the written CSV file
    '''
    merge_type = 'inner' if complete_only else 'outer'

    # get all of the files, sort alphabetically
    file_list = sorted([file for file in os.listdir(folder) if file[-4:] == '.csv'])
    if verbose:
        logger.info('found files: %d', len(file_list))
        logger.info('\n'.join(file_list))

    # load all of the datafiles, applying the same skip and header to each file
    # drop any rows that have no value for the merge column
    # drop any duplicate values for the merge columns
    data_frame_list = []
    for file in file_list:
        try:
            data_frame_list.append(pd.read_csv(os.path.join(folder, file),
                                               header=header,
                                               skiprows=lambda x: x in skip_row
                                               ).dropna(subset=merge_on).drop_duplicates(subset=merge_on))
        except Exception as e:
            e.add_note(file)
            raise

    if verbose:
        logger.info('loaded files: %d', len(data_frame_list))

    # ensure the merge_on column exists in all files
    for df, source_file in zip(data_frame_list, file_list):
        for merge_col in merge_on:
            if merge_col not in df.columns:
                logger.warning('%s does not have column %s', source_file, merge_col)
                # will error out later, but this allows full list of problems to be logged

    if verbose:
        logger.info('all have the merge column')

    # merge the first two
    # use source data file as suffix for all columns that repeat
    out_df = pd.merge(data_frame_list[0], data_frame_list[1], how=merge_type,
                      suffixes=('_' + file_list[0][:-4], '_' + file_list[1][:-4]),
                      on=merge_on)

    if verbose:
        logger.info('first pair (%s, %s) merged', file_list[0], file_list[1])

    # if more, keep merging
    if len(file_list) > 2:
        for next_df, source_file in zip(data_frame_list[2:], file_list[2:]):
            if verbose:
                r, c = next_df.shape
                logger.info('adding %s (%d, %d)', source_file, r, c)

            out_df = pd.merge(out_df, next_df, on=merge_on, how=merge_type,
                              suffixes=('', '_' + source_file[:-4]))

            if verbose:
                r, c = out_df.shape
                logger.info('added %s — total size is now (%d, %d)', source_file, r, c)

    if verbose:
        logger.info('all merged, saving')

    # format file name: use provided name or derive from folder
    if out_name:
        if not out_name.endswith('.csv'):
            out_name += '.csv'
    else:
        out_name = folder.strip('/') + '.csv'

    out_df.to_csv(out_name)
    return out_name
