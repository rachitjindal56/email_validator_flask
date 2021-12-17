from flask import Flask,flash, render_template, request
from flask.helpers import send_file
from werkzeug.utils import secure_filename
import requests
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['SECRET_KEY'] = '33c062ea7be6d2190072ca056353edfa'
api_key = "****"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
@app.route("/",methods=['POST','GET'])
def home():
    ans = ""
    filename = ""
    if request.method == "POST":
        file = request.files["file"]

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        output = []
        data = pd.read_csv('static/uploads/'+filename)

        df = data.iloc[:,0].values
        
        for x in df:
            response = requests.get(
                "https://isitarealemail.com/api/email/validate",
                params = {'email': x},
                headers = {'Authorization': "Bearer " + api_key })

            status = response.json()['status']
            ans = []
            if status == "valid":
                ans.append("Email is Valid")
            elif status == "invalid":
                ans.append("Email is Invalid")
            else:
                ans.append("Email was Unknown")
            
            output.append(ans[0])            

        data['Status'] = output
        data.to_csv(os.path.join('static/output/', filename))

        return render_template("home.html",filename=filename)
    
    return render_template("home.html",output=ans,filename=filename)

@app.route("/download/<path:fx>",methods = ['GET','POST'])
def download(fx):
    return send_file('static/'+fx,as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)