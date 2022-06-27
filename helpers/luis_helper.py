# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from trip_details import TripDetails


class Intent(Enum):
    FIND_TRIP = "Find_trip"
    CANCEL = "Cancel"
    NONE_INTENT = "None"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)
            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.FIND_TRIP.value:
                result = TripDetails()

                to_entities = recognizer_result.entities.get("$instance", {}).get(
                    "to", []
                )
                if len(to_entities) > 0:
                    result.destination = to_entities[0]["text"].capitalize()

                from_entities = recognizer_result.entities.get("$instance", {}).get(
                    "from", []
                )
                if len(from_entities) > 0:
                    result.origin = from_entities[0]["text"].capitalize()

                budget_entities = recognizer_result.entities.get("$instance", {}).get(
                    "budget", []
                )
                if len(budget_entities ) > 0:
                    result.budget = budget_entities[0]["text"].capitalize()
                    
                dates = []

                start_date_entities = recognizer_result.entities.get("start_date", [])

                if start_date_entities:
                    result.start_date = start_date_entities[0]["timex"][0]
                    dates.append(result.start_date)
                    if len(start_date_entities) > 1:
                        result.end_date = start_date_entities[1]["timex"][0]
                        dates.append(result.end_date)

                end_date_entities = recognizer_result.entities.get("end_date", [])

                if end_date_entities:
                    result.end_date = end_date_entities[0]["timex"][0]
                    dates.append(result.end_date)
                    if len(end_date_entities) > 1:
                        result.start_date = end_date_entities[1]["timex"][0]
                        dates.append(result.start_date)

                other_date_entities = recognizer_result.entities.get("datetime", [])

                if len(other_date_entities):
                    datetime = other_date_entities[0]["timex"][0]
                    if "," in datetime:
                        dates = datetime.replace("(", "").split(",")
                    else:
                        dates.append(datetime)
                    if len(dates) > 1:
                        if dates[0] > dates[1]:
                            dates[0], dates[1] = dates[1], dates[0]
                        result.start_date = dates[0]
                        result.end_date = dates[1]

        except Exception as exception:
            print(exception)

        return intent, result
