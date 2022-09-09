
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
data = pd.read_csv("list_saham.csv")

@app.route("/")
def index():
    # ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
    #             "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]

    return """
    choose one sector from this list
    ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
    "Industrials", "Infrastructures", "Properties and Real Estate", "Technology", "Transportation & Logistic"]
    or 'All Sector' if you want to get all sectors
    """

@app.route("/api", methods=["GET"])
def api():
    sector = request.args.get("sector")
    all_sector =     ["Basic Materials", "Consumer Cyclicals", "Consumer Non-Cyclicals", "Energy", "Financials", "Healthcare",
    "Industrials", "Infrastructures", "Properties & Real Estate", "Technology", "Transportation & Logistic"]
    
    sector = sector.upper().replace("AND", "&")
    if sector.upper() == "ALL SECTOR":
        output_code = []
        output_company = []
        output_sector = []
        for _ in all_sector:
            loc_data = data.loc[data["sektor"].str.upper() == _.upper()]
            kode_x = loc_data["kode"]
            company_x = loc_data["nama perusahaan"]
            sector_x = loc_data["sektor"]

            for i in kode_x.index:
                output_code.append(kode_x[i])
                output_company.append(company_x[i])
                output_sector.append(sector_x[i])
            # temp = [kode_x[i] for i in kode_x.index]
            # output_code.extend(temp)
    else:
        loc_data = data.loc[data["sektor"].str.upper() == sector.upper()]
        kode_x = loc_data["kode"]
        company_x = loc_data["nama perusahaan"]
        sector_x = loc_data["sektor"]

        output_code = [kode_x[i] for i in kode_x.index]
        output_company = [company_x[i] for i in company_x.index]
        output_sector = [sector_x[i] for i in sector_x.index]

    if len(loc_data) > 0:
        response = jsonify(
            message = "done",
            code = output_code,
            company = output_company,
            sector = output_sector
        )
    else:
        response = jsonify(
            message = "failed",
            code = "not found",
            company = "not found",
            sector = "not found"
        )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(threaded=True)
