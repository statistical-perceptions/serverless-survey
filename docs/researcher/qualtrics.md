# Coordinating with Qualtrics 


```{important}
This is the base documentation that may need updates
```

## Basic use

1. the first qualtrics survey sends embedded data via forwarding only
2. middle ones receive data and send data 
3. the last one receives data only

### Sending the ID from Qualtrics

1. Add an embedded data block with the identifier to forward (eg panel ID or Response ID)
2. redirect end of survey to a url
3. embed the response id in the forwarding url:

Template
```
https://statistical-perceptions.github.io/IdentiCurve/<question_out_html_file>.html?id=<qualtrics piped text>
```

Example

```
https://statistical-perceptions.github.io/sample-nobackend/?id=${e://Field/ResponseID}
```
in this case, I only had one question page so there is no question_id set and I used the ResponseID feild. 

note:
- if needed, we can pass more than a single unique identifier on, but that requires code changes


### Recieving Data into Qualtrics

1. set up embedded data as the first block on the workflows tab. set the variables as per the instructions output
2. (if applicable) use piped text to refer to those values in the question text
3. (optional) add a branch after the embedded data to have people skip the survey "if id is Equal to demo" 

- [getting data from url](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/embedded-data/#SettingValuesFromTheSurveyURL)


### Branching to different ss questions based on qualtrics answers 

1. on the survey flow tab add a branch
2. set the condition to be based on a question
3. add the url to forward to
4. (if applicable) add the variable value to the forward url 


Template
```
https://statistical-perceptions.github.io/IdentiCurve/<question_out_html_file>.html?id=<qualtrics piped text>&var=value
```

Example

```
https://statistical-perceptions.github.io/sample-nobackend/?id=${e://Field/ResponseID}&group=w
```
in this case, I only had one question page so there is no question_id set and I used the ResponseID feild. 

### Branching to different ss questions based on embedded data

1. make sure the embedded data received includes the pass through variable
2. on the survey flow tab add a branch
3. set the condition to be based on embedded data and choose the values
4. add the url to forward to
5. (if applicable) add the variable value to the forward url 


Template
```
https://org-or-user.github.io/repo/question_out_html_file.html?id=<qualtrics piped text>&var=value
```

Example

```
https://statistical-perceptions.github.io/IdentiCurve/nc2t1w.html?id=${e://Field/ResponseID}&group=${e://Field/group}
```

### Semi-automatic forwarding to different qustions

In order to have a survey where there are different versions of the questions for different participants depending on a response of a question, set up a question in qualtrics where the response will be the "logic variable." Then make it so that the logic variable is passed along with the ID and its values appear in the url so that the variable in piped text can make it work.  

1. set up configurations so that the logic variable values are in the question ids (or html file names)
2. make sure embedded data received includes the variable used for logic
3. set up the url like (for `group` as the logic variable)


```
https://ghorg.github.io/repo/page_url${e://Field/logicvariable}.html?id=${e://Field/ResponseID}&group=${e://Field/logicvariable}
```
 
For example if the following is in qualtrics as the forward url 


```
https://statistical-perceptions.github.io/IdentiCurve/nc2t1${e://Field/group}.html?id=${e://Field/ResponseID}&group=${e://Field/group}
```

when `group=a` the url will become

```
https://statistical-perceptions.github.io/IdentiCurve/nc2t1a.html?id=RH2904&group=a
```

## Qualtrics Help 

- [Passing with Query Strings](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/passing-information-through-query-strings/): about the url
- [Piped text](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/piped-text/piped-text-overview/): about getting and formatting variables for the url or for using responses to modify qualtrics questions
- [embedded data](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/embedded-data/): for storing data to send and receive it

