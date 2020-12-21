from flask import Flask, render_template, request
import numpy as np
import pandas as pd
app = Flask(__name__)
import pickle

df = pd.read_excel('F:\\projects\\Machine Learning\\Car_price_prediction\\Data\\Cars_mumbai.xlsx')
dummies = pd.get_dummies(df.Steering)

df1 = pd.concat([df,dummies],axis = 'columns')
df2 = df1.drop(['Manual'],axis = 'columns')
dummies = pd.get_dummies(df.Fuel)
df3 = pd.concat([df2,dummies],axis = 'columns')
df4 = df3.drop(['Petrol'],axis = 'columns')
df5 = df4.drop(['Steering','Fuel'],axis = 'columns')
dummies = pd.get_dummies(df.Make)
df6 = pd.concat([df5,dummies],axis = 'columns')
df6 = df6.drop(['Volvo'],axis = 'columns')

X = df6.drop(['Make','Price','Location'],axis = 'columns')
Y = df6[['Price']]

with open ('cars_mumbai','rb') as f:
    model = pickle.load(f)
    
print(52)
def Predict_Price(Make,Distance,Owner,Automatic,Diesel):
    location = np.where(X.columns == Make)[0][0]
#     print(location)
    x = np.zeros(len(X.columns))
    x[0] = Distance
    x[1] = Owner
    x[2] = Automatic
    x[3] = Diesel
    if location > 0:
        x[location] = 1
    return abs(model.predict([x])[0][0])

@app.route('/',methods= ["GET","POST"])
def predictor():
    if request.method == "POST":
        print(53)
        my_dict = request.form
        print(my_dict)
        car  = my_dict['cars']
        km = int(my_dict['Kilometers'])
        owner = int(my_dict['owner'])
        transmission = int(my_dict['transmission'])
        fuel = int(my_dict['fuel'])
        car_price = Predict_Price(car,km,owner,transmission,fuel)
        # print(car_price)
        return render_template('results.html',brand = car, car_prediction = round(car_price))
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)