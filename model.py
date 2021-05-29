# import Flask and jsonify
from flask import Flask, jsonify, request
# import Resource, Api and reqparser
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy
import pickle
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, FunctionTransformer, StandardScaler


app = Flask(__name__)
api = Api(app)

class RawFeats:
    def __init__(self, feats):
        self.feats = feats

    def fit(self, X, y=None):
        pass


    def transform(self, X, y=None):
        return X[self.feats]

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

model = pickle.load( open( "model.p", "rb" ) )

class Approval(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        
        # creating instance of labelencoder
        labelencoder = LabelEncoder()
        # Assigning numerical values and storing in another column
        df.Gender = labelencoder.fit_transform(df.Gender)
        df.Married = labelencoder.fit_transform(df.Married)
        df.Dependents = labelencoder.fit_transform(df.Dependents)
        df.Education = labelencoder.fit_transform(df.Education)
        df.Self_Employed = labelencoder.fit_transform(df.Self_Employed)
        df.Property_Area = labelencoder.fit_transform(df.Property_Area)

        res = model.predict(df)
        # we cannot send numpt array as a result
        return res.tolist() 

# assign endpoint
api.add_resource(Approval, '/approval')

if __name__ == '__main__':
    app.run(debug=True)