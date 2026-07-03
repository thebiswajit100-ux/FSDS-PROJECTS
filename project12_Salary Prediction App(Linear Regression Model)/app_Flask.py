import sys

# Check if the script is run with Streamlit or directly with Python (Flask)
is_streamlit = any('streamlit' in arg for arg in sys.argv) or 'run' in sys.argv

if is_streamlit:
    # ==========================================
    # ORIGINAL STREAMLIT CODE (NO MODIFICATIONS)
    # ==========================================
    import streamlit as st
    import pickle
    import numpy as np
    
    #Load the trained model from the pickle file
    model= pickle.load(open('D:\Machine_Learning\Regression_Model\Salary Prediction App\Model\linear_regression_model.pkl','rb'))
    
    # Set the title of the app
    st.title("Salary Prediction App")
    #Description of the app
    st.write("This app predicts the salary based on years of experience using a simple linear regression model.")
    
    # Add input widget for years of experience
    years_experience = st.number_input("Enter years of experience:", min_value=0.0, max_value=50.0, step=0.1)
    
    # When button is clicked, make prediction and display the result
    if st.button("Predict Salary"):
        # Make a prediction using the trained model
        experience_input = np.array([[years_experience]])  # Convert the input to a 2D array for prediction
        prediction = model.predict(experience_input)
       
        # Display the result
        st.success(f"The predicted salary for {years_experience} years of experience is: ${prediction[0]:,.2f}")
       
    # Display information about the model
    st.write("The model was trained using a dataset of salaries and years of experience.built model by prakash senapati")

else:
    # ==========================================
    # FLASK DEPLOYMENT CODE
    # ==========================================
    from flask import Flask, request, render_template_string
    import pickle
    import numpy as np
    
    app = Flask(__name__)
    
    # Load the trained model using the original absolute path
    model = pickle.load(open('D:\Machine_Learning\Regression_Model\Salary Prediction App\Model\linear_regression_model.pkl', 'rb'))
    
    # Simple HTML page with form and results
    HTML_TEMPLATE = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Salary Prediction App</title>
    </head>
    <body>
        <h2>Salary Prediction App (Flask Version)</h2>
        <p>This app predicts the salary based on years of experience using a simple linear regression model.</p>
        
        <form method="POST" action="/">
            <label for="years_experience">Enter years of experience (0.0 to 50.0):</label>
            <input type="number" step="0.1" min="0" max="50" name="years_experience" id="years_experience" required value="{{ years_experience }}">
            <button type="submit">Predict Salary</button>
        </form>
    
        {% if error %}
            <p style="color: red;">{{ error }}</p>
        {% endif %}
    
        {% if prediction is not none %}
            <h3>Prediction Result:</h3>
            <p>The predicted salary for <strong>{{ years_experience }}</strong> years of experience is: <strong>${{ "{:,.2f}".format(prediction) }}</strong></p>
        {% endif %}
    
        <br>
        <small>Model built by prakash senapati. Deployed using Flask.</small>
    </body>
    </html>'''
    
    @app.route('/', methods=['GET', 'POST'])
    def home():
        prediction = None
        years_experience = ""
        error = None
        
        if request.method == 'POST':
            try:
                raw_input = request.form.get('years_experience', '')
                years_experience = float(raw_input)
                
                # Input validation constraints
                if years_experience < 0.0 or years_experience > 50.0:
                    error = "Validation Error: Years of experience must be between 0.0 and 50.0."
                else:
                    experience_input = np.array([[years_experience]])
                    pred = model.predict(experience_input)
                    prediction = float(pred[0])
            except ValueError:
                error = "Validation Error: Please enter a valid decimal number."
            except Exception as e:
                error = f"Error during prediction: {str(e)}"
                
        return render_template_string(HTML_TEMPLATE, error=error, years_experience=years_experience, prediction=prediction)
    
    # Set secure headers in after_request
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    
    if __name__ == '__main__':
        # Listen only on localhost for development security
        app.run(host='127.0.0.1', port=5000, debug=True)