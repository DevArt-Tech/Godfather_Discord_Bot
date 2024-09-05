import requests
import random


def get_message(user_message: str, token: str):
    response = requests.get(
        f'https://api.wit.ai/message?q={user_message}',
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.json()


def parse_message(config: dict, wit_ai_response: dict):
    intents = [intent["name"] for intent in wit_ai_response["intents"]]
    for intent in intents:
        entities = config["question"]["intents"][intent]["entities"]
        entities_response_keys = list(wit_ai_response["entities"].keys())
        entity_complete = ""
        for entity in entities_response_keys:
            if entity is not None:
                entity = entity.split(":")[0]
                entity_complete += entity + "-"
        entity_complete = entity_complete[:-1]

        bot_answers = entities[entity_complete]["bot_answers"]
        response_message = random.choice(bot_answers)

    return response_message