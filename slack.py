import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient
from slack_bolt import App

# Set your tokens
SLACK_BOT_TOKEN = "blank"
SLACK_APP_TOKEN = "blank"
OPENAI_API_KEY = "blank"

# Initialize Slack app and client
app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)

# Event handler for bot mentions
@app.event("app_mention")
def handle_message_events(body, logger):
    # Extract prompt from mention message
    prompt = body["event"]["text"].split(">")[1].strip()

    # Inform the user that the bot is processing the request
    client.chat_postMessage(
        channel=body["event"]["channel"],
        text="Hello from your bot! :robot_face: \nThanks for your request, I'm on it!"
    )

    # Call OpenAI API to generate response
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )

        # Extract response from the completion
        generated_text = response.choices[0].message["content"]

        # Reply to the channel with the generated response
        client.chat_postMessage(
            channel=body["event"]["channel"],
            text=f"Here you go: \n{generated_text}"
        )
    except openai.error.RateLimitError:
        # Handle rate limit error
        client.chat_postMessage(
            channel=body["event"]["channel"],
            text="Sorry, I'm currently experiencing high demand. Please try again later."
        )

if __name__ == "__main__":
    # Start the Slack Socket Mode handler
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
