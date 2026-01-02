from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS   # ← NEW
from config import *
from ml.model_utils import predict_fault

app = Flask(__name__)
CORS(app)   # ← NEW

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route("/api/latest_with_prediction")
def latest_with_prediction():
    docs = list(collection.find().sort("datetime", -1).limit(50))
    docs = [serialize_doc(d) for d in docs]
    if not docs:
        return jsonify([])
    preds, probs = predict_fault(docs)
    for d, p, prob in zip(docs, preds, probs):
        d["predicted_fault"] = int(p)
        d["fault_probability"] = float(prob)
    return jsonify(docs)

if __name__ == "__main__":
    app.run(debug=True)
