# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import (
    MessageFactory,
    TurnContext,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.schema import InputHints

from trip_details import TripDetails
from trip_finding_recognizer import TripFindingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from .trip_finding_dialog import TripFindingDialog

class MainDialog(ComponentDialog):
    def __init__(
        self,
        luis_recognizer: TripFindingRecognizer,
        trip_finding_dialog: TripFindingDialog,
        telemetry_client: BotTelemetryClient = None,
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)
        self.telemetry_client = telemetry_client or NullTelemetryClient()

        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = self.telemetry_client

        trip_finding_dialog.telemetry_client = self.telemetry_client

        wf_dialog = WaterfallDialog(
            "WFDialog", [self.intro_step, self.act_step, self.review_step, self.final_step]
        )
        wf_dialog.telemetry_client = self.telemetry_client

        self._luis_recognizer = luis_recognizer
        self._trip_finding_dialog_id = trip_finding_dialog.id

        self.add_dialog(text_prompt)
        self.add_dialog(trip_finding_dialog)
        self.add_dialog(wf_dialog)

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Store user request
        step_context.values["user_request"] = str(step_context.result)

        if not self._luis_recognizer.is_configured:
            return await step_context.begin_dialog(
                self._trip_finding_dialog_id, TripDetails()
            )

        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        return await step_context.begin_dialog(self._trip_finding_dialog_id, luis_result)

    async def review_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result is not None:
            result = step_context.result
            msg_txt = f"I understood you want to go to {result.destination} from {result.origin}, going on {result.start_date}, and returning on {result.end_date}, for a maximum budget of {result.budget} per person."
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Did I manage to understand your request correctly?")
            ),
        )


    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_review = str(step_context.result).lower()
        if "n" in user_review and not "y" in user_review:
            self.telemetry_client.track_exception("Bad_Answer", properties = {"user_request": step_context.values['user_request']})
        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)

