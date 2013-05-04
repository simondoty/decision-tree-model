# Simon Doty (dotysn)
# Predicting Urbanization in the Austin Area Using Spatial Data Mining
# CS 378 -- Data Mining, Prof Ravikumar

# This script finds the nearest locations of various
# points of interest to each cell (record in the dataset).


import arcpy
from arcpy import env

# Set workspace environment
working_dir = "C:/Users/simon/Desktop/PROJECT/"
env.workspace = working_dir
in_features = "C:/Users/simon/Desktop/PROJECT/study_area/grid_500ft_UND_2006.shp"


#create tuple store of table {source directory, output table name} for each near feature
#run near on each and output the table

geographic_features = list()

# TxDOT Roads
geographic_features.append( (working_dir + "txdot/txdot_buff.shp", "txdot_roads") ) 

# Facilities:
# Cultural
geographic_features.append( (working_dir + "facilities/Cultural/Cultural.shp", "cultural") )
# Entertainment
geographic_features.append( (working_dir + "facilities/Entertainment/Entertainment.shp", "entertainment") )
# Health
geographic_features.append( (working_dir + "facilities/Health/health_facilities.shp", "health") )
# Recreation
geographic_features.append( (working_dir + "facilities/Rec/Rec.shp", "rec") )

# Cities:
# Austin (by itself centered on capital)
geographic_features.append( (working_dir + "cities/Austin.shp", "austin") )
# Surrounding Cities and Towns
geographic_features.append( (working_dir + "cities/Surrounding_Cities.shp", "surrounding_cities") )


# Education:
# Schools
geographic_features.append( (working_dir + "Schools2012/Schools2012.shp", "schools") )
# Colleges
geographic_features.append( (working_dir + "facilities/Colleges/Colleges.shp", "colleges") )



if arcpy.Exists(in_features):
    for feature in geographic_features:
    	print "running near calculation on dataset..." + feature[0]
    	arcpy.GenerateNearTable_analysis(in_features, feature[0], feature[1])
    	print "done with feature"

print "done with all features"
