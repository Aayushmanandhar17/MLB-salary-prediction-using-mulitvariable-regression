##IMPORT
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd ##pip install pandas in terminal
import numpy as np ##same as above for installation
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from flask import Flask, render_template, request, url_for


app=Flask(__name__)


org_data=pd.read_csv(r"baseball_data.csv")

data=org_data[['League','Salary','Wins']]
data['Wins']=(data['Wins']/162.5)*100


#arrange the data based on target and the actual data without target
target=np.log(data['Salary'])
main_data=data.drop(['Salary'],axis=1)

#running a multivariable regression model

multi_regr=LinearRegression().fit(main_data,target)
#Predicted salary for the main data
fitted_vals=multi_regr.predict(main_data)

#manually creating a data
#creating aemplty array
our_stat=np.ndarray(shape=(1,2))

##Putting the mean value in case we don't manually pass the value
our_stat=main_data.mean().values.reshape(1,2)

MSE=mean_squared_error(target,fitted_vals)
RMSE=np.sqrt(MSE)


##Creating a function to manually pass the value
##League=0=NL
##league=1=AL
def prediction(wins,league):
    if(wins<0 or wins>100):
        print("invalid wins")
        return
    our_stat[0][1]=wins
    if league=="AL":
        our_stat[0][0]=0
    else:
        our_stat[0][0]=1

    total_estimate=multi_regr.predict(our_stat)
    upperbound=total_estimate+RMSE
    lowerbound=total_estimate-RMSE
    print(our_stat)

    return total_estimate,upperbound,lowerbound





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form',methods=["POST"])
def form():
    Wins= request.form.get("wins",None)
    League=request.form.get("league")
    if League=="AL":
        name_league="American League"
    else:
        name_league="National League"


    if (int(Wins)<=0 ):
        Wins=0
    elif (int(Wins)>100):
        Wins=100

    avg_salary,maximum_avg,minimum_avg=prediction(int(Wins),league=League)
    text=f" You should spend ${round(float(np.e**avg_salary),2)} millions in salary to have a  {Wins} % winnings in {name_league} "
    bounds=f" Maximum Estimate= ${round(float(np.e**maximum_avg),2)} millions || Minimum estimate= ${round(float(np.e**minimum_avg),2)} millions "



    return render_template("index.html", Text=text, bound=bounds,Data=round(float(np.e**avg_salary),2))



if __name__ == '__main__':
    app.run()
