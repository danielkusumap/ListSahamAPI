
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
        output_company_name = []
        output_sector = []
        for _ in all_sector:
            data = data.loc[data["sektor"].str.upper() == _.upper()]
            kode = data["kode"]
            company = data["nama perusahaan"]
            sector = data["sector"]
##            temp = [kode[i] for i in kode.index]
            for i in kode.index:
                output_code.append(kode[i])
                output_company_name.append(company[i])
                output_sector.append(sector[i])
##            output_code.extend(temp)
    else:
        data = data.loc[data["sektor"].str.upper() == sector.upper()]
        kode = data["kode"]
        company = data["nama perusahaan"]
        sector = data["sector"]
        output_code = [kode[i] for i in kode.index]
        output_company_name = [company[i] for i in company.index]
        output_sector = [sector[i] for i in sector.index]
        
    if len(kode) > 0:
        response = jsonify(
            message = "done",
            code = output_code,
            company_name = output_company_name,
            sector = output_sector
        )
    else:
        response = jsonify(
            message = "failed",
            code = "not found",
            company_name = "not found",
            sector = "not found"
        )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(threaded=True)
