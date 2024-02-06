from flask import Flask, request, render_template
import openai
import requests

openai.api_key = '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'

server = Flask(__name__)

conversation_history = []  # List to store conversation history

def get_cat_photo():
    try:
        response = requests.get('https://api.thecatapi.com/v1/images/search?limit=1&breed_ids=beng&api_key=live_iBEgvsdSo7i90bVAVgEtAdhRHs7gQQ9v4uhxGpWzymcyMuQkQ5PhKLfnaR2Pqmds')
        if response.status_code == 200:
            data = response.json()
            return data[0]['url']
        else:
            return "Failed to fetch cat photo."
    except Exception as e:
        return str(e)

def send_gpt(prompt):
    if "cat" in prompt.lower() and "photo" in prompt.lower():
        cat_photo_url = get_cat_photo()
        if cat_photo_url:
            return cat_photo_url
        else:
            return "Sorry, I couldn't find a cat photo at the moment."
    else:
        try:
            response = openai.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)

@server.route('/', methods=['GET', 'POST'])
def get_request_json():
    global conversation_history  # Access the global conversation history list
    if request.method == 'POST':
        if len(request.form['question']) < 1:
            return render_template(
                'chat3.5.html', conversation=conversation_history, res="Question can't be empty!")
        question = request.form['question']
        print("======================================")
        print("Receive the question:", question)
        res = send_gpt(question)
        print("Q：\n", question)
        print("A：\n", res)
        
        # Append the question and response to the conversation history list
        conversation_history.append({"question": question, "response": res})

        return render_template('chat3.5.html', conversation=conversation_history)
    return render_template('chat3.5.html', conversation=conversation_history)

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=80)
