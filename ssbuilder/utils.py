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

