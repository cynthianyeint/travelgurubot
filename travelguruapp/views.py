from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import *

from datetime import datetime, time

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
		keyword = str(parameters.get("keyword"))
		if (keyword == "uncertainty"): #detect uncertainty - show images, videos
			res = show_images(keyword)
		elif (keyword == "positive"): #detect positive decision
			res = choose_place(keyword)
		elif (keyword == "thanks"): #detect thanks & ask user to rate service
			res = rate_service(keyword)
		else:
			res = makeWebhookResult(keyword)
	elif (action == "choose_place"): #request from button click - choosing place
		keyword = result.get("resolvedQuery")
		res = reply_click_event(keyword)
	else: #request from button click - rate service
		keyword = result.get("resolvedQuery")
		res = save_rate(keyword)
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
		speech = data.price_detail
	elif (keyword == "hmm"):
		speech = data.promotion_one + "\n" + "\n" + data.promotion_two
	elif (keyword == "room"):
		speech = "Ok, cool! I will notify my human colleagues about your choices. They will contact you as soon as possible to make further arrangements."
	else: 
		speech = "Sorry! I didn't get."

	return {
        "speech": speech,
        "displayText": speech,
        "source": "travelguru"
    }

def show_media(keyword):
	print ("Show media")
	return show_images(keyword)
	# show_video(keyword)


def show_images(keyword):
	speech = ":simple_smile:" + " Here are some photos of what you will see on the dinner cruise."
	attachments = []
	image = Image.objects.all()
	for i in image:
		attachments.append({
				"text": "",
				"fallback": "Sorry. We are not able to show pictures.",
				"callback_id": "show_image",
				"image_url": i.url,
				"color": "#3AA3E3"
			},)
	attachments.append({
		"text": "Here is a Youtube video of Langkawi: <https://www.youtube.com/watch?v=Sj_lR_UTt-s>",
		"color": "#3AA3E3"
	})

	slack_message ={
		"text": speech,
		"attachments": attachments
	}
	return {
        "speech": speech,
        "displayText": speech,
        "data": {"slack": slack_message},
        "source": "travelguru"
    }

def show_video(keyword):
	speech = "Here's a Youbue video of Langkawi"
	slack_message = {
		# "text": "<https://www.youtube.com/w atch?v=Sj_lR_UTt-s>",
		"text": "here is link: <http://imgs.xkcd.com/comics/regex_golf.png>"
	}
	return {
		"speech": speech,
		"displayText": speech,
		"data": {"slack": slack_message},
		"source": "travelguru"
	}

def choose_place(keyword):
	speech = "Great! You have definitely made the right choice!."
	places = Place.objects.all()
	place_name = []
	place_id = []
	for p in places:
		place_name.append(p.name)
		place_id.append(p.pk)
	
	button_details = []

	for i in range (0, places.count()):
		button_details.append({
				"name": "btn",
				"text": place_name[i],
				"type": "button",
				"value": place_id[i]
			})

	slack_message = {
		"text": speech,
		"attachments": [
			{
				"text": "Here are your choices: Please choose only 1 of them.",
				"callback_id": "choose_place",
				"color": "#3AA3E3",
				"attachment_type": "default",
				"actions": button_details
			}
		]
	}
	return {
		"speech": speech,
		"displayText": speech,
		"data": {"slack": slack_message},
		"source": "travelguru"
	}

def reply_click_event(keyword):
	selected_place = Place.objects.get(pk=keyword)
	speech = "Great! You choose: " + selected_place.description #retrieve answer from backend. 

	slack_message = {
		"text": speech,
		"attachments": [
			{
				"text": "Can you tell me more about the type of room that you intend to stay in?",
				"callback_id": "choose_place",
				"color": "#3AA3E3",
				"attachment_type": "default"
			}
		]
	}

	return {
		"speech": speech,
		"displayText": speech,
		"data": {"slack": slack_message},
		"source": "travelguru"
	}

def rate_service(keyword):
	speech = "Rate the services that I have provided on a scale of 1 to 5."

	slack_message = {
		"text": speech,
		"attachments":[
			{
				"text": speech,
				"callback_id": "rate_service",
				"color": "#3AA3E3",
				"attachment_type": "default",
				"actions": [
					{
						"name": "btn",
						"text": "1, terrible",
						"type": "button",
						"value": "terrible"
					},
					{
						"name": "btn",
						"text": "2, poor",
						"type": "button",
						"value": "poor"
					},
					{
						"name": "btn",
						"text": "3, average",
						"type": "button",
						"value": "average"
					},
					{
						"name": "btn",
						"text": "4, good",
						"type": "button",
						"value": "good"
					}
					,{
						"name": "btn",
						"text": "5, excellent",
						"type": "button",
						"value": "excellent"
					}
				]
			}
		]
	}

	return {
		"speech": speech,
		"displayText": speech,
		"data": {"slack": slack_message},
	}

def save_rate(keyword):

	#save rate result to database
	rating = Rate()
	rating.rate = keyword
	rating.save()

	now = datetime.now()
	now_time = now.time()

	print (now_time)
	if time(23,00) <= now_time <= time(8,0):#night time
		speech = "Thank you. Have a nice dream." #farewell msg for night time
	else: #day time
		speech = "Thank you. Have a great day ahead." #farewell msg for day time

	
	return {
		"speech": speech,
		"displayText": speech
	}

