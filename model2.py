# import Flask and jsonify
from flask import Flask, jsonify, request
# import Resource, Api and reqparser
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy
import pickle

app = Flask(__name__)
api = Api(app)

class preprocess:

    def __init__(self):
        # Your __init__ function takes in arguments as input
        # and does some initialization, such as creating model parameters.
        print('init() called')
        pass

    def fit(self, X, y = None):
        # Your forward() function takes in an X (and optionally a y)
        # and fits its parameters to the data. It then returns "self".
        # This transformer does not fit anything, because it is parameterless.
        print('fit() called')
        return self

    def transform(self, df, y = None):
             
       # creating instance of labelencoder
        labelencoder = LabelEncoder()
        # Assigning numerical values and storing in another column
        df.Gender = labelencoder.fit_transform(df.Gender)
        df.Married = labelencoder.fit_transform(df.Married)
        df.Dependents = labelencoder.fit_transform(df.Dependents)
        df.Education = labelencoder.fit_transform(df.Education)
        df.Self_Employed = labelencoder.fit_transform(df.Self_Employed)
        df.Property_Area = labelencoder.fit_transform(df.Property_Area)
        #df.Loan_Status = labelencoder.fit_transform(df.Loan_Status)
        print('transform() called')
        return df

model = pickle.load( open( "model.p", "rb" ) )

class Approval(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        
        # getting predictions from our model.
        # it is much simpler because we used pipelines during development
        res = pipeline.predict(df)
        # we cannot send numpt array as a result
        return res.tolist() 

# assign endpoint
api.add_resource(Approval, '/approval')

if __name__ == '__main__':
    app.run(debug=True)