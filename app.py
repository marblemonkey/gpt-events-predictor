import os
import metaforecast_querier
import events_predictor
import logging
import ast
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=("GET", "POST"))
def index():
\

    if request.method == "POST":
        question = request.form["question"]
        metaforecast_questions = metaforecast_querier.search_metaforecast(question)
        formatted_metaforecast_questions = metaforecast_querier.format_result(
            metaforecast_questions
        )
        response = events_predictor.predict_event(
            question,
            metaforecast_questions=formatted_metaforecast_questions,
            num_results=5,
            temperature=0.5,
        )
        app.logger.info(f"Response: {response}")
        return redirect(
            url_for(
                "index",
                result=response,
                metaforecast_questions=metaforecast_questions,
            )
        )

    result = request.args.get("result")
    metaforecast_questions = request.args.get("metaforecast_questions")

    if metaforecast_questions:
        metaforecast_questions = ast.literal_eval(metaforecast_questions)
        metaforecast_question_objs = (
            metaforecast_querier.result_dict_to_question_objects(metaforecast_questions)
        )
    else:
        metaforecast_question_objs = []

    return render_template(
        "index.html",
        result=result,
        metaforecast_questions=metaforecast_question_objs,
    )


if __name__ == "__main__":
    app.run(debug=True)
