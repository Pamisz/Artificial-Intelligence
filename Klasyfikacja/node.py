import copy
import random
import numpy as np


class Node:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.feature_idx = None
        self.feature_value = None
        self.node_prediction = None

    def gini_best_score(self, y, possible_splits):
        best_gain = -np.inf
        best_idx = 0

        total_samples = len(y)
        for i in possible_splits:
            if i == 0:
                continue
            left_positive = sum(1 for x in y[:i + 1] if x == 1)
            right_positive = sum(1 for x in y[i + 1:] if x == 1)
            left_negative = sum(1 for x in y[:i + 1] if x == 0)
            right_negative = sum(1 for x in y[i + 1:] if x == 0)

                
            left_size = left_positive + left_negative
            right_size = right_positive + right_negative

            gini_left = 1 - (left_positive / left_size) ** 2 - (left_negative / left_size) ** 2
            gini_right = 1 - (right_positive / right_size) ** 2 - (right_negative / right_size) ** 2

            weight_left = left_size / total_samples
            weight_right = right_size / total_samples
            gini_gain = 1 - weight_left * gini_left - weight_right * gini_right

            if gini_gain > best_gain:
                best_gain = gini_gain
                best_idx = i


        return best_idx, best_gain

    def split_data(self, X, y, idx, val):
        left_mask = X[:, idx] < val
        return (X[left_mask], y[left_mask]), (X[~left_mask], y[~left_mask])

    def find_possible_splits(self, data):
        possible_split_points = []
        for idx in range(data.shape[0] - 1):
            if data[idx] != data[idx + 1]:
                possible_split_points.append(idx)
        return possible_split_points

    def find_best_split(self, X, y, feature_subset):
        best_gain = -np.inf
        best_split = None

        if feature_subset is None:
         feature_indices = list(range(X.shape[1]))  
        else:
            if isinstance(feature_subset, int):
                feature_indices = random.sample(range(X.shape[1]), feature_subset)
            else:
                feature_indices = list(feature_subset)

        for d in feature_indices:
            order = np.argsort(X[:, d]) 
            y_sorted = y[order]      
            possible_splits = self.find_possible_splits(X[order, d])  
            idx, gain = self.gini_best_score(y_sorted, possible_splits)  
            
            if gain > best_gain:  
                best_gain = gain
                best_split = (d, idx)  

        if best_split is None: 
            return None, None

 
        feature_idx, split_idx = best_split
        best_value = (X[split_idx, feature_idx] + X[split_idx + 1, feature_idx]) / 2  

        return feature_idx, best_value 


    def predict(self, x):
        if self.feature_idx is None:
            return self.node_prediction
        if x[self.feature_idx] < self.feature_value:
            return self.left_child.predict(x)
        else:
            return self.right_child.predict(x)

    def train(self, X, y, params):

        self.node_prediction = np.mean(y)
        if X.shape[0] == 1 or self.node_prediction == 0 or self.node_prediction == 1:
            return True

        self.feature_idx, self.feature_value = self.find_best_split(X, y, params["feature_subset"])
        if self.feature_idx is None:
            return True

        (X_left, y_left), (X_right, y_right) = self.split_data(X, y, self.feature_idx, self.feature_value)

        if X_left.shape[0] == 0 or X_right.shape[0] == 0:
            self.feature_idx = None
            return True

        # max tree depth
        if params["depth"] is not None:
            params["depth"] -= 1
        if params["depth"] == 0:
            self.feature_idx = None
            return True

        # create new nodes
        self.left_child, self.right_child = Node(), Node()
        self.left_child.train(X_left, y_left, copy.deepcopy(params))
        self.right_child.train(X_right, y_right, copy.deepcopy(params))
