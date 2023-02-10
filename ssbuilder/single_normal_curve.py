import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import norm
import click
import yaml

'''
File Contents
- function to generate a slider object using plotly
- html template components
- function to generate html from components 
- function to generate multiple html from configuratio file 

To edit html, edit the template strings in the middle of the file 

'''


def normal_curve_slider(static_name='other group', static_color="#CE00D1", 
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
    if not(min_slider_value):
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

    # if hide_y_ticks:
    #     fig.update_layout(
    #         xaxis = dict(
    #             tickmode='array',
    #             ticktext=['One, 'Three', 'Five', 'Seven', 'Nine', 'Eleven']'
    #     )
    #     )

    return fig

# Start templates ------------------------------------------
#  see the order they are combined in the make html function

# this is the beginning of the form 
#  this is all invisible
form_top_html_template = '''
<!-- form to send to qualtrics -->
<form action="{next_question_url}" method="GET">
    <div>
        <!-- hidden field for ID to pass on-->
        <input name="id" id="id" type="hidden" value="demo"/>
    </div>
    <div>
        <!-- hidden field to pass on location value-->
        <input name="{location_var_name}" id="{location_var_name}" value="-1" type="hidden" />
    </div>
    <div>
        <!-- hidden field to pass on overlap value-->

        <input name="{overlap_var_name}" id="{overlap_var_name}" value="default" type="hidden" />

    </div>
'''

#  for possible more validation in above
# required = "required"
# oninvalid = "this.setCustomValidity('This is a demo, cannot submit')"
# oninput = "this.setCustomValidity('')"

# end of the form
#    separate from above so that the plot  can go in the middle
#  this is all of the visible parts 
form_end_html = '''
    <div>
        <div class="form-check form-check-inline">
        <label for="{confirm_id}" class="form-check-label">{confirm_message}</label>
    
        <input name="{confirm_var_name}" id="{confirm_id}" value="confirmed" type="radio"  class="form-check-input" required="required"/>
    </div>
    <div class="form-check form-check-inline">
        <label for="{skip_id}" class="form-check-label">{skip_message}</label>
        <input name="{confirm_var_name}" id="{skip_id}" value="skip" type="radio"  class="form-check-input"  />
    
    </div>
        <input type="submit" class="btn btn-primary"/>
    </div>

'''

#  this sets up the actual html file 
page_header_template = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{page_title}</title>
    <!-- uncomment and add an icon to make one appear --> 
    <!-- <link rel="icon" href="./favicon.ico" type="image/x-icon"> -->
    
</head>

<body>

'''

# this ends the html file and includes the processing scripts 
page_footer_template = '''
</form>


<script>
    // prefill id from URL with incoming
    (new URL(window.location.href)).searchParams.forEach((x, y) =>
            document.getElementById(y).value = x);

    <!-- script to pull data from plot into form -->
    // get object
    var myPlot = document.getElementById('{question_id}');

    // watch the plot, act on changes
    myPlot.on('plotly_afterplot', function () {{
        // extract the active trace
        var curTrace = myPlot.data.filter(trace => trace.visible === true);
        //  assign the values from metadata
        document.getElementById("{location_var_name}").value = curTrace[1].meta.location;
        document.getElementById("{overlap_var_name}").value = curTrace[1].meta.overlap;
    }});

</script>
</body>

</html>

'''

# this is the main body of the question
card_body_template = '''
<div class="card text-center w-75 mx-auto my-5">
  <div class="card-header">
    {question_text}
  </div>
  <div class="card-body">
     {plot_html}
  </div>
  <div class="card-footer text-muted">
    {form_end}
  </div>
</div>

'''

settings_message_template = ''' ---------------------------
Created: [https://statistical-perceptions.github.io/IdentiCurve/{out_html_file}](docs/{out_html_file})
Forwards to: {next_question_url}.
Sends: id, {location_var_name}, {overlap_var_name}, {confirm_var_name}
'''

def make_question_page(question_id, figure=None, figure_values = None,
                       page_title = 'Normal Curve Question',
                       question_text = 'Move the slider',
                       confirm_message = 'Confirm my answer',
                       skip_message = 'Prefer not to answer',
                       out_html_file=None,
                       location_var_name=None,
                       overlap_var_name=None,
                      confirm_var_name=None,
                       var_name_suffix=True, 
                       pretty_url=False,
                      next_question_url='https://uri.co1.qualtrics.com/jfe/form/SV_3rU4XfDtiVN8HMW'):
    '''
    generate html file
    
    Parameters
    ----------
    question_id : string {required}
        name for the question internally
    figure : figure object 
        from normal_curve_slider otherwise will use default values
    figure_values : dictionary
        parameters to pass to normal_curve_slider
    page_title : string
        what to show in the tab title default = 'Normal Curve Question',
    question_text : string
        the text of the questions
    confirm_message : text
        prompt for confirmation
    skip_message : text 
        prompt for skipping
    out_html_file : string
        name fo the html file, that will be in the url for the participant 
        if not passed will add ".html" to the questionid
    location_var_name : string {'loc'}
        name for the variable of the location, if not passed will be 'loc' +question_id
    overlap_var_name : string {'ov'}
        name for the variable of the location, if not passed will be 'ov'  +question_id
    confirm_var_name : string {'confirm'}
        name for the variable, if not passed will be question_id + 'confirm'  +question_id
    var_name_suffix : boolean {True}
        if true, add question_id to the passed values for all _var_names. Default is True,
        can be changed to False if you specify the variable names directly
    next_question_url : string
        url for the next qualtrics question
    pretty_url : boolean {False}
        if True make pages like `/IndentiCurve/name/` instead of `/IdentiCurve/name.html` 
        
    Notes
    -----
    variables with _var_name + "id" will be passed to qualtrics
    '''
    #format this
    question_id = question_id.replace('/','').replace(' ','-').lower()
    
    #     ensure file name is valid
    if not(out_html_file):
        out_html_file = question_id + '.html'
    elif not(out_html_file[-5:]=='.html'):
        out_html_file += '.html'
    
     
    out_html_file =out_html_file.replace('/','').replace(' ','-').lower()

    
    # fix defaults
    if not(location_var_name):
        location_var_name =  'loc'
        
    if not(overlap_var_name):
        overlap_var_name = 'ov'
      
    if not(confirm_var_name):
        confirm_var_name = 'confirm'
        
    if var_name_suffix:
        location_var_name += question_id
        overlap_var_name += question_id
        confirm_var_name += question_id
    
    # generate figure if not passed
    if not(figure):
        if not(figure_values):
            figure = normal_curve_slider()
        else:
            figure = normal_curve_slider(**figure_values)
    
    # get figure html 
    plot_html= figure.to_html(include_plotlyjs='cdn',full_html=False,div_id=question_id)
    
    # combine all template variables 
    page_info = {'page_title':page_title,
                'question_text':question_text,
                'location_var_name':location_var_name,
                'overlap_var_name':overlap_var_name,
                'plot_html':plot_html,
                'confirm_message':confirm_message,
                'skip_message':skip_message,
                'confirm_var_name':confirm_var_name,
                'skip_id':question_id +'skip',
                'confirm_id':question_id+'confirm',
                'question_id':question_id,
                'next_question_url':next_question_url,
                'out_html_file':out_html_file}
    # this goes inside the card body
    page_info['form_end']= form_end_html.format(**page_info)
    
    
    # fill in all of the template variables and build a string that is the content
    page = page_header_template.format(**page_info) 
    page += form_top_html_template.format(**page_info)
    page += card_body_template.format(**page_info)
    page += page_footer_template.format(**page_info)



    ## format the final path
    if pretty_url:
        subdir = out_html_file[:-5]
        out_html_file = os.path.join('docs', subdir, 'index.html')
    else:
        out_html_file = os.path.join('docs', out_html_file)

    ## Write the pate
    with open(out_html_file, 'w') as f:
        f.write(page)
    
    
    # this is for the user
    #    notebook exmaples print it as markdown
    #    config generator capturs into a file
    return settings_message_template.format(**page_info)

@click.command()
@click.option('--config-file')

def generate_from_configuration(config_file=None):
    '''
    Generate html files from a configuration file
    '''
    if not(config_file):
        config_file = 'configuration.yml'
        instruction_file = 'instructions.md'
    else:
        instruction_file = config_file[:-4] + '-instructions.md'

    with open(config_file, 'r') as f:
        loaded_config = yaml.load(f, Loader=yaml.Loader)


    instructions = [make_question_page(**q) for q in loaded_config]

    with open(instruction_file,'w') as f:
        f.write('\n'.join(instructions))
