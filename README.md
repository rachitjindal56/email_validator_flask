# email_validator_flask

## API usd form: https://isitarealemail.com/

This repo contains a web app for verification of bulk email addresses.
It uses Python Flask for developement and Heroku for deployment

## Insert your api_key (taken from above link) and also make a custom SECRET_KEY using following code :
# { secrets.token_hex(16) }
app.config['SECRET_KEY'] = '33c062ea7be6d2190072ca056353edfa'
api_key = "****"

# The below code takes file ('.csv') as input and stores it in the upload_folder present in static folder.
file = request.files["file"]

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   
# Now read the uploaded file containing the email
        output = []
        data = pd.read_csv('static/uploads/'+filename)

        df = data.iloc[:,0].values
 
# The code-snippet given requeats the api to validate the email from the doc and returns the status nd confidence of the entered email.
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
