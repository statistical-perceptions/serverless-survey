# Overview

## What it does

Serverless survey transforms a configuration file of questions and plot settings and generates a set of html files that comprise a survey that will, upon submission forward to another service, typically qualtrics. 


## Recommended Use

We recommend using [our provided template repo](sstemplate) and creating one repository per study or project.  A study may have multiple surveys in it, but will all be hosted in the same place. Treat each repository as a separate folder, with no nesting. 

In this case your overall workflow will include the following steps:
1. Use [template](sstemplate) (more details in template README)
2. Set up your study in the configuration file [following yaml guide, page settings,](configuration_yaml) and [question specific settings](questions)
3. Set up your qualtrics survey to forward and recieve data using embedded data following our [qualtrics instructions page](qualtrics)
4. Build the survey using actions in your study repo  (more details in [template](sstemplate) README)
5. Test to check that your data is showing up as expected in qualtrics (check all of the studies)
6. Run your study! 

You'll then have a set of data files to merge together to combine multiple sections and be able to analyze your data. 

[sstemplate]: https://github.com/statistical-perceptions/ss-template