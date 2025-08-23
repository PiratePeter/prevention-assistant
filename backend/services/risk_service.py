import os

import geopandas as gpd
import requests
from flask import jsonify
from shapely.geometry import Point

from services.questionnaire_service import gen_questionaire_logic

WEBGIS_URL_BASE = os.getenv("WEBGIS_URL")
DANGER_LEVEL_MAP = {-1: "Keine Gefährdung bekannt", 1: "Restgefährdung", 2:"geringe Gefährdung", 3: "mittlere Gefährdung", 4: "erhebliche Gefährdung"}	

gdf = gpd.read_parquet("data/natgefka_sygefgeb.parquet")
if gdf.geometry.name != "geometry":
    gdf = gdf.set_geometry("geometry")

def get_risk_evaluation_logic(request):
    #TODO: get from request
    x=2631274.50
    y=1218223.25
    previous_claims_description=""


    max_gefstu = check_max_gefstu(x, y)

    gis_data = fetch_gis_data(x,y)
    attributes = gis_data["features"][0]["attributes"] # TODO: Catch "list index out of range"

    risks = {
        "HOCHWASSER": DANGER_LEVEL_MAP[max_gefstu],
        "HAGEL": attributes["HAGEL_TEXT"],
        "STURM": attributes["STURM_TEXT"],
    }
    questions = gen_questionaire_logic(risks, previous_claims_description)

    return jsonify(questions)


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
