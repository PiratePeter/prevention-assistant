import os

import geopandas as gpd
import requests
from flask import jsonify
from shapely.geometry import Point

WEBGIS_URL_BASE = os.getenv("WEBGIS_URL")
DANGER_LEVEL_MAP = {-1: "Unbekannt", 1: "Restgefährdung", 2:"geringe Gefährdung", 3: "mittlere Gefährdung", 4: "erhebliche Gefährdung"}	

def get_risk_evaluation_logic(request):
    #TODO: get from request
    x=2631274.50
    y=1218223.25

    max_gefstu = check_max_gefstu(x, y)
    gis_data = fetch_gis_data(x,y)
    attributes = gis_data["features"][0]["attributes"] # TODO: Catch "list index out of range"
    data = {
        "DESCRIPTION": "Last time ...",
        "GEFAHREN": {
            "HOCHWASSER": DANGER_LEVEL_MAP[max_gefstu],
            "HAGEL": attributes["HAGEL_TEXT"],
            "STURM": attributes["STURM_TEXT"],
        }
    }
    return jsonify(data)


    """
    OBERFLAECHENABFLUSS
    OBERFLAECHENABFLUSS_TEXT_DE
    HOCHWASSER_SEEN
    SEEN_TEXT_DE
    HOCHWASSER_FLIESSGEWAESSER
    FLIESSGEWAESSER_TEXT_DE
    HAGEL
    HAGEL_TEXT
    STURM
    STURM_TEXT
    """
def fetch_gis_data(x,y):
    params = {
        "geometry": f"{x},{y}",
        "geometryType": "esriGeometryPoint",
        "outFields": "*",
        "returnGeometry": "false",
        "returnTrueCurves": "false",
        "f": "json"
    }
    try:
        resp = requests.get(WEBGIS_URL_BASE, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def check_max_gefstu(x_coord: float, y_coord: float, crs: str = "EPSG:2056"):
    gdf = gpd.read_parquet("data/natgefka_sygefgeb.parquet")
    if gdf.geometry.name != "geometry":
        gdf = gdf.set_geometry("geometry")
    point = gpd.GeoDataFrame(
        {"geometry": [Point(x_coord, y_coord)]},
        crs=crs
    )
    if gdf.crs != point.crs:
        point = point.to_crs(gdf.crs)
    overlaps = gpd.sjoin(gdf, point, predicate="intersects")
    if overlaps.empty:
        return -1
    else:
        return overlaps.iloc[0]["max_gefstu"]
