#! /usr/bin/env python3
import yaml
from mgrs import MGRS
import json
import webbrowser
import argparse


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="PCD Grid Selector")
    parser.add_argument("input", default="pointcloud_metadata.yaml", help="Input YAML file")
    parser.add_argument("--grid", default="54SUE", help="MGRS grid code")
    args = parser.parse_args()

    # Print projection type and grid code
    grid_code = args.grid
    print("Projection Type: ", "MGRS")
    print("Grid Code: ", grid_code)

    # YAML読み込み
    with open(args.input, "r") as f:
        data = yaml.safe_load(f)

    # load resolution: the default is 100
    x_res = data.get("x_resolution", 100)
    y_res = data.get("y_resolution", 100)

    m = MGRS()
    grids = []

    # PCD領域を緯度経度に変換
    for fname, coords in data.items():
        if fname in ["x_resolution", "y_resolution"]:
            continue
        x, y = coords

        mgrs_lb = f"{grid_code}{x:03d}{y:03d}"
        mgrs_rt = f"{grid_code}{x+x_res:03d}{y+y_res:03d}"
        lat_lb, lon_lb = m.toLatLon(mgrs_lb.encode())
        lat_rt, lon_rt = m.toLatLon(mgrs_rt.encode())
        grids.append({"fname": fname, "lb": [lat_lb, lon_lb], "rt": [lat_rt, lon_rt]})

    html_file = "/tmp/pcd_grid_map.html"

    # Leaflet HTMLテンプレート（Leaflet.pm + Turf.js対応）
    html_template = f"""
      <!DOCTYPE html>
      <html>
      <head>
        <title>PCD Grid Selector</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
        <link rel="stylesheet" href="https://unpkg.com/leaflet.pm/dist/leaflet.pm.css" />
        <style>
          #map {{ width: 100%; height: 90vh; }}
          #copyBtn {{ width: 100%; height: 10vh; font-size: 16px; }}
        </style>
      </head>
      <body>
      <div id="map"></div>
      <button id="copyBtn">Copy Selected Grid Names</button>

      <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
      <script src="https://unpkg.com/leaflet.pm/dist/leaflet.pm.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/@turf/turf/turf.min.js"></script>
      <script>
        const grids = {json.dumps(grids, indent=2)};
        const selectedGrids = new Set();

        const map = L.map('map').setView([grids[0].lb[0], grids[0].lb[1]], 15);

        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors'
        }}).addTo(map);

        // PCD矩形描画
        grids.forEach(grid => {{
          const bounds = [[grid.lb[0], grid.lb[1]], [grid.rt[0], grid.rt[1]]];
          const rect = L.rectangle(bounds, {{color: "blue", weight: 1, fillOpacity: 0.3}}).addTo(map);
          grid.rect = rect;  // 後で投げ縄選択時に参照

          // クリックで選択切り替え
          rect.on('click', () => {{
            const current = rect.options.fillColor;
            const newColor = current === "red" ? "blue" : "red";
            rect.setStyle({{fillColor: newColor}});
            if(newColor === "red") selectedGrids.add(grid.fname);
            else selectedGrids.delete(grid.fname);
          }});

          // マウスオーバーでファイル名表示
          rect.on('mouseover', (e) => {{
            rect.bindTooltip(grid.fname, {{permanent: false, direction: "top"}}).openTooltip();
          }});
          rect.on('mouseout', (e) => {{
            rect.closeTooltip();
          }});
        }});

        // Leaflet.pmで投げ縄選択
        map.pm.addControls({{
          position: 'topleft',
          drawPolygon: true,
          editMode: false,
          removalMode: false,
          drawMarker: false,
          drawPolyline: false,
          drawCircle: false,
          drawCircleMarker: false,
          drawRectangle: false
        }});

        map.on('pm:create', e => {{
          if(e.shape === 'Polygon') {{
            const poly = e.layer.toGeoJSON();
            grids.forEach(grid => {{
              const bounds = [[grid.lb[0], grid.lb[1]], [grid.rt[0], grid.rt[1]]];
              const rectPoly = turf.polygon([[
                [bounds[0][1], bounds[0][0]],
                [bounds[1][1], bounds[0][0]],
                [bounds[1][1], bounds[1][0]],
                [bounds[0][1], bounds[1][0]],
                [bounds[0][1], bounds[0][0]]
              ]]);
              if(turf.booleanIntersects(poly, rectPoly)) {{
                selectedGrids.add(grid.fname);
                grid.rect.setStyle({{fillColor: 'red'}});
              }}
            }});
            e.layer.remove(); // 投げ縄ポリゴンを消す
          }}
        }});

        // ボタンクリックで clipboard にコピー
        document.getElementById('copyBtn').addEventListener('click', () => {{
          const text = Array.from(selectedGrids).join(" ");
          navigator.clipboard.writeText(text).then(() => {{
            alert("Copied:\\n" + text);
          }});
        }});
      </script>
      </body>
      </html>
      """

    # Dump HTML file
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    webbrowser.open(html_file)


if __name__ == "__main__":
    main()
