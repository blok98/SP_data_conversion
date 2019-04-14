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
    return jsonify(getPopularProducts(expiration_date='2017-12-20',limiet=8))


@app.route('/personalproducts', methods=['POST'])
def personalproducts():
    sessiondata = request.json
    print(sessiondata)
    return jsonify(getPersonalProducts(sessiondata,limiet=8))


if __name__ == '__main__':
    app.run()
