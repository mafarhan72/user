from flask import Flask, render_template, request
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('user_details')

app = Flask(__name__)

@app.route("/")
def index_page():
    # Renders the HTML file located in the 'templates' folder
    return render_template('index.html')

@app.route("/success", methods=["POST"])
def received_data():
    first_name= request.form.get("first_name")
    last_name=request.form.get("last_name")
    email= request.form.get("email")
    zip_code= request.form.get("zip")
    phone= request.form.get("phone")
    gender= request.form.get("gender")
    email_response = table.get_item(Key={"email":email})
    item = email_response.get("Item")
    if not item:              
        response = table.put_item(
            Item ={
                "first_name": first_name,
                "last_name":last_name,
                "email": email,
                "zip_code": zip_code,
                "phone": phone,
                "gender": gender,
            },)
        return render_template('index.html', message="User registered successfully!", status="success")
    else:
        return render_template('index.html', message="Email already exists", status="failed")
        
    


if __name__ == "__main__":
    app.run(debug=True)