from flask import Flask, render_template

app = Flask(__name__)

@app.route("/for-loop")
def loop_for():
    equipos = [
        "REAL MADRID",
        "FC BARCELONA",
        "MILAN AC",
        "LIVERPOOL",
        "BAYER MUNICH",
        "AJAX AMSTERDAN",
        "INTER MILAN",
        "JUVENTUS",
        "MANCHESTER UNITED",
        "OPORTO"
    ]

    equipos_cham = {
        "REAL MADRID": 14,
        "FC BARCELONA": 5,
        "MILAN AC": 7,
        "LIVERPOOL": 6,
        "BAYER MUNICH": 5,
        "AJAX AMSTERDAN": 4,
        "INTER MILAN": 3,
        "MANCHESTER UNITED": 3      
    }

    return render_template(template_name_or_list="for_loop.html", teams = equipos,
                           teams_dic = equipos_cham)



if __name__ == "__main__":
    app.run()