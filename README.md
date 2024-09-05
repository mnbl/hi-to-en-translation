
# Hindi to English News Translation

This project is a web-based application that scrapes news headlines from Hindi news websites, translates them into English using Google Translate, and also provides an interface for Hindi to English text translation using a fine-tuned NLP model.

## Features
1. **Web Scraping**:
   - Scrapes news headlines from various Hindi news websites.
   - Cleans and processes the headlines to remove unnecessary characters, numbers, and special symbols.
   - Translates the headlines from Hindi to English using Google Translate.
   - Saves the original Hindi headlines and their English translations in CSV and Excel files.

2. **NLP Model**:
   - Utilizes the pre-trained model: `Helsinki-NLP/opus-mt-hi-en`.
   - Fine-tuned on the collected dataset of Hindi news headlines.
   - The model can translate Hindi text input to English.

3. **Flask App**:
   - Provides a simple web interface where users can input Hindi text and receive English translations.
   - The front-end is created using HTML and styled with CSS.
   - AJAX is used to send user input to the Flask backend for translation.

## File Details

### 1. `web_scrapping.py`
   - Scrapes news headlines from a list of predefined Hindi news websites.
   - Translates each headline into English using Google Translate.
   - Saves the scraped data (original and translated headlines) into `language.csv` and `language.xlsx` files.

### 2. `News Headlines Translation Hindi To English.ipynb`
   - A Jupyter Notebook demonstrating the training and fine-tuning of the pre-trained NLP model (`Helsinki-NLP/opus-mt-hi-en`) on the collected dataset of Hindi news headlines.
   
### 3. `app.py`
   - A Flask-based web application for translating Hindi text into English.
   - Users can enter Hindi text, and the app will display the corresponding English translation.


## Requirements

- Python 3.x
- Flask
- BeautifulSoup4
- Requests
- Googletrans (Google Translate API)
- Transformers (Hugging Face)
- Pandas
- NLTK
- Matplotlib
- Seaborn
- WordCloud
- Numpy
- Gensim
- Scikit-learn
- Torch

## How to Run the Project

### Step 1: Install Dependencies
```bash
$ pip3 install -r requirements.txt
```

### Step 2: Run Web Scraping Script
```bash
$ python web_scrapping.py
```
This will scrape news headlines, translate them, and save them into CSV and Excel files.

### Step 3: Run Notebook file
```bash
$ jupyter notebook
open "News Headlines Translation Hindi To English.ipynb"
```
This will preprocess the data and train language translation model.

### Step 3: Run the Flask App
```bash
$ python app.py
```
Go to `http://127.0.0.1:5000` in your browser and start translating Hindi text into English using the NLP model.

## Example Usage

### Web Scraping:
The script scrapes headlines from websites like:
- Jagran
- Bhaskar
- NDTV
- Amar Ujala
- Navbharat Times
...and many more.

The collected data is saved in a file called `language.csv` and `language.xlsx`.

### Flask App:
The web app allows you to input Hindi text (e.g., "नमस्ते") and get the English translation ("Hello") instantly.
