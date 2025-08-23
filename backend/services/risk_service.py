import os

import requests
from flask import jsonify

WEBGIS_URL_BASE = os.getenv("WEBGIS_URL")

def get_risk_evaluation_logic(request):
    x=2622793.8220000006 #TODO: get from request
    y=1166321.5309999995 #TODO: get from request

    data = fetch_gis_data(x,y)
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
