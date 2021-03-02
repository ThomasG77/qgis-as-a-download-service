# QGIS as a download service

# Purpose

The idea is to be able to consume data from https://geoservices.ign.fr/documentation/diffusion/index.html using extent instead of downloading massive files for small areas. In the future, we would like to give a drawing or a shp file as an input to select download URLs.

For the moment, we only have a demo using raster from the French "Carte d'État Major" (1820-1866). As they are delivered by "tiles", we created a grid. You can from this grid, click on each "tile", download file and add it in one step. We use QGIS actions for this intend.

See the process in action in below demo

<img src="qgis-as-a-service-resized.gif"/>

## Want to download all? Don't abuse and take another road with below recipe

Be kind as we host the data on our own server. So if you want the full data, you should better use URLs from files `files_40k.txt` (all France) and `files_10k.txt` (only Paris and around called "Ile de France". Both files are list of files from section "Carte d'État Major" from https://geoservices.ign.fr/documentation/diffusion/index.html

In this case, something like `wget -c -i files_40k.txt` will do the job.

You may also use our script `download.sh` that do download, extract and do some other operations.

## Credits

Mainly based on idea from Klas Karlsson (see below) but to ease OpenData consumption for GIS users

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">2&#39;000 raster files to keep track on and load into <a href="https://twitter.com/hashtag/QGIS?src=hash&amp;ref_src=twsrc%5Etfw">#QGIS</a> easily on demand?<br><br>Use:<br>gdaltindex -write_absolute_path index.shp *.tif<br><br>Add some Python code to an Action for the layer, and click in the map to load the raster!<br><br>(I used -f GPKG and *.nc, but you get the point) <a href="https://t.co/vz9mSQHJvh">pic.twitter.com/vz9mSQHJvh</a></p>&mdash; Klas Karlsson (@klaskarlsson) <a href="https://twitter.com/klaskarlsson/status/1159514845127028738?ref_src=twsrc%5Etfw">August 8, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
