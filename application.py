from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
application = Flask(__name__)


@application.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("queryResult").get("action") != "postalcode":
        pcode=req.get("queryResult").get("parameters").get("postalcode")
        if(pcode!= None):
            yql_url = "api.postcodes.io/postcodes/"+"pcode";
        #yql_url = getBaseUrl()
        result = urlopen(yql_url).read()
        data = json.loads(result)
        res = makeWebhookResult(data)
        return res
    else:
        return {}

##def getBaseUrl():
  ##  baseurl = "api.postcodes.io/postcodes/pcode"

def makeWebhookResult(data):
  #  kuralSet = data.get('KuralSet')
    if(data)is None:
        print ("Please enter valid postal code")
        return{}
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    City = data.get('admin_district')
    speech = longitude+latitude+City

    # if (line1 is None) or (line2 is None) or (translation is None):
    #     return {}


    # print(json.dumps(item, indent=4))


    print("Response:")
    print(speech)

    return {

    "fulfillmentText": speech

            }

if __name__ == '__main__':
    # port = int(os.getenv('PORT', 5000))
    #
    # print("Starting app on port %d" % port)
    #
    # app.run(debug=False, port=port, host='0.0.0.0')
    #to debug in local environmnet
    port = 8080

    application.run(debug=True, port=port, host='0.0.0.0')