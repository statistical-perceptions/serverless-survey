// get object
var myPlot = document.getElementById('{question_id}');

// watch the plot, act on changes
myPlot.on('plotly_afterplot', function () {{
     // curly braces are escaped for python processeding, thats thwy they are doubled
    {{
        // extract the active trace
        var curTrace = myPlot.data.filter(trace => trace.visible === true);
        //  assign the values from metadata
        //  the meta available are set in the python code that generates the plot
        //  this allows the passed value names (that are referenced in the form) to be configured
        document.getElementById("{location_var_name}").value = curTrace[1].meta.location;
        document.getElementById("{overlap_var_name}").value = curTrace[1].meta.overlap;
    }}
}});
// curly are escaped for python processeding, thats thwy they are doubled