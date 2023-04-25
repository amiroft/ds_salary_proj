from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error

# SVR model
svr = SVR(kernel='linear')
svr.fit(X_train, y_train)
svr_pred = svr.predict(X_test)
mae_svr = mean_absolute_error(y_test, svr_pred)
print('SVR MAE:', mae_svr)

# Gradient Boosting Regressor model
gbr = GradientBoostingRegressor()
gbr.fit(X_train, y_train)
gbr_pred = gbr.predict(X_test)
mae_gbr = mean_absolute_error(y_test, gbr_pred)
print('GBR MAE:', mae_gbr)

# K-Nearest Neighbors Regressor model
knn = KNeighborsRegressor()
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)
mae_knn = mean_absolute_error(y_test, knn_pred)
print('KNN MAE:', mae_knn)
