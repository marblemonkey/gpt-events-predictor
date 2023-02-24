from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from collections import namedtuple
import helpers

transport = RequestsHTTPTransport(url="https://metaforecast.org/api/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

platforms_query = gql(
    """
    {
        platforms{
            id
        }
    }
    """
)


def search_metaforecast(search_str, num_results=5):
    """Searches metaforecast for questions matching the given string"""

    platforms = client.execute(platforms_query)
    platforms = [platform["id"] for platform in platforms["platforms"]]
    print(platforms)

    variables = {
        "SearchInput": {
            "forecastingPlatforms": platforms,
            "forecastsThreshold": 0,
            "limit": num_results,
            "query": search_str,
            "starsThreshold": 2,
        }
    }

    query = gql(
        """
        query SearchQuestions($SearchInput: SearchInput!) {
            searchQuestions(input: $SearchInput) {
                platform {
                    id
                }
                title
                options {
                    name
                    probability
                }
            }
        }
        """
    )

    result = client.execute(query, variable_values=variables)
    return result


def get_question_yes_probability(question):
    """Returns the probability that the given question will be answered yes"""

    for option in question["options"]:
        if option["name"] == "Yes":
            return option["probability"]
    return None


def format_result(result, num_results=5):
    """Formats the result of a search into a string"""

    valid_results = [
        question
        for question in result["searchQuestions"]
        if get_question_yes_probability(question)
    ]
    top_results = valid_results[:num_results]

    result_str = ""
    for question in top_results:
        result_str += f"Q: {question['title']}"
        result_str += "\n"
        result_str += f"Probability: {get_question_yes_probability(question):.3f}"
        result_str += "\n\n"

    return result_str


def result_dict_to_question_objects(result):
    """Converts the result of a search into a list of Question objects"""

    Question = namedtuple("Question", ["title", "platform", "probability"])

    questions = []
    for question in result["searchQuestions"]:
        probability = get_question_yes_probability(question)
        if probability:
            questions.append(
                Question(
                    title=question["title"],
                    platform=question["platform"]["id"],
                    probability=helpers.round_to_significant_digits(probability, 3),
                )
            )
    return questions


if __name__ == "__main__":
    result = search_metaforecast("Biden")
    print(result)
    print(format_result(result))
