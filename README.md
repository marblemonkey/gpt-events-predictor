# Event Predictor App

This is a web app that uses the OpenAI API to make probablistic predictions about future events given by the user.
You can see it online at [predictor.pmdata.info](http://predictor.pmdata.info/).

## How it works

The app queries [Metaforecast](https://metaforecast.org/) for similar questions and provides those probability estimates to the the provided questions.
It provides those estimates to GPT as part of the text prompt and asks GPT to predict the probability of the event occuring.

It takes multiple samples from GPT and averages the probability estimates to get a final estimate.

## Setup

```pip install -r requirements.txt```

## Run

First set the value of the environment variable `OPENAI_API_KEY` to your OpenAI API key.
Then run the app.

Using Flask
   
   ```flask run```

Using Gunicorn

   ```gunicorn app:app```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
