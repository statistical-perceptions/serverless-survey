# Coordinating with Qualtrics 


```{important}
This is the base documentation that may need updates
```

## Overview

1. the first qualtrics survey sends data to normal curve only
2. middle ones receive data from and send data to the normal curve
3. the last one receives data only

## Qualtrics -> SS

1. Add an embedded data block with the identifier to forward (eg panel ID or Response ID)
2. redirect end of survey to a url
3. embed the response id in the forwarding url:

Template
```
https://statistical-perceptions.github.io/IdentiCurve/<question_out_html_file>.html?id=<qualtrics piped text)
```

Example

```
https://statistical-perceptions.github.io/sample-nobackend/?id=${e://Field/ResponseID}
```
in this case, I only had one question page so there is no question_id set and I used the ResponseID feild. 

note:
- if needed, we can pass more than a single unique identifier on, but that requires code changes


### SS -> qualtrics

1. set up embedded data as the first block on the workflows tab
2. (if applicable) use piped text to refer to those values in the question text
3. (optional) add a branch after the embedded data to have people skip the survey "if id is Equal to demo" 

- [getting data from url](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/embedded-data/#SettingValuesFromTheSurveyURL)
- 

## Qualtrics Help 

- [Piped text](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/piped-text/piped-text-overview/)
- [sum question](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/question-types-guide/specialty-questions/constant-sum/)
- [embedded data](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/embedded-data/)

