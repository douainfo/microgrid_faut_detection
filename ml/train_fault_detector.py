from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from config import *

client=MongoClient(MONGO_URI)
df=pd.DataFrame(list(client[MONGO_DB_NAME][MONGO_COLLECTION_NAME].find({})))

df=df.dropna(subset=["voltage","current","power","frequency","soc_battery","label"])
X=df[["voltage","current","power","frequency","soc_battery"]]
y=df["label"].astype(int)

Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

model=RandomForestClassifier(n_estimators=200,class_weight="balanced")
model.fit(Xtr,ytr)

joblib.dump(model,MODEL_PATH)
print("Model saved.")
