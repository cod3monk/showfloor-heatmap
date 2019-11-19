# showfloor-heatmap
SC17 showfloor heatmap

Reads data from a Cisco Prime and turns it into a heatmap of clients associations. Needs manual input for AP locations. It also supports live bandwidth heatmaps, which update in realtime with [sFlow-RT](http://sflow-rt.com/).

## Example

See the following youtube video: https://www.youtube.com/watch?v=yYeZzxcRPpk


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
7. Add `?show_aps` to URL to also show AP placement on showfloor.

If you need to add any ap locations later. `imagesviewer.py` supports searching for individual ap names (Command-F), but the resulting file needs to be merged manually.

## Live sFlow-RT version

1. Create an sFlow-RT app, as described [here](http://sflow-rt.com/writing_applications.php) with the following script:
```javascript
controller = "140.221.244.2"; // needs to be changed

setFlow('sc17-wifi',
{
  keys: "if:ipsource:"+controller+":ipdestination:ipsource",
  value:'bytes',
  filter:"(ipsource="+controller+" & udpsourceport=5247) | (ipdestination="+controller+" & udpdestinationport=5247)",
  t: 10
});
```
2. Update the sFlow-RT URL in the `index_traffic.html` file, to point to your app.
3. Open up `website/index_traffic.html`, which will update every 200ms.
4. To change interval use `?interval=1000` (for 1 second updates).

## TODOs

* Center map (currently it is aligned left)

## Authors

* Julian Hammer
* Neil McKee (sFlow-RT integration)

## Licencse
GNU Affero General Public License Version 3.0
