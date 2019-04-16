from flask import Flask, make_response, request, jsonify

app = Flask(__name__)

# definition of the results function
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    if action == "":
        result = {} # an empty dictionary

        # fulfillment text is the default response that is returned to the dialogflow request
        result["fulfillmentText"] = "your response message here"

        # jsonify the result dictionary
        # this will make the response mime type to application/json
        result = jsonify(result)

        # return the result json
        return make_response(result)

# default route for the webhook
# it accepts both the GET and POST methods
@app.route('/webhook', methods=['GET', 'POST'])
def index():
    # calling the result function for response
    return results()

# call the main function to run the flask app
if __name__ == '__main__':
   app.run(debug=True)