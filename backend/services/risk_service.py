import os

import geopandas as gpd
import requests
from flask import jsonify
from pyproj import Transformer
from shapely.geometry import Point

from services.questionnaire_service import gen_questionaire_logic

WEBGIS_URL_BASE = os.getenv("WEBGIS_URL")
DANGER_LEVEL_MAP = {-1: "Keine Gefährdung bekannt", 1: "Restgefährdung", 2:"geringe Gefährdung", 3: "mittlere Gefährdung", 4: "erhebliche Gefährdung"}	

gdf = gpd.read_parquet("data/natgefka_sygefgeb.parquet")
if gdf.geometry.name != "geometry":
    gdf = gdf.set_geometry("geometry")

def get_risk_evaluation_logic(request):
    data = request.json
    # building_info = data.get('building_info') #TODO: add to llm api call
    previous_claims_description = data.get('damage_desc')
    lon = data.get('location').get('lon')
    lat = data.get('location').get('lat')

    transformer = Transformer.from_crs("epsg:4326", "epsg:2056", always_xy=True)
    x, y = transformer.transform(lon, lat)

    max_gefstu = check_max_gefstu(x, y)

    gis_data = fetch_gis_data(x,y)

    hail_risk = DANGER_LEVEL_MAP[-1]
    storm_risk = DANGER_LEVEL_MAP[-1]

    if 0 < len(gis_data["features"]):
        attributes = gis_data["features"][0]["attributes"]
        hail_risk = attributes["HAGEL_TEXT"]
        storm_risk = attributes["STURM_TEXT"]
    
    risks = {
        "HOCHWASSER": DANGER_LEVEL_MAP[max_gefstu],
        "HAGEL": hail_risk,
        "STURM": storm_risk,
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
