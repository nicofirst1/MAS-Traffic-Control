This directory contains imported network and scenarios.
As well as [map_utils](FlowMas/maps/maps_utils.py) a set of scripts to handle maps related processes.
## Importing OSM 
To import a custom map from [OpenStreetMap](https://www.openstreetmap.org/) you will need to install the sumo binaries and use the [webWizard](http://sumo.sourceforge.net/userdoc/Tutorials/OSMWebWizard.html) to download the necessary files.

### Using OSM with NetParams
If you just want to use the map you can set the _osm_path_ parameter of _flow.core.params.NetParams_  pointing to the _osm_bbox.osm.xml_ file.

### Using OSM with inflow
If you wish to use the _get_edges_ function in [map_utils](FlowMas/maps/maps_utils.py) to add inflows to an imported OSM map you need to follow these instructions.

Having your directory **map_dir** with all the _xml_ files you need to run the following commands:
- `cd map_dir`
- locate the  _osm_bbox.osm.xml_ file.
- `netconvert --osm-files osm_bbox.osm.xml  --output-file yourMapName.net.xml --keep-edges.by-vclass passenger --remove-edges.isolated`

This will generate the file __yourMapName.net.xml__ which needs to be fed to the _get_edges_ function in [map_utils](FlowMas/maps/maps_utils.py).

