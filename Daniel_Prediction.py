# Internship Candidate - DANIEL PEREIRA DA COSTA
# Prediction model built based on Mission_Prediction_Dataset.csv dataset

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn import metrics

# Reading csv file
disease_data = pd.read_csv("/Users/danieldacosta/PycharmProjects/CyberLab/Mission_Prediction_Dataset.csv")  # Paste here the path to the CSV file

### PREPROCESSING DATA

# Analyzing Data statistics
disease_data.shape
disease_data.describe()

# Checking for Missing Values
disease_data.isnull().any().sum()

# Distribution of dataset
features = disease_data.iloc[:, 0:13].columns
for i in range(disease_data.shape[1] - 1):
    plt.figure(i+1)
    column = [disease_data[features[i]].values]
    sns.distplot(column)
    plt.xlabel(features[i])
features = ['column1', 'column4', 'column5', 'column8', 'column3', 'column7', 'column10', 'column11', 'column12', 'column13', 'column2', 'column6','column9','column14']
disease_data = disease_data[features]  # Putting side by side features with the same input data type

# Analyzing Output Distribution
data_size = disease_data.shape[0]
sick = disease_data[disease_data['column14'] == 1]
not_sick = disease_data[disease_data['column14'] == 0]
x = len(sick)/data_size
y = len(not_sick)/data_size
print('Sick :', x*100, '%')
print('Not sick :', y*100, '%')
plt.figure(14)  # Plotting output feature for distribution analysis
labels = ['Sick', 'Not Sick']
graph = pd.value_counts(disease_data['column14'], sort=True)
graph.plot(kind = 'bar', rot=0)
plt.title("Transaction class distribution")
plt.xticks(range(2), labels)
plt.xlabel("Class")
plt.ylabel("Frequency")

plt.figure(15)
sns.heatmap(disease_data.corr(), annot=True)  # Correlation Matrix of the Data


# Checking and Removing Outliers using Z-score function
z = np.abs(stats.zscore(disease_data))
threshold = 3
disease_data = disease_data[(z < 3).all(axis=1)]

# Scatter Plot - Uncomment only if needed. High computational time required.

#from pandas.plotting import scatter_matrix
#scatter_matrix(disease_data.iloc[1:, :]) #Correlacao entre os dados

# Normalizing Data

gaussian_features = disease_data.iloc[:, 0:4]  # Features with a gaussian distribution were standardized
sc = StandardScaler()
gaussian_featuresX = sc.fit_transform(gaussian_features)


categorical_features = disease_data.iloc[:, 4:10]  # Categorical features were normalized, except the binary ones
sc = MinMaxScaler(feature_range=(0, 1))
categorical_featuresX = sc.fit_transform(categorical_features)


X = np.concatenate((gaussian_featuresX, categorical_featuresX, disease_data.iloc[:, 10:13]), axis=1)  # Reassembling the data after nomalization
Y = disease_data.iloc[:, 13]
sc = StandardScaler()
X = sc.fit_transform(X)

# Splitting data for Training and Test sets

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30)


## CREATING NEURAL NETWORKS

classifier = Sequential()
# First Hidden Layer
classifier.add(Dense(7, activation='tanh', kernel_initializer='random_normal', input_dim=13))
# Second  Hidden Layer
classifier.add(Dense(7, activation='tanh', kernel_initializer='random_normal'))
# Output Layer
classifier.add(Dense(1, activation='sigmoid', kernel_initializer='random_normal'))

# Compiling the neural network

classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Early stopping

es = EarlyStopping(monitor='val_loss', mode='min',verbose=0, patience=10)

# Fitting the data to the training dataset

history = classifier.fit(X_train, y_train, batch_size=20, epochs=400, validation_split=0.1, callbacks=[es], verbose=0)
eval_model = classifier.evaluate(X_train, y_train, verbose=0)

# Training results

print('\nNeural Networks Results: ')

print('\nTrain loss:', eval_model[0])
print('Train Accuracy', eval_model[1])

y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Confusion Matrix

cm = confusion_matrix(y_test, y_pred)
print('\nConfusion Matrix: \n', cm)

# Test Results

eval_test = classifier.evaluate(X_test, y_test,verbose=0)
print('\nTest loss:', eval_test[0])
print('Test Accuracy', eval_test[1])

# Plot training history

plt.figure(16)
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.xlabel('Loss - Neural Network')


## SUPPORT VECTOR MACHINES

print('\nSupport Vector Machines Results:\n')

# Creating SVM

svclassifier = SVC(kernel='sigmoid', gamma='auto')
svclassifier.fit(X_train, y_train)
y_pred = svclassifier.predict(X_test)

# Confusion Matrix

print('Confusion Matrix\n', confusion_matrix(y_test, y_pred))

# SVM accuracy

print('SVM Accuracy: ', metrics.accuracy_score(y_test, y_pred))

plt.show()  # Comment this line if any figure wants to be displayed