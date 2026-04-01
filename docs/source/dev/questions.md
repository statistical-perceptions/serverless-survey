# Question Implementation 

Each question type is implemented as a class the class also specifies the HTML/js templates to use for that question type. The constructor documents the logging variables that can be passed. 


To add a new question, you'll need a new class that has: 
- a constructor method that takes `logging_vars` dictionary, ideally with specified defaults
- a `generate_figure` method that can take any necessary parameters and returns a plotly figure object. 

Additionally, you'll need to add:
- a `plot_log_<questiontype>.js` file to `assets/plot_logging_js`
- an HTML template for the form that can be loaded and filled in as a python fstring.  


The keys in the `logging_vars`  dictionary should match the template feilds in the HTML template. 

The javascript needs to: 
1. get the object by `question_id`
1. on `plotly_afterplot`, extract the attributes of the plot that are the question answer


```javascript
var myPlot = document.getElementById('{question_id}');
```