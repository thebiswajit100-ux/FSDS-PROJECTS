import streamlit as st
import numpy as np
import pickle

model = pickle.load(open('D:\Machine_Learning\Regression_Model\Salary Prediction App\Model\linear_regression_model.pkl', 'rb'))

st.title('Salary Prediction App')

st.write('This app predicts the salary based on years of experience using a simple linear regression model.')

years_of_experience = st.number_input('Enter years of experience:', min_value=0.0, max_value=50.0, step=0.1)

if st.button('Predict Salary'):
    predicted_salary = model.predict(np.array([[years_of_experience]]))
    st.success(f'The predicted salary for {years_of_experience} years of experience is: ${predicted_salary[0]:,.2f}')
    

st.write('Remember, this is a simple linear regression model and may not account for all factors affecting salary. Use this prediction as a general estimate.')
