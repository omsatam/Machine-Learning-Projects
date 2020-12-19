from flask import Flask, render_template, request
app = Flask(__name__)
import pickle

with open ('corona_model_updated','rb') as f:
    model = pickle.load(f)
print(52)
@app.route('/',methods= ["GET","POST"])
def predictor():
    if request.method == "POST":
        print(53)
        my_dict = request.form
        name = my_dict['Name']
        fever = int(my_dict['fever'])
        age = int(my_dict['age'])
        breathing = int(my_dict['breathing'])
        bodypain = int(my_dict['bodypain'])
        tired = int(my_dict['tired'])
        features = [[fever,age,tired,breathing,bodypain]]
        infection_prob = model.predict_proba(features)[0][1]
        print(infection_prob)
        return render_template('show_proba.html',Name = name ,infection = round(infection_prob*100))
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)