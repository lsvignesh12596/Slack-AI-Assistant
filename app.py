import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import  SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from functions import draft_email


# Load environment variables from .env file
load_dotenv(find_dotenv())


# Set Slack API Creds
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the slack app
app = App(token = SLACK_BOT_TOKEN)

# Initialize the flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

def get_bot_user_id():
    """
    Get the bot user id using the Slack API.
    Returns:
        str: The bot user id
    """

    try:
        # Initialize the slack client with your bot token
        slack_client = WebClient(token = SLACK_BOT_TOKEN)
        response = slack_client.auth_test()
        return response['user_id']
    except SlackApiError as e:
        print(f"Error: {e}")


def my_function(text):
    """
    Custom function to process the text and return a response
    In this example, the function converts the input text to uppercase
    Args:
        text (str): The input text to process
    Returns:
        str: The processed text
    """
    response = text.upper()
    return response

@app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for emntions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from slack
        say (callable): A function for sending a response to the channel.
    """

    text = body["event"]['text']
    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    say("Sure, I'll get right on that!")
    # response = my_function(text)
    response = draft_email(text)
    say(response)

@flask_app.route("/slack/events", methods=['POST'])
def slack_events():
    """
    Route for handling slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return handler.handle(request)


# Run the flask app
if __name__ == "__main__":
    flask_app.run()
