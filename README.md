# About

This repo is intended to be a set of useful scripts for working with Google's [Open Buildings](https://sites.research.google/open-buildings/)
dataset, specifically to help translate it into [Cloud Native Geospatial](https://cloudnativegeo.org) formats. The outputs will live
at https://beta.source.coop/cholmes/google-open-buildings so most people can just make use of those directly. But these are intended to
show the process, and then they've expanded to be a way to benchmark performance.

This is basically my first Python project, and certainly my first open source one. It is only possible due to ChatGPT, as I'm not a python
programmer, and not a great programmer in general (coded professionally for about 2 years, then shifted to doing lots of other stuff). So
it's likely not great code, but it's been fun to iterate on it and seems like it might be useful to others. 

# Functionality

So far there is just one 'tool', a CLI built with click that performs two functions:

* `convert` takes as input either a single CSV file or a directory of CSV files, downloaded locally from the Google Buildings dataset.
* `benchmark` runs the convert command in a number of different ways and reports the time.

# Roadmap

The next script to write is to add country and admin level 1 attributes from GeoBoundaries. This was the trickiest step in processing v2 buildings.
This will be an interesting to benchmark, with the options being more like DuckDB and PostGIS (pandas could try but may not work on the biggest ones), and potentially even big query.

# Ideas

I'll try to turn these into tickets, but just wanted to jot down some ways I've thought about evolving the script.

* Make GPQ a flag to pass in, not hardcoded.
* Make parquet compression options a flag to pass in (and raise appropriate errors about which one can be used.
* Add the splitting of multipolygons to the ogr process. This may need to make use of Fiona, but that may lose the speed of the [column-oriented API](https://gdal.org/development/rfc/rfc86_column_oriented_api.html) - so may be interesting to have both options to benchmark.
* Include ability to get the source CSV's directly from the cloud, unzip them and process them.
