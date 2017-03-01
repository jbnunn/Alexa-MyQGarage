import requests
import os
import json
import time
import myq

USERNAME = "<MYQ_LOGIN_USERNAME>"
PASSWORD = "<MYQ_LOGIN_PASSWORD>"
mq = myq.MyQ(USERNAME,PASSWORD)

def lambda_handler(event, context):

    if event['session']['application']['applicationId'] != "amzn1.ask.skill.<your-alexa-skills-id>":
        print "Invalid Application ID"
        raise
    else:
        # Not using sessions for now
        sessionAttributes = {}
        mq.login()
        mq.get_device_id()

        if event['session']['new']:
            onSessionStarted(event['request']['requestId'], event['session'])
        if event['request']['type'] == "LaunchRequest":
            speechlet = onLaunch(event['request'], event['session'])
            response = buildResponse(sessionAttributes, speechlet)
        elif event['request']['type'] == "IntentRequest":
            speechlet = onIntent(event['request'], event['session'])
            response = buildResponse(sessionAttributes, speechlet)
        elif event['request']['type'] == "SessionEndedRequest":
            speechlet = onSessionEnded(event['request'], event['session'])
            response = buildResponse(sessionAttributes, speechlet)

        # Return a response for speech output
        return(response)



# Called when the session starts
def onSessionStarted(requestId, session):
    print("onSessionStarted requestId=" + requestId + ", sessionId=" + session['sessionId'])

# Called when the user launches the skill without specifying what they want.
def onLaunch(launchRequest, session):
    # Dispatch to your skill's launch.
    getWelcomeResponse()

# Called when the user specifies an intent for this skill.
def onIntent(intentRequest, session):
    intent = intentRequest['intent']
    intentName = intentRequest['intent']['name']

    # Dispatch to your skill's intent handlers
    if intentName == "StateIntent":
        return stateResponse(intent)
    elif intentName == "MoveIntent":
        return moveIntent(intent)
    elif intentName == "HelpIntent":
        return getWelcomeResponse()
    else:
        print "Invalid Intent (" + intentName + ")"
        raise

# Called when the user ends the session.
# Is not called when the skill returns shouldEndSession=true.
def onSessionEnded(sessionEndedRequest, session):
    # Add cleanup logic here
    print "Session ended"

def getWelcomeResponse():
    cardTitle = "Welcome"
    speechOutput = """You can open or close your garage door by saying, ask my garage door to open."""

    # If the user either does not reply to the welcome message or says something that is not
    # understood, they will be prompted again with this text.
    repromptText = 'Ask me to close your garage door by saying ask my garge door to close'
    shouldEndSession = True

    return (buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))

def moveIntent(intent):
    """
    Ask my garage to {open|close|shut|go up|go down}
        "intent": {
          "name": "StateIntent",
          "slots": {
            "doorstate": {
              "name": "doorstate",
              "value": "close"
            }
          }
        }
    """
    if (intent['slots']['doorstate']['value'] == "close") or (intent['slots']['doorstate']['value'] == "shut") or (intent['slots']['doorstate']['value'] == "go down"):
        mq.close()
        speechOutput = "Ok, I'm closing your garage door"
        cardTitle = "Closing your garage door"
    elif (intent['slots']['doorstate']['value'] == "open") or (intent['slots']['doorstate']['value'] == "go up"):
        mq.open()
        speechOutput = "Ok, I'm opening your garage door"
        cardTitle = speechOutput
    else:
        speechOutput = "I didn't understand that. You can say ask the garage door to open or close"
        cardTitle = "Try again"

    repromptText = "I didn't understand that. You can say ask the garage door if it's open, or tell it to open or close"
    shouldEndSession = True

    return(buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))

def stateResponse(intent):
    """
    Ask my garage door if it's {open|closed}
        "intent": {
          "name": "StateIntent",
          "slots": {
            "doorstate": {
              "name": "doorstate",
              "value": "closed"
            }
          }
        }
    """
    doorstate = mq.status()

    if (intent['slots']['doorstate']['value'] == "open") or (intent['slots']['doorstate']['value'] == "up"):
        if doorstate == "open":
            speechOutput = "Yes, your garage door is open"
            cardTitle = "Yes, your garage door is open"
        elif doorstate == "closed":
            speechOutput = "No, your garage door is closed"
            cardTitle = "No, your garage door is closed"
        else:
            speechOutput = "Your garage door is " + doorstate
            cardTitle = "Your garage door is " + doorstate

    elif (intent['slots']['doorstate']['value'] == "closed") or (intent['slots']['doorstate']['value'] == "shut") or (intent['slots']['doorstate']['value'] == "down"):
        if doorstate == "closed":
            speechOutput = "Yes, your garage door is closed"
            cardTitle = "Yes, your garage door is closed"
        elif doorstate == "open":
            speechOutput = "No, your garage door is open"
            cardTitle = "No, your garage door is open"
        else:
            speechOutput = "Your garage door is " + doorstate
            cardTitle = "Your garage door is " + doorstate

    else:
        speechOutput = "I didn't understand that. You can say ask the garage door if it's open"
        cardTitle = "Try again"

    repromptText = "I didn't understand that. You can say ask the garage door if it's open"
    shouldEndSession = True

    return(buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))


# --------------- Helpers that build all of the responses -----------------------
def buildSpeechletResponse(title, output, repromptText, shouldEndSession):
    return ({
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": "MyQ - " + title,
            "content": "MyQ - " + output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": repromptText
            }
        },
        "shouldEndSession": shouldEndSession
    })

def buildResponse(sessionAttributes, speechletResponse):
    return ({
        "version": "1.0",
        "sessionAttributes": sessionAttributes,
        "response": speechletResponse
    })
