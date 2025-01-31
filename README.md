# SVM Classifier for Breast Cancer Detection
Overview

This project implements a Support Vector Machine (SVM) classifier using the dual optimization method for predicting the recurrence of breast cancer. The dataset used in this project is a breast cancer dataset that includes various features extracted from patient data.

# Project Structure
Data Preprocessing:

The dataset is read from a file and categorical data is mapped to numerical values using predefined mappings. This step is crucial for preparing the data for the SVM model.

SVM Dual Optimization:

The SVM classifier is built using a dual optimization approach. The dual function calculates the objective function for the dual form of the SVM, and the optimize function solves this optimization problem using scipy.optimize.minimize.
The weight vector w and bias b are determined from the optimized Lagrange multipliers. A decision function svm_func is generated to classify new data points.

Model Testing:

The performance of the SVM classifier is evaluated using a test dataset. The test function calculates the accuracy of the classifier on the selected data points.

Hyperplane Visualization:

The line function prints the equation of the decision boundary, which separates the classes in the feature space

# Files
You can find the dataset [here](./Breast_Cancer_dataset_2.txt).

The main Python script that includes data preprocessing, SVM optimization, and testing can be found [here](./svm_classifier.py).
