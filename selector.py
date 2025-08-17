#! /usr/bin/env python3
import yaml
import mgrs
import folium
import webbrowser

def main():
    # 1. Load YAML file
    yaml_file = "grid.yaml"
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    x_res = data.pop("x_resolution")
    y_res = data.pop("y_resolution")

    # 2. Convert MGRS to Latitude/Longitude
    m = mgrs.MGRS()
    grid_id = "54SUE"  # TODO:

    def mgrs_to_latlon(mgrs_code):
        lat, lon = m.toLatLon(mgrs_code)
        return lat, lon

    # 3. Create Folium map
    mymap = folium.Map(location=[35.0, 135.0], zoom_start=12, tiles="OpenStreetMap")

    for fname, (x, y) in data.items():
        # Determine the range of this cell
        x1, y1 = x, y
        x2, y2 = x + x_res, y + y_res

        # Convert to MGRS code
        c1 = f"{grid_id}{x1:05d}{y1:05d}"
        c2 = f"{grid_id}{x2:05d}{y1:05d}"
        c3 = f"{grid_id}{x2:05d}{y2:05d}"
        c4 = f"{grid_id}{x1:05d}{y2:05d}"

        # Convert to latitude and longitude
        latlon = [mgrs_to_latlon(c) for c in [c1, c2, c3, c4]]

        # Convert to GeoJSON format
        geojson = {
            "type": "Feature",
            "properties": {"name": fname},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[ [lon, lat] for lat, lon in latlon ]]
            },
        }

    # ---------- 4. Add as GeoJson (color can be toggled by clicking) ----------
        gj = folium.GeoJson(
            geojson,
            style_function=lambda feature: {
                "color": "blue",
                "weight": 2,
                "fillColor": "blue",
                "fillOpacity": 0.3,
            },
            highlight_function=lambda feature: {
                "fillColor": "red",
                "fillOpacity": 0.6,
            },
            tooltip=folium.Tooltip(fname),  # ← Display PCD name on hover
        )
        gj.add_to(mymap)

    # ---------- Output ----------
    html_file_path="/tmp/map.html"

    mymap.save(html_file_path)
    webbrowser.open(html_file_path)


if __name__ == "__main__":
    main()