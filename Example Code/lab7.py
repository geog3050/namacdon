import ee

# Bound location for reducers.
loc = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level2') \
    .filter("ADM1_NAME == 'Iowa'") \
    .filter(ee.Filter.eq('ADM1_NAME','Iowa')) \
    .geometry()

Ames = ee.Geometry.Point([-93.62979103572975, 42.0262680827013]).buffer(8000),
FortDodge = ee.Geometry.Point([-94.17104381434059, 42.50086891347599]).buffer(6000),
CouncilBluffs = ee.Geometry.Point([-95.86256079461845, 41.26153419246502]).buffer(8000),
DesMoines = ee.Geometry.Point([-93.63577581043222, 41.586879593468105]).buffer(11000),
MasonCity = ee.Geometry.Point([-93.20075733699181, 43.15251917288241]).buffer(6000),
Waterloo = ee.Geometry.Point([-92.3408552974903, 42.493158356413744]).buffer(8000),
Dubuque = ee.Geometry.Point([-90.68219726210572, 42.50743365723641]).buffer(8000),
Clinton = ee.Geometry.Point([-90.20172376068327, 41.845362170470885]).buffer(6000),
Davenport = ee.Geometry.Point([-90.55420439540134, 41.54157190356464]).buffer(11000),
Ottumwa = ee.Geometry.Point([-92.41311726516487, 41.01299522892045]).buffer(6000),
CedarRapids = ee.Geometry.Point([-91.67457713644235, 41.97642149349897]).buffer(11000)

# Create a feature collection of all the geometries
geometries = ee.FeatureCollection([DesMoines, Davenport, CedarRapids,
Ames, CouncilBluffs, Dubuque, Waterloo, MasonCity, Ottumwa, FortDodge, Clinton])

# Establish function for Landsat 7 and 8 cloud masks (stock GEE code)
def maskL8sr(image):
  cloudShadowBitMask = (1 << 3)
  cloudsBitMask = (1 << 5)
  qa = image.select('pixel_qa')
  mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
  return image.updateMask(mask)
def cloudMaskL457(image):
  qa = image.select('pixel_qa')
  cloud = qa.bitwiseAnd(1 << 5).And(qa.bitwiseAnd(1 << 7)).Or(qa.bitwiseAnd(1 << 3))
  return image.updateMask(cloud.Not())

# Import Landsat image collections, Landsat 7 for before and Landsat 8 for after
datasetb1 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR') \
  .filterDate('2002-07-01', '2002-09-10').map(cloudMaskL457)
datasetb2 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR') \
  .filterDate('2001-07-01', '2001-09-10').map(cloudMaskL457)
datasetb3 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR') \
  .filterDate('2000-07-01', '2000-09-10').map(cloudMaskL457)
dataset1 = datasetb1.merge(datasetb2).merge(datasetb3)
dataset2 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
  .filterDate('2020-07-01', '2020-09-10').map(maskL8sr)

# Define function for NDVI
def NDVI7(image):
  return image.normalizedDifference(['B4','B3'])

def NDVI8(image):
  return image.normalizedDifference(['B5','B4'])


# Define function for SAVI
def NDWI7(image):
  return image.normalizedDifference(['B4','B5'])

def NDWI8(image):
  return image.normalizedDifference(['B5','B6'])


# Make palattes for natural color imagery
visParams7 = {'bands': ['B3',  'B2',  'B1'], 'min': 0, 'max': 3000, 'gamma': 1.4,}
visParams8 = {'bands': ['B4',  'B3',  'B2'], 'min': 0, 'max': 3000, 'gamma': 1.4,}

# Make palette for color scale for change vetor map
cvect_params = {'min': -3.142, 'max': 3.142, 'palette': ['f9316d','fdca41','57ad2f','311687']}

# Make palette for UID (green/red)
ndvi_params = {  'min': 0, 'max': 1, 'palette': ['f6b9bd','ef848b','e9505a','ba4048','74282d']}

# Map the functions over the collections, and reduce to turn image collections into single images.
befN = dataset1.map(NDVI7).median()
befW = dataset1.map(NDWI7).median()
aftN = dataset2.map(NDVI8).median()
aftW = dataset2.map(NDWI8).median()
NDVIdiff = aftN.subtract(befN)
NDWIdiff = aftW.subtract(befW)

# Calculate change magnitude
NDVIdiffsq = NDVIdiff.pow(2)
NDWIdiffsq = NDWIdiff.pow(2)
sumsqrs = NDVIdiffsq.add(NDWIdiffsq)
cmag = sumsqrs.sqrt()

# Create "mean plus 1 standard deviation" threshold mask
reducers = ee.Reducer.mean().combine({
  'reducer2': ee.Reducer.stdDev(),
  'sharedInputs': True
})
stats_cmag = cmag.reduceRegion({
    'reducer': reducers,
    'geometry': geometries,
    'scale': 30,
   'bestEffort': True
})
stats_uid = NDVIdiff.reduceRegion({
    'reducer': reducers,
    'geometry': geometries,
    'scale': 30,
   'bestEffort': True
})
stdevc = ee.Number(stats_cmag.get('nd_stdDev'))
meanc = ee.Number(stats_cmag.get('nd_mean'))
stdevu = ee.Number(stats_uid.get('nd_stdDev'))
meanu = ee.Number(stats_uid.get('nd_mean'))
cmag_thresh = cmag.updateMask(cmag.gt(meanc.add(stdevc.multiply(2))))
uid_thresh = NDVIdiff.updateMask(NDVIdiff.gt(meanu.add(stdevu.multiply(2))))

# Calculate change direction
cdir = NDVIdiff.atan2(NDWIdiff)

# Calculate change Vector by masking change direction with the threshold
cvect = cdir.updateMask(cmag_thresh)

# Export Maps
composite_before = ee.Image(dataset1.median().clip(loc))
composite_after = ee.Image(dataset2.median().clip(loc))
#Export.image.toDrive({image: cvect, folder: 'Lab7', description: 'CVA_', scale: 30, region: loc})
#Export.image.toDrive({image: uid_thresh, folder: 'Lab7', description: 'UID_', scale: 30, region: loc})
#Export.image.toDrive({image: composite_before, folder: 'Lab7', description: 'Before_', scale: 30, region: loc})
#Export.image.toDrive({image: composite_after, folder: 'Lab7', description: 'After_', scale: 30, region: loc})

# Add to map
Map.addLayer(composite_after, visParams8, "After")
Map.addLayer(composite_before, visParams7, "Before")
Map.addLayer(geometries, {'opacity': 0.05})
Map.addLayer(uid_thresh.clip(loc), ndvi_params, 'NDVI Difference')
Map.addLayer(cvect.clip(loc), cvect_params, 'CVA')
