from flask import Flask, request, jsonify, render_template_string
from transformers import MarianMTModel, MarianTokenizer, GenerationConfig

app = Flask(__name__)

# Load your model and tokenizer
model_name = "Helsinki-NLP/opus-mt-hi-en"
tokenizer = MarianTokenizer.from_pretrained("./saved_model")
model = MarianMTModel.from_pretrained("./saved_model")

# Define the HTML template for the web page, including JavaScript for AJAX
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Translator</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            margin: 40px;
            background-color: #f4f4f9;
            color: #333;
        }
        textarea, button, p {
            font-size: 16px;
        }
        textarea {
            width: 80%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box; /* Makes sure the padding does not affect the specified width */
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background-color: #45a049;
        }
        #translation {
            padding: 10px;
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-top: 20px;
            min-height: 50px;
        }
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script>
    $(document).ready(function(){
        $('#translate-button').click(function(){
            var textToTranslate = $('#text-to-translate').val();
            $.ajax({
                url: '/translate',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ text: textToTranslate }),
                success: function(data) {
                    $('#translation').text(data.translation);
                }
            });
        });
    });
    </script>
</head>
<body>
    <h1>Translate from Hindi to English</h1>
    <textarea id="text-to-translate" rows="5" cols="60" placeholder="Enter Hindi text here..."></textarea>
    <br>
    <button id="translate-button">Translate</button>
    <h2>Translation:</h2>
    <p id="translation"></p>
</body>
</html>
'''



@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text_to_translate = data['text']
    inputs = tokenizer(text_to_translate, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=512, num_beams=6, bad_words_ids=[[61126]], forced_eos_token_id=0)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(debug=True)