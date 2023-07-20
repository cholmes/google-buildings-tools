# About

This repo is intended to be a set of useful scripts for working with Google's [Open Buildings](https://sites.research.google/open-buildings/)
dataset, specifically to help translate it into [Cloud Native Geospatial](https://cloudnativegeo.org) formats. The outputs will live
at https://beta.source.coop/cholmes/google-open-buildings so most people can just make use of those directly. But these are intended to
show the process, and then they've expanded to be a way to benchmark performance.

This is basically my first Python project, and certainly my first open source one. It is only possible due to ChatGPT, as I'm not a python
programmer, and not a great programmer in general (coded professionally for about 2 years, then shifted to doing lots of other stuff). So
it's likely not great code, but it's been fun to iterate on it and seems like it might be useful to others. 

## Installation

Since this is my first python project I've yet to figure out how to make it easy to get all the dependencies, so for now look at them and pip install ;) I promise I'll consult chatgpt on this soon, or PR's and suggestions welcome. Hopefully I'll get it so there's a CLI tool that gets added to your path. Right now you have to run the program with a call like `python google-buildings-cli.py benchmark original-csv/36b_buildings.csv test-output --format parquet`

# Functionality

So far there is just one 'tool', a CLI built with click that performs two functions:

* `convert` takes as input either a single CSV file or a directory of CSV files, downloaded locally from the Google Buildings dataset. It can write out as GeoParquet, FlatGeobuf, GeoPackage and Shapefile, and can process the data using DuckDB, GeoPandas or OGR. 
* `benchmark` runs the convert command against one or more different formats, and one or more different processes, and reports out how long each took.

A sample output for `benchmark`, run on 36b_buildings.csv, a 130 mb CSV file is:

╒═══════════╤════════════════╤════════════════╤════════════════╤════════════════╕
│ process   │ fgb            │ gpkg           │ parquet        │ shp            │
╞═══════════╪════════════════╪════════════════╪════════════════╪════════════════╡
│ duckdb    │ 0:00:04.287083 │ 0:01:52.222495 │ 0:00:02.880891 │ 0:00:05.404221 │
├───────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ ogr       │ 0:00:03.620750 │ 0:00:08.528865 │ 0:00:02.319576 │ 0:00:03.609031 │
├───────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ pandas    │ 0:00:35.763740 │ 0:00:47.535597 │ 0:00:04.880124 │ 0:00:37.751942 │
╘═══════════╧════════════════╧════════════════╧════════════════╧════════════════╛

## Format Notes

I'm mostly focused on GeoParquet and FlatGeobuf, as good cloud-native geo formats. I included GeoPackage and Shapefile mostly for benchmarking purposes. GeoPackage I think is a good option for Esri and other more legacy software that is slow to adopt new formats. Shapefile is total crap for this use case - it fails on files bigger than 4 gigabytes, and lots of the source S2 Google Building CSV's are bigger, so it's not useful for translating. The truncation of field names is also annoying, since the CSV file didn't try to make short names (nor should it, the limit is silly).

GeoPackage is particularly slow with DuckDB, it's likely got a bit of a bug in it. But it works well with Pandas and OGR. 

## Process Notes

When I was processing V2 of the Google Building's dataset I did most of the initial work with GeoPandas, which was awesome, and has the best GeoParquet implementation. But the size of the data made its all in memory processing untenable. I ended up using PostGIS a decent but, but near the end of that process I discovered DuckDB, and was blown away by it's speed and ability to manage memory well. So for this tool I was mostly focused on those two.

Note that GeoParquet from DuckDB by default runs [gpq](https://github.com/planetlabs/gpq) on the DuckDB Parquet output, which adds a good chunk of processing time. This makes it so the DuckDB processing output is slower than it would be if DuckDB natively wrote GeoParquet metadata, which I believe is on their roadmap. So that will likely emerge as the fastest benchmark time. In the code you can set RUN_GPQ_CONVERSION to false if you want to get a sense of it. In the above benchmark running the Parquet with DuckDB without GPQ conversion at the end resulted in a time of 0:00:01.845316

Note also that currently DuckDB fgb, gpkg and shp output don't include projection information, so if you want to use the output then you'd need to run ogr2ogr on the output. It sounds like that may get fixed pretty soon, so I'm not going to add a step that includes the ogr conversion.

OGR was added later, and as of yet does not yet do the key step of splitting multi-polygons, since it's just using ogr2ogr as a sub-process and I've yet to find a way to do that from the CLI (though knowing GDAL/OGR there probably is one - please let me know). To run the benchmark with it you need to do --skip-split-multis or else the times on it will be 0 (except for Shapefile, since it doesn't differentiate between multipolygons and regular polygons). I hope to add that functionality and get it on par, which may mean using Fiona. But it seems like that may affect performance, since Fiona doesn't use the [GDAL/OGR column-oriented API](https://gdal.org/development/rfc/rfc86_column_oriented_api.html).

# Roadmap

The next tool to write is to add country and admin level 1 attributes from GeoBoundaries. This was the trickiest step in processing v2 buildings.
This will be an interesting to benchmark, with the options being more like DuckDB and PostGIS (pandas could try but may not work on the biggest ones), and potentially even big query. The next functionality to add after that will be do spatial partitioning, and perhaps after that add Iceberg and Delta Lake and compare those two (I didn't get to that step with the v2 buildings). And perhaps I'll also add a tool to easily grab any data from the partitioned geoparquet on source.coop and get it in the format you want.

# Ideas

I'll try to turn these into tickets, but just wanted to jot down some ways I've thought about evolving the script.

* Make GPQ a flag to pass in, not hardcoded.
* Make parquet compression options a flag to pass in (and raise appropriate errors about which one can be used.
* Add the splitting of multipolygons to the ogr process. This may need to make use of Fiona, but that may lose the speed of the [column-oriented API](https://gdal.org/development/rfc/rfc86_column_oriented_api.html) - so may be interesting to have both options to benchmark.
* Include ability to get the source CSV's directly from the cloud, unzip them and process them.
* Print out the file sizes of the resulting formats in the benchmark.
