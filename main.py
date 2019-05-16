from flask import Flask, make_response, request, jsonify

# from services import JobRecommendationService
# from services import JobRetrievalService

app = Flask(__name__)

# definition of the results function
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    print('hey old fren')
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
        print('whoa')
        params = req.get('queryResult').get('parameters')
        keywords = params.get('UserDegree') + ' ' + params.get('UserSkill1') + ' ' + params.get('UserSkill2')
        print(keywords)
        # top5JobsTitle = JobRecommendationService.give_suggestions(keywords)
        # job_result = 
        top5JobsTitle = "Some Job Title";
        result = {} # an empty dictionary

        payload = {
          "facebook": {
            "attachment": {
              "type": "audio",
              "payload": {
                "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
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