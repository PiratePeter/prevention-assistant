import os

import geopandas as gpd
import requests
from flask import jsonify
from shapely.geometry import Point

WEBGIS_URL_BASE = os.getenv("WEBGIS_URL")

def get_risk_evaluation_logic(request):
    #TODO: get from request
    x=2630621.0 #2622793.8220000006
    y=1218404.0 #1166321.5309999995

    max_gefstu = check_max_gefstu(2630621.0, 1218404.0)
    data = {'max_gefstu': str(max_gefstu)}
    # data = fetch_gis_data(x,y)
    return jsonify(data)

def fetch_gis_data(x,y):
    params = {
        "geometry": f"{x},{y}",
        "geometryType": "esriGeometryPoint",
        "outFields": "OBERFLAECHENABFLUSS,HOCHWASSER_SEEN,HOCHWASSER_FLIESSGEWAESSER,HAGEL,STURM",
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
