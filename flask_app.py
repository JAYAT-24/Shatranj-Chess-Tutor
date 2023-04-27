from flask import Flask, render_template, request
from chess_engine import *

import openai
from flask import Flask, render_template


from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Set the API key from the .env file

app = Flask(__name__)
#openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def index():
    white_moves = "d4 d5 e4"
    black_moves = "Nc6 d6 h5"
    prompt = f"Given the following chess moves:\nWhite: {white_moves}\nBlack: {black_moves}\nWho is currently in advantage and list all cells that this side have control on? What is the next suggested move for white, just write 1 code for the next move?"
    try:
        headers = {
            "Authorization": f"Bearer {openai.api_key}"
        }
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
        )
        print(response)
        advantage = response.choices[0].text.strip()
        print(advantage)
        return render_template('index.html', advantage=advantage)

    except openai.error.InvalidRequestError as e:
        print(f"Invalid Request Error: {e}")
        return "An error occurred.invalid Please try again later."
    except openai.error.AuthenticationError as e:
        print(f"Authentication Error: {e}")
        return "An error occurred.authentication Please try again later."
    except openai.error.APIError as e:
        print(f"API Error: {e}")
        return "An error occurred. api  Please try again later."
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred.e Please try again later."


@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    print(depth)
    print("Calculating...")
    engine = Engine(fen)
    move = engine.iterative_deepening(depth - 1)
    print("Move found!", move)
    print()
    return move


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester


if __name__ == '__main__':
    app.run(debug=True)
