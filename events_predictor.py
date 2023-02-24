import openai
import datetime
import metaforecast_querier
import helpers
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("prompt.txt", "r") as f:
    prompt_base = f.read()


def get_current_date_str():
    """Returns the current date in ISO format (YYYY-MM-DD)."""

    return datetime.datetime.now().strftime("%Y-%m-%d")


def str_to_float_or_none(s):
    """Converts a string to a float or returns None if the string is not a number."""

    try:
        return float(s)
    except ValueError:
        return None


def replace_params(prompt, params):
    """Replaces the parameters in the prompt with the values in params.
    Parameters are indicated by [[param_name]] in the prompt."""

    for key, value in params.items():
        prompt = prompt.replace(key, value)
    return prompt


def average_results(result_strings, min_not_none=2):
    """Averages the results of a list of strings.
    The strings are expected to be floats or "None".
    If the number of non-None results is less than min_not_none, returns None."""

    results = [str_to_float_or_none(s) for s in result_strings]
    results = [r for r in results if r is not None]
    if len(results) < min_not_none:
        return None
    return sum(results) / len(results)


def predict_event(question, num_results=1, temperature=0, metaforecast_questions=""):
    """Predicts the probability of an event using the OpenAI API."""

    prompt = replace_params(
        prompt_base,
        {
            "[[date]]": get_current_date_str(),
            "[[question]]": question,
            "[[metaforecast-questions]]": metaforecast_questions,
        },
    )
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=4,
        temperature=temperature,
        n=num_results,
    )

    respones = [r.text for r in response.choices]
    print(respones)
    average = average_results(respones)
    response_text = (
        helpers.round_to_significant_digits(average, 3)
        if average is not None
        else "N/A"
    )

    return response_text


def main():
    test_question = "Will Biden get re-elected in 2024?"
    metaforecast_questions = metaforecast_querier.format_result(
        metaforecast_querier.search_metaforecast(test_question)
    )
    print(
        predict_event(
            test_question,
            num_results=5,
            temperature=0.5,
            metaforecast_questions=metaforecast_questions,
        )
    )
    print(metaforecast_questions)


if __name__ == "__main__":
    main()
