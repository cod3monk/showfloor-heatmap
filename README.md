# showfloor-heatmap
SC16 showfloor heatmap

Reads data from a Cisco Prime and turns it into a heatmap. Needs manual input for AP locations

## How to run

1. Clone this repo
2. Create a config.ini (based on config.ini.EXAMPLE)
3. Get current ap_list.json from a Prime: `./queryprime.py > website/ap_list.json`
4. Get a floormap image (in SVG and PNG) and save it to `website/floormap.*`
5. Use `./imageviewer.py` to create `website/ap_loc.json` file
   1. Load File... (`website/floorplan.png`)
   2. Load AP List.. (`website/ap_list.json`)
   3. See terminal for AP name and click on location (Zoom with CMD++ and CMD+-)
   4. Skip APs with CMD+n and go back to last AP with CMD+b
   5. Save AP Locations to `website/ap_loc.json`
6. Point browser to `website/index.html` (e.g., with `./runserver.py` in `website`)

## TODOs

* Resizing the browser window
* Automatic reload json
* Support Multiple floors
* Center map