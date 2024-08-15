# Soil Organic Carbon Prediction API

**Overview**

This API provides predictions for soil organic carbon (SOC) content and stock based on various environmental factors.

## Learn more

* [API](https://connect.doit.wisc.edu/soil_organic_carbon_prediction/)

**Endpoints**

* **POST /v1/prediction**
  * Predicts SOC content and stock based on input parameters.

**Input Parameters**

* depth_cm (float): Depth of the soil layer in centimeters.
* total_precipitation (float): Total annual precipitation in millimeters.
* min_temperature (float): Minimum annual temperature in degrees Celsius.
* mean_temperature (float): Mean annual temperature in degrees Celsius.
* max_temperature (float): Maximum annual temperature in degrees Celsius.
* dem (float): Digital Elevation Model value in meters.
* slope (float): Slope angle in degrees.
* aspect (float): Slope aspect in degrees (azimuth).
* hillshade (float): Hillshade index (0-255).
* bd_mean (float): Mean bulk density of the soil in grams per cubic centimeter (g/cm³).
* clay_mean (float): Mean clay content of the soil in percentage (%).
* om_mean (float): Mean organic matter content of the soil in percentage (%).
* ph_mean (float): Mean pH value of the soil.
* sand_mean (float): Mean sand content of the soil in percentage (%).
* silt_mean (float): Mean silt content of the soil in percentage (%).
* land_use (int): Land use code (refer to the land use classification system used).
* land_cover (int): Land cover code (refer to the land cover classification system used).

## LU and LC code mapings
```json
{
    '1':'Agriculture',
    '2':'Developed',
    '3':'Forest',
    '4':'Non-Forest Wetland',
    '5':'Other',
    '6':'Rangeland or Pasture',
    '7':'Non-Processing Area Mask'
}
```
```json
{
   '1':'Trees',
   '2':'Tall Shrubs & Trees Mix (SEAK Only)',
   '3':'Shrubs & Trees Mix',
   '4':'Grass/Forb/Herb & Trees Mix',
   '5':'Barren & Trees Mix',
   '6':'Tall Shrubs (SEAK Only)',
   '7':'Shrubs',
   '8':'Grass/Forb/Herb & Shrubs Mix',
   '9':'Barren & Shrubs Mix',
   '10':'Grass/Forb/Herb',
   '11':'Barren & Grass/Forb/Herb Mix',
   '12':'Barren or Impervious',
   '13':'Snow or Ice',
   '14':'Water',
   '15':'Non-Processing Area Mask'
}
```

**Output**

* soil_organic_carbon (float): Predicted SOC content
* soil_organic_carbon_stock (float): Predicted SOC stock

**Usage**

1. Install required dependencies.
2. Start the API server.
3. Send a POST request to the /v1/prediction endpoint with input parameters in JSON format.

**Example Request**
Check Code-Notebooks/example_api_call-2.ipynb to get an example of the API request.
