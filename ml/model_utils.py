import joblib, pandas as pd
from config import MODEL_PATH
_model=None

def load_model():
    global _model
    if _model is None:
        _model=joblib.load(MODEL_PATH)
    return _model

def predict_fault(records):
    model=load_model()
    df=pd.DataFrame(records)
    X=df[["voltage","current","power","frequency","soc_battery"]]
    preds=model.predict(X)
    probs=model.predict_proba(X)[:,1]
    return preds,probs
