import re, random

from flask import Flask, make_response, request, jsonify

from services import JobRecommendationService
from services import JobRetrievalService

app = Flask(__name__)

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

        print("PARAMS", params)

        keywords = params.get('userSkill') + ',' + params.get('userDegree')
        
        top5JobTitle = JobRecommendationService.give_suggestions(keywords)
        # top5JobTitle = ['CS Dev', 'Whatever Dev']

        buttons = []
        for job in top5JobTitle:
            button = {
            "type": "postback",
            "title": job,
            "payload": "Find Job " + job}
            buttons.append(button)

        result = {} # an empty dictionary

        payload = {
            "facebook": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "Here are possible job title suitable you, choose one.",
                        "buttons": buttons
                    }
                }
            }
        }

        
        result["payload"] = payload

        # jsonify the result dictionary
        # this will make the response mime type to application/json
        print(result)
        result = jsonify(result)
        print(result)
        # return the result json
        return make_response(result)

    elif action == "input.jobs":
        params = req.get('queryResult').get('parameters')
        result = {}
        print("PARAMS", params)
        jobQuery = params.get('job')
        jobs = JobRetrievalService.retreiveJobs(jobQuery)
        # jobs = ['XA','XA','XA','XA','XA','XA','XA','XA', 'XB', 'XA']
        print(jobs)
        elements = []
        for job in jobs:
            print("--> " + str(job))
            element = {
                "title": job + '|' + generateLocation(),
                "subtitle": generateCompanyName() + '\n\n' + generateSalary(),
                "default_action": {
                    "type": "web_url",
                    "url": "https://seek.com.au",
                    "messenger_extensions": "false",
                    "webview_height_ratio": "tall"
                }
            }
            elements.append(element)
        
        if not elements:
            payload = {
                "facebook": {
                    "attachment":{
                        "type":"template",
                        "payload":{
                            "template_type":"button",
                            "text":"Sorry we could not find a job in our database.",
                            "buttons":[
                                {
                                    "type":"web_url",
                                    "url":"https://www.seek.com.au/" + jobQuery + "-jobs",
                                    "title":"Search in Seek"
                                }
                            ]
                        }
                    }
                }
            }

        else:
            payload = {
              "facebook": {
                "attachment": {
                  "type": "template",
                  "payload": {
                    "template_type":"generic",
                    "elements": elements
                  }
                }
              }
            }

        result["payload"] = payload

        # jsonify the result dictionary
        # this will make the response mime type to application/json
        result = jsonify(result)
        # return the result json
        return make_response(result)


def generateCompanyName():
    companyChocies = ['Wipro', 'USYD', 'CommonWealth Bank', 'Bad Life Choices', 'Berger Paints', 'Healthy Life', 'Green Cookery', 'Uber', 'Ola', 'Masonary Choices', 'Fox News', 'Channel 9', 'News 9', 'Huawei AU', 'Spotify AU', 'UNSW', 'Tech Allstars']
    return companyChocies[random.randint(0, len(companyChocies) - 1)]


def generateLocation():
    locationChoices = ['Sydney', 'Canberra', 'New Castle', 'Perth']
    return locationChoices[random.randint(0, len(locationChoices) - 1)]


def generateSalary():
    return "AUD" + str(random.randint(50000, 105000))


# default route for the webhook
# it accepts both the GET and POST methods
@app.route('/webhook', methods=['GET', 'POST'])
def index():
    print('we are here')
    # calling the result function for response
    return results()


# call the main function to run the flask app
if __name__ == '__main__':
    app.run(debug=True)
