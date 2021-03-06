# GEOG:5500 Repository

This is the repository for my GEOG:5500 class at the University of Iowa. It
contains the code developed for assignments and quizzes during the class, as
well as the code for the final project.

## Table of Contents

1. [Assignments](Assignments): All of the code for assignments in the class.
2. [Example Code](Example_Code): Short coding snippets that I have created for
other projects or just for fun.
3. [Final Project](Final_Project): The repository for my final project code.

## Getting Started

### Environments

In order to use the code in this repository, some specific Python
environments need to be created.

```
Required packages:
Google Earth Engine Python API (ee)
ESRI ArcGIS Python API (arcpy)
```

### Installing Packages

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

## Applications

This code is designed around creating functional geoprocessing tools for expediting
tasks and functions. The final project in particular is a suite of coding tools
for acquiring imagery using the Google Earth Engine application, then readying it
in ArcGIS for use in Deep Learning models. The pipeline allows the user to select
the area of interest, date ranges, and other aspects of the imagery to be retrieved,
then prepares it in ArcGIS by developing labeled image chips in a DL model.

## About the Author

### Background

Please see my <a href="https://geog3540.github.io/namacdon/images/MacDonald_CV.pdf">
Curriculum Vitae</a> and <a href="https://geog3540.github.io/namacdon/bio/index.html">
Biography</a>.

## License

All of the code herein is [MIT licenced](license.txt).
