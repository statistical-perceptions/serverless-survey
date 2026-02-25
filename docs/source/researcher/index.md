# Researcher Guide

```{toctree}
configuration.md
questions.md
qualtrics.md
analysis.md
```

## What it does

Serverless survey transforms a configuration file of questions and plot settings and generates a set of html files that comprise a survey that will, upon submission forward to another service, typically qualtrics. 


## Recommended Use

We recommend using [our provided template repo](sstemplate) and creating one repository per study or project.  A study may have multiple surveys in it, but will all be hosted in the same place. Treat each repository as a separate folder, with no nesting. 

In this case your overall workflow will include the following steps:
1. Use [template](sstemplate) (more details in template README)
3. Start your qualtrics study(ies) to get the URLs for forward from the generated questions
2. Set up your study in the configuration file [following yaml guide, page settings,](configuration_yaml) and [question specific settings](questions)
5. Build the survey using actions in your study repo  (more details in [template](sstemplate) README)
6. Use the generated instructions to set up your qualtrics survey to forward and recieve data using embedded data following our [qualtrics instructions page](qualtrics)
7. check at the end of the instructions page that your study does not need to send more than the maximum amount of data to qualtrics at once
8. Take your survey, entering plausible values to check that your data is showing up as expected in qualtrics (check all of the surveys). 
9. Run your study! 

**Notes**:
- your repo can be private, but you do have to turn on the github pages
- there is a limited number of characters that can be passed, but it is not well documented and varies browser to browser.  We recommend no more than 2000 characters passing to qualtrics at each time.  You can split into multiple surveys for longer studies. 

You'll then have a set of data files to merge together to combine multiple sections and be able to analyze your data. 

## Use details

There is a CLI tool and it generates html files in a single folder.  These files can then be hosted anywhere. 

The CLI includes two main commands: 
- `ssgeneratehtml` generates the html files and instructions md file. 
- `sslengthcheck` checks the length of the forwarded message after a study has been generated. It uses the instructions file as input

[sstemplate]: https://github.com/statistical-perceptions/ss-template