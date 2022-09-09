
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
data = pd.read_csv("../list_saham.csv")

@app.route("/")
def index():
    # ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
    #             "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]

    return """
    choose one sector from this list
    ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
    "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]
    or 'All Sector' if you want to get all sectors
    """

@app.route("/api", methods=["GET"])
def api():
    sector = request.args.get("sector")
    all_sector =     ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
    "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]
    
    sector = sector.upper().replace("AND", "&")

    if sector.upper() == "ALL SECTOR":
        output = []
        for _ in all_sector:
            kode = data.loc[data["sektor"].str.upper() == _.upper()]["kode"]
            temp = [kode[i] for i in kode.index]
            output.extend(temp)
    else:
        kode = data.loc[data["sektor"].str.upper() == sector.upper()]["kode"]
        output = [kode[i] for i in kode.index]
    if len(kode) > 0:
        response = jsonify(
            message = "done",
            code = output
        )
    else:
        response = jsonify(
            message = "failed",
            code = "not found"
        )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(threaded=True)