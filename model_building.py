import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import statsmodels.api as sm
import pickle

# Read data
df = pd.read_csv('eda_data.csv')

# Choose relevant columns 
df_model = df[['avg_salary','Rating','Size','Type of ownership','Industry','Sector','Revenue','num_comp',
               'hourly','employer_provided','job_state','same_state','age','python_yn','spark','aws',
               'excel','job_simp','seniority','desc_len']]


# Feature engineering
df_model['large_company'] = (df_model['Size'].apply(lambda x: x.replace('+','').replace(' employees','').replace(',','')).astype(float) > 5000).astype(int)
df_model['revenue_per_emp'] = df_model['Revenue']/df_model['num_comp']
df_model['python_aws'] = df_model['python_yn']*df_model['aws']
df_model['python_excel'] = df_model['python_yn']*df_model['excel']
df_model['seniority_num'] = df_model['seniority'].map({'junior':0,'senior':1,'lead':2,'manager':3,'director':4,'not specified':5})

# Get dummy data 
df_dum = pd.get_dummies(df_model)

# Split data
X = df_dum.drop('avg_salary', axis =1)
y = df_dum.avg_salary.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Multiple linear regression 
X_sm = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

lm = LinearRegression()
lm.fit(X_train, y_train)

# Cross validation score
np.mean(cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))

# Lasso regression
lm_l = Lasso(alpha=.13)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))

# Lasso regression alpha tuning
alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3)))
    
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]

# Random forest 
rf = RandomForestRegressor()
np.mean(cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error', cv= 3))

# Tune models GridsearchCV 
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}
gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

# Test ensembles 
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)

# Save model
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

# Load model
file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0]
