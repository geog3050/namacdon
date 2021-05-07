# Final Project
This is my final project page. Here, you can view the code and some images of the
results from the project.

## Introduction
For my final project, I explored the creation and implementation of a geospatial programming code collection that utilizes satellite imagery to analyze land productivity in the South Caucuses, specifically seeking to study how it has been impacted by Armenia and Azerbaijan’s dispute over the Nagorno-Karabakh region. Due to the decades of conflict, land productivity and consistent settlement has been an issue for the area’s inhabitants. In this project, we studied 30+ years of remote sensing imagery data to try and detect trends and changes in the landscape’s usage. This involved the use of Google Earth Engine as the data repository, and geospatial programming techniques as the functional environment, including Python libraries such as arcpy, numpy, and others.

### Background
Armenia and Azerbaijan have been continually in conflict since their independence from the Soviet Union. In fact, disputes in these countries in the early 1990s are cited as being one of the major factors in the USSR’s dissolution, as the central government was unable to effectively handle the tensions that boiled over in the South Caucuses. In the ensuing 30 years, the two countries have repeatedly fought over disputed land areas, with each country occupying territories that are internationally recognized as belonging to the other. There were major military actions as recently as last year, with borders changing and populations being displaced. This constant cycle of conflict has led to major disruptions in primary production in the disputed areas, which is something that can be studied using remote sensing and geospatial analysis. Vegetation phenology is well-suited for observation from satellite-based remote sensing. Spectral indexes such as the Normalized Difference Vegetation Index (NDVI), which uses the Red and Near-Infrared bands of imagery, can act as a proxy for vegetative health. This can be applied to a time-series of images over the same location to detect trends and changes over time.

The literature on this subject has several excellent examples of this type of analysis. Witmer (2008) used Landsat data to map detect agricultural abandonment following the war in Bosnia, finding it a viable substitute for studies in areas too dangerous to conduct fieldwork in. Hagenlocher, Lang, and Tiede (2012) used high resolution imagery to study changes in vegetation cover around IDP camps in Sudan. Most relevant to the area of interest in this study, Baumann, Radeloff, Avedian, and Kuemmerle (2014) used Landsat imagery to assess land cover change in Nagorno-Karabakh, using post-classification comparison of images from three years (1987, 2000, and 2010) to detect large-trend changes in the landscape. Similar to Witmer, they found that land abandonment due to active conflict is slow to be rehabilitated, often due to land mines and depopulation effects in the conflict area. My project will seek to increase the detail of these previous studies by using all of the available imagery versus selected dates, as well as employing more up-to-date classification and change detection methods. This will all be performed in a coding environment suitable for reuse and application to other areas of interest.

### Goal
In this project, I gathered data relevant to the Nagorno-Karabakh region that is disputed by Armenia and Azerbaijan. This is primarily multispectral satellite imagery, and from this spectral indexes relevant to vegetation phenology were calculated. This is possible because certain wavelengths have been proven to correlate with aspects of vegetative health, water moisture content, and other vital characteristics that can serve as a remotely-sensed proxy for vegetation growth or decline.

### Objectives
The objectives of this project are to detect areas that have undergone growth or decline in primary production in the specified area of interest. A main focus is on attempting to isolate changes to agricultural production, but other symptomatic evidence of human-environment alterations are also of interest, such as regrowth over land previously cleared for settlement, de- or reforestation, etc. As mentioned previously, there have been many studies conducted that use environmental changes as a proxy for human settlement disturbances, as direct observation of human-scale features is often impossible at the temporal and spatial resolutions available. The much larger-scale and temporally-durable impacts that humans have on their environment is easier to observe remotely, and from this we can make inferences about the human-led causes. However, much of the work previously conducted on this subject has been executed with manual data collection and processing techniques, therefore making it unable to be easily reproduced and applied to other areas of interest. By using an open-source imagery repository like GEE and providing to the public the source code employed, an additional objective of this study is to provide an openly-accessible suite of geospatial programming code that can be easily transferred to other regions or applications.

### Data
#### Google Earth Engine
Google Earth Engine (GEE) is a server-based repository of imagery and coding tools that allows advanced mapping, analysis, and visualization operations to be performed with minimal client-side requirements. This means that users of the service do not need to have high-end computing equipment, expensive software packages, or even high-speed internet access, instead retaining all of these technologically-intensive requirements on the Google servers. GEE’s data catalog includes imagery from the major open-access, space-based Earth Observation (EO) systems, such as Landsat, MODIS, Sentinel, and others, as well as many derived products and other sources of geospatial data. For this project, we will be utilizing the Landsat program’s data.

#### Landsat
Landsat is NASA and USGS’s primary EO system, with seven different satellite sensors named Landsat having been successfully gathering images of the Earth’s surface since the 1970s. Landsat 6 failed to achieve orbit and threatened the continuity of this dataset, but Landsat 5 was kept operational for an extraordinary 29 years. Landsat 8 was launched in 2013 and provides 16-day revisit ability at 30m MSI and 15m panchromatic from the Operational Land Imager (OLI) sensor, as well as thermal imagery from its Thermal Infrared Sensor (TIRS). Landsat 9, with an equivalent sensor package Landsat 8, is scheduled for launch in 2021 and will assume Landsat 7’s orbital path. There are numerous conflicts and major events that have occurred in this timeframe, at many scales and in many locations, making the long-baseline, highly accurate Landsat program an ideal source of RS data for studying violent conflict and its impacts. For this study in particular, I will use data from Landsats 5, 7, and 8 to cover the last 30 years, focusing on the Nagorno-Karabagh region and the changes in the landscape since the fall of the Soviet Union.

```
Satellite	 Launched	Decommissioned	Sensor	 Resolution
Landsat 5	  1984	        2013	          TM	    30m
Landsat 7	  1999	        Operational	  ETM+	    30m
Landsat 8	  2013    	Operational	  OLI	    30m
```

#### Other Data
Political boundaries will be included to help identify regions and areas of interest. This will be done through Google Earth Engine’s repository of feature classes, as well as importing or creating polygons as needed (such as for unrecognized/informally-designated areas).

## Workflow

![workflow](https://github.com/geog3050/namacdon/blob/f680ff7b8a4695d713c7b11a1e4ecd8299ac1470/Final_Project/workflow.png)

## References
```
Baumann, M., Radeloff, V. C., Avedian, V., & Kuemmerle, T. (2014). Land-use change in the Caucasus during and after the Nagorno-Karabakh conflict. Regional Environmental Change, 15(8), 1703-1716. doi:10.1007/s10113-014-0728-3
Hagenlocher, M., Lang, S., & Tiede, D. (2012). Integrated assessment of the environmental impact of an IDP camp in Sudan based on very high resolution multi-temporal satellite imagery. Remote Sensing of Environment, 126, 27-38. doi:10.1016/j.rse.2012.08.010
Witmer, F. D. W. (2008). Detecting war‐induced abandoned agricultural land in northeast Bosnia using multispectral, multitemporal Landsat TM imagery. International Journal of Remote Sensing, 29(13), 3805-3831. doi:10.1080/01431160801891879
```
