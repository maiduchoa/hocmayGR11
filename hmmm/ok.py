import re

import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("train.csv")


data.head()
data.info()
data.columns 
to_remove = ['ID', 'Customer_ID', 'Month', 'Name', 'Age', 'SSN', 'Occupation', 'Type_of_Loan']
data = data.drop(columns=to_remove)
data.info()
data.columns
columns = [
    'Annual_Income', 'Num_of_Loan', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit',
    'Num_Credit_Inquiries', 'Outstanding_Debt', 'Amount_invested_monthly', 'Monthly_Balance'
]
for col in columns:
    print("\n")
    print(data[col].describe())
    print(data[col].unique())
for col in columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")
    print("\n")
    print(data[col].info())
data['Credit_History_Age'].unique()
def age_to_days(age):
    if age is np.nan:
        return age
    years = 0
    months = 0
    years_match = re.search(r'(\d+)\s*Years?', age)
    months_match = re.search(r'(\d+)\s*Months?', age)
    if years_match:
        years = int(years_match.group(1))
    if months_match:
        months = int(months_match.group(1))
    return (years * 365) + (months * 30)
    
data['Credit_History_Age'] = data['Credit_History_Age'].apply(age_to_days)
data['Credit_History_Age'].info()
data.info()
columns = [
    'Annual_Income', 'Monthly_Inhand_Salary', 'Num_of_Loan', 'Num_of_Delayed_Payment',
    'Changed_Credit_Limit', 'Num_Credit_Inquiries', 'Outstanding_Debt', 'Credit_History_Age',
    'Amount_invested_monthly', 'Monthly_Balance'
]
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
data[columns] = imputer.fit_transform(data[columns])
for col in columns:
    print('\n')
    print(data[col].info())
data.info()
data['Credit_Mix'].unique()
data['Credit_Mix'] = data['Credit_Mix'].replace('_', 'Standard')
data['Credit_Mix'].unique()
le = LabelEncoder()
data['Credit_Mix'] = le.fit_transform(data['Credit_Mix'])
data['Credit_Mix'].info()
data['Credit_Mix'].unique()
data['Payment_Behaviour'].unique()
data = data[data['Payment_Behaviour'] != '!@9#%8']
data.info()
le = LabelEncoder()
data['Payment_Behaviour'] = le.fit_transform(data['Payment_Behaviour'])
data['Payment_Behaviour'].info()
data['Payment_Behaviour'].unique()
data['Payment_of_Min_Amount'].unique()
data['Payment_of_Min_Amount'] = data['Payment_of_Min_Amount'].replace('NM', 'No')
data.info()
data['Payment_of_Min_Amount'].unique()
le = LabelEncoder()
data['Payment_of_Min_Amount'] = le.fit_transform(data['Payment_of_Min_Amount'])
data['Payment_of_Min_Amount'].info()
data['Payment_of_Min_Amount'].unique()
data['Credit_Score'].unique()
credit_score_le = LabelEncoder()
data['Credit_Score'] = credit_score_le.fit_transform(data['Credit_Score'])
data['Credit_Score'].info()
data['Credit_Score'].unique()
data.info()
X, y = data.iloc[:, :-1], data.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_train.shape, y_train.shape
X_test.shape, y_test.shape
gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
print(classification_report(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", cbar=False, xticklabels=credit_score_le.inverse_transform([0, 1, 2]), yticklabels=credit_score_le.inverse_transform([0, 1, 2]))
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show();