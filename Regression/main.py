import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

    
data = get_data()
inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

# TODO: calculate closed-form solution
theta_best = [0, 0]
X_train = np.c_[np.ones((len(x_train), 1)), x_train]
theta_best = np.linalg.inv(X_train.T.dot(X_train)).dot(X_train.T).dot(y_train)

# TODO: calculate error
X_test = np.c_[np.ones((len(x_test), 1)), x_test]
y_test_predicted = X_test.dot(theta_best)
mse_test = np.mean((y_test-y_test_predicted) ** 2)
print("MSE:", mse_test)
print("\n")

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# TODO: standardization
mean_x_train = np.mean(x_train)
std_x_train = np.std(x_train)
x_train = (x_train - mean_x_train) / std_x_train

mean_y_train = np.mean(y_train)
std_y_train = np.std(y_train)
y_train = (y_train - mean_y_train) / std_y_train

x_test = (x_test - mean_x_train) / std_x_train
y_test = (y_test - mean_y_train) / std_y_train

# TODO: calculate theta using Batch Gradient Descent
learning_rate = 0.1
iterations = 1000
m = len(x_train)
theta_v2 = [np.random.rand(), np.random.rand()]

X_train = np.c_[np.ones((len(x_train), 1)), x_train]
X_test = np.c_[np.ones((len(x_test), 1)), x_test]

for i in range(iterations):
    gradients = 2/m * (X_train.T @ (X_train@theta_v2 - y_train))
    theta_v2 = theta_v2 - learning_rate * gradients

    y_test_predicted = X_test.dot(theta_v2)
    mse_test = np.mean((y_test-y_test_predicted) ** 2)
    if i % 100 == 0 :
        print("MSE:", mse_test)


# TODO: calculate error
print("\nError:")

y_test_predicted = theta_v2[0] + x_test * theta_v2[1]
y_test_predicted = (y_test_predicted * y_test) + np.mean(y_test)

mse_test = np.mean((y_test-y_test_predicted) ** 2)
print(mse_test)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_v2[0]) + float(theta_v2[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()