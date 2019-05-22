import re

from flask import Flask, make_response, request, jsonify

# from services import JobRecommendationService
# from services import JobRetrievalService

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
        

        # top5JobTitle = JobRecommendationService.give_suggestions(keywords)
        top5JobTitle = ['CS Dev', 'Whatever Dev']

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

    else if action == "input.skills":
        params = req.get('queryResult').get('parameters')
        print("PARAMS", params)


        payload = {
          "facebook": {
            "attachment": {
              "type": "template",
              "payload": {
                
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