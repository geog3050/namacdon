# Project Title

This is the repository for my GEOG:5500 class at the University of Iowa. It
contains the code developed for assignments and quizzes during the class, as
well as the code for the final project.

## Getting Started

In order to use the code in the final project folder, some specific Python
environments need to be installed.

### Environments

Google Earth Engine, which typically runs on Javascript inside the GEE client,
is also available as a Python package.<br/>
If installing with conda, follow the instructions
<a href="https://developers.google.com/earth-engine/guides/python_install-conda">
here</a>, otherwise you can install from the command line using:

```
!pip install google-api-python-client
```
Additionally, ESRI's arcpy package is used to implement certain functions to
preprocess and classify the imagery. While this does require a paid license to
operate, the code is annotated so that you could replicate the steps in an
open-source system such as QGIS.
