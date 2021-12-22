# Mapping-Mountainous-Arctic-Lakes-From-the-Air
This repository is part of a bigger project lead by Cristian Gudasz at Umeå University


![alt text](AwsomeLiDAR.png)

# Run the script by giving it paths to the data
python Y:/William/GitHub/Mapping-Mountainous-Arctic-Lakes-From-the-Air/Hydrological_processing.py D:/Abisko/Abisko_watersheds/National_2m_dem/ D:/temp/test_raided_speed/ --streaminitation=2500 --outlets=D:/Abisko/Abisko_watersheds/lake_outlets/outlets.shp --watershed_dir=D:/Abisko/Abisko_watersheds/watersheds/

This code is dependent on WhiteboxTools which was installed using pip install WhiteboxTools: https://www.whiteboxgeo.com/manual/wbt_book/preface.html
