from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import *

import json
import os

# Create your views here.
def test(request):
	return HttpResponse("return this string")

@csrf_exempt
def webhook(request):
	if request.method == 'POST':
		req = JSONParser().parse(request)
		res = processRequest(req)
		return JsonResponse(res, safe=False)

def processRequest(req):
	result = req.get("result")
	action = result.get("action")
	parameters = result.get("parameters")

	print ("Result: ", result)
	print ("Action: ", action)
	print("Parameters: ", parameters)
	print(str(parameters.get("keyword")))

	if (action == "handle_request"):
		#keyword = result.get('resolvedQuery')
		keyword = str(parameters.get("keyword"))
		res = makeWebhookResult(keyword)
	elif (action == "button_test"):
		keyword = result.get('resolvedQuery')
		res = testButton(keyword)
	else:
		keyword = "testing"
		res = makeWebhookResult(keyword)
	return res

def makeWebhookResult(keyword):
	print ("Keyword: ", keyword)
	speech = "Typed: " + keyword 

	data = General.objects.all().first()
	print ("Data: ", data.price)

	if (keyword == "accept"):
		speech = "Have you heard of the new travel destination in Malaysia that as awesome as Mauritius but at an amazingly low price?"
	elif (keyword == "reject"):
		speech = "No problem, thanks."
	elif (keyword == "tellmore"):
		speech = "We are having an amazing promotion now. Only " + data.price + " per person for a weekend vacation at Langkawi"
	elif (keyword == "askprice"):
		#speech = "The price includes 2 days, 1 night stay, at a hotel of your choice from our trusted hotel partners. All meals included. How does that sound to you?"
		speech = data.price_detail
	elif (keyword == "hmm"):
		#speech = "Don't hestitate any longer! This promotional price is only valid if you book before 8th August 2017." + " In addition, we will throw in a dinner cruise free of charge if you sign up together!"
		speech = data.promotion_one + "\n" + "\n" + data. promotion_two
	elif (keyword == "uncertainty"):
		speech = "Here are some photos of what you will see on the dinner cruise."
	else:
		speech = "Testing"

	return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "travelguru"
    }

def testButton(keyword):
	print ("Keyword: ", keyword)
	speech = "Testing button.."
	
	slack_message = {
		"text": speech,
		"attachments": [
			{
				"text": "Please Choose:",
				"fallback": "Sorry. You are unable to choose",
				"callback_id": "button_test",
				"color": "#3AA3E3",
				"attachment_type": "default",
				"actions": [
					{
						"name": "btn",
						"text": "Btn1",
						"type": "button",
						"value": "one"
					},
					{
						"name": "btn",
						"text": "Btn2",
						"type": "button",
						"value": "two"
					}
				]
			}
		]
	}

	return {
        "speech": speech,
        "displayText": speech,
        "data": {"slack": slack_message},
        "source": "travelguru"
    }
