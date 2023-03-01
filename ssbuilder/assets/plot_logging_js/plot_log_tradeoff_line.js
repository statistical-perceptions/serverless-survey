// get object
var myPlot = document.getElementById('{question_id}');

// watch the plot, act on changes
myPlot.on('plotly_afterplot', function () {{
     // curly braces are escaped for python processeding, thats thwy they are doubled
    {{
        // console.log(myPlot.data.slice(6,))
        // extract the active trace
        traces = myPlot.data.slice(6,)
        var curTrace = traces.filter(trace => trace.visible == true)[0];
        //  assign the values from metadata
        //  the meta available are set in the python code that generates the plot
        //  this allows the passed value names (that are referenced in the form) to be configured
        document.getElementById("{location_var_name}").value = curTrace.meta.location;
    }}
}});
// curly are escaped for python processeding, thats thwy they are doubled