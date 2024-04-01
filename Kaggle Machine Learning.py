## Basic data exlporation
import pandas as pd
import shutil
shutil.unpack_archive("/Users/Chunyi/Documents/Python/pythonProject/melb_data.csv.zip")
melbourne_file_path = '/Users/Chunyi/Documents/Python/pythonProject/melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path)
melbourne_data.describe()
newesthomeage = 6
melbourne_data.columns

## First machine learning model
# dropna drops missing values (think of na as "not available")
melbourne_data = melbourne_data.dropna(axis=0)
y = melbourne_data.Price
melbourne_features = ['Rooms', 'Bathroom','Landsize', 'Lattitude', 'Longtitude']
X = melbourne_data[melbourne_features]
X.describe()
X.head()

from sklearn.tree import DecisionTreeRegressor

# Define model. Specify a number for random_state to ensure same results each run
melbourne_model = DecisionTreeRegressor(random_state=1)

# Fit Model
melbourne_model.fit(X,y)

print("Making prediction for the following 5 houses:")
print(X.head())
print("The predictions are")
print(melbourne_model.predict(X.head()))

## Validation data
# Validating model results by mean absolutle error

from sklearn.metrics import mean_absolute_error
predicted_home_prices = melbourne_model.predict(X)
mean_absolute_error(y,predicted_home_prices)

# Above is not accuarte so we need to split some data out for test and see below
# Split data into training and validation data, for both features and target
from sklearn.model_selection import train_test_split

# The split is based on a random number generator. Supplying a numeric value to
# the random_state argument guarantees we get the same split every time we
# this script

train_X, val_X, train_y, val_y = train_test_split(X,y, random_state=0)

# Define model
melbourne_model =DecisionTreeRegressor()

# Fit model
melbourne_model.fit(train_X, train_y)

# Get predicted prices on validation data
val_predictions = melbourne_model.predict(val_X)
print(mean_absolute_error(val_y,val_predictions))

## Underfitting and Overfitting
# Utility function to help compare MAE scores from different values
# for max_leaf_nodes

from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X,train_y)
    pres_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, pres_val)
    return (mae)

# Use for loop to compare accuracy of model with with different values
# for max_leaf_nodes
# Compare MAE with differing values of max_leaf_nodes

for max_leaf_nodes in [5,50,500,5000]:
    my_mae = get_mae (max_leaf_nodes,train_X,val_X,train_y,val_y)
    print("Max leaf nodes: %d \t\t Mean Absolute Error %d" %(max_leaf_nodes, my_mae))

# dict comprehension way to ge the best nodes

scores = {leaf_size: get_mae(leaf_size, train_X, val_X, train_y, val_y)
           for leaf_size in [5,50,500,5000] }
best_tree_size = min(scores, key = scores.get)

## Random Froests
# Build Random Forest model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
forest_model = RandomForestRegressor(random_state=1)
forest_model.fit(train_X,train_y)
melb_preds = forest_model.predict(val_X)
print(mean_absolute_error(val_y,melb_preds))

