from flask import Flask, send_from_directory, jsonify, redirect, request
from website.products import getPopularProducts, getPersonalProducts

app = Flask(__name__)

@app.route('/')
def home():

    return redirect("/index_SP2.html", code=302)


@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=False)

@app.route('/popularproducts')
def popularproducts():
    return jsonify(getPopularProducts(limiet=2))


@app.route('/personalproducts', methods=['POST'])
def personalproducts():
    sessiondata = request.json
    print(sessiondata)
    return jsonify(getPersonalProducts(sessiondata,limiet=3))


if __name__ == '__main__':
    app.run()
