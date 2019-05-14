from flask import Flask, make_response, request, jsonify
import pandas as pd

from recommendationEngine import recommendationApp

app = Flask(__name__)

df_data = pd.read_csv('seek_australia.csv')

# definition of the results function
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    '''
    "action": "input.skills",
    "parameters": {
      "UserName": "Aaquib Ladiwala",
      "UserDegree": "Masters in IT",
      "UserSkill1": "Programming Java",
      "UserSkill2": "Python AEM"
    },
    '''
    if action == "input.skills":
        params = req.get('queryResult').get('parameters')
        keywords = params.get('UserDegree') + ' ' + params.get('UserSkill1') + ' ' + params.get('UserSkill2')

        top5JobsTitle = recommendationApp.give_suggestions(keywords)
        job_result = 

        result = {} # an empty dictionary

        # fulfillment text is the default response that is returned to the dialogflow request
        result["fulfillmentText"] = 'Suggested job titles'

        # display cards

        

        # jsonify the result dictionary
        # this will make the response mime type to application/json
        result = jsonify(result)

        # return the result json
        return make_response(result)

def retreiveJobs(job_title='Business Analyst', job_type='Full Time', city='Sydney'):
    searchResultDf = df[(df['city']=='Sydney') & (df['job_title']=="Business Analyst") & (df['job_type']=="Full Time")]

# default route for the webhook
# it accepts both the GET and POST methods
@app.route('/webhook', methods=['GET', 'POST'])
def index():
    # calling the result function for response
    return results()

# call the main function to run the flask app
if __name__ == '__main__':
    app.run(debug=True)