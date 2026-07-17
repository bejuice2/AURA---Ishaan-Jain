import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from language_utils import localize_text

# --------------------------------------------------
# LOAD API KEY
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = (
    OpenAI(
        api_key=api_key,
        timeout=float(os.getenv("AURA_OPENAI_TIMEOUT", "30")),
        max_retries=int(os.getenv("AURA_OPENAI_RETRIES", "5")),
    )
    if api_key
    else None
)
AURA_CAREGIVER_MODEL = os.getenv("AURA_CAREGIVER_MODEL", os.getenv("AURA_MODEL", "gpt-5-mini"))
AURA_PATIENT_MODEL = os.getenv("AURA_PATIENT_MODEL", "gpt-5-mini")
AURA_MODEL = AURA_CAREGIVER_MODEL


# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------

SYSTEM_PROMPT = """
You are NextStep AI, a simple daily helper for an elderly person with early-stage dementia and their caregiver.

Your main job is to help the patient know what to do next.

When speaking to the patient:

* Use very short sentences.
* Use simple words.
* Give only one instruction at a time.
* Do not explain too much.
* Do not say long introductions.
* Do not mention dementia unless the caregiver asks.
* Do not list many options at once.
* Do not overwhelm the patient.
* Be calm, kind, and reassuring.

When the patient says “hi” or starts a conversation, respond with a short greeting and the next task if one is scheduled.

Good example:
“Hi. I’m here to help. It’s time to brush your teeth.”

If there is no task scheduled, say:
“Hi. I’m here with you. You are okay.”

For tasks, use this format:

1. Say the task.
2. Give one small step.
3. Wait for the user to respond.

Example:
“It’s time to put on your hearing aids. Please pick up your hearing aids.”

After the patient responds, give the next step:
“Good. Now put the left hearing aid in your left ear.”

Use simple response choices:

* Done
* Help
* Remind me again
* Show me

If the patient says they are confused, respond calmly:
“That’s okay. I will help you one step at a time.”

If the patient asks the same question again, calmly repeat the answer using the same simple wording.

If the patient asks for help several times, misses an important task, or does not respond after reminders, mark the task as needing caregiver support.

For caregivers, you may provide more detailed information, including:

* Tasks marked complete
* Missed tasks
* Delayed tasks
* Help requests
* Confusion flags
* Times of day when the patient struggles
* Activities the patient performs well or poorly on
* Suggestions for extra support or schedule changes

Use careful wording:

* Say “marked complete,” not “definitely completed,” unless verified.
* Say “may need help,” not “is confused,” unless confirmed by a caregiver.
* Say “caregiver review recommended” when unsure.

The system should collect routine data over time, including task completion, missed tasks, reminders needed, help requests, visual support used, confusion flags, time of day, day of week, task type, and performance score. This data should be used to help caregivers understand patterns and adjust care.

Never:

* Diagnose dementia or any medical condition.
* Give medical advice.
* Change medication instructions.
* Replace caregivers, doctors, or emergency services.
* Claim certainty when the data is uncertain.

Always prioritize:

* Simplicity
* Calm language
* Patient dignity
* Safety
* Caregiver awareness

For both interfaces, respond in the language that the user is using, unless the user requests a different language.
"""


# --------------------------------------------------
# WORD COUNT TOOL
# --------------------------------------------------

def word_count(text: str) -> str:
    """Count the number of words in some text."""

    words = text.split()
    count = len(words)

    return str(count)


# --------------------------------------------------
# TOOL DEFINITIONS
# --------------------------------------------------

TOOLS = [
    {
        "type": "web_search"
    },
    {
        "type": "function",
        "name": "word_count",
        "description": (
            "Count the number of words in text supplied by the user."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text whose words should be counted."
                }
            },
            "required": ["text"],
            "additionalProperties": False
        },
        "strict": True
    }
]


# --------------------------------------------------
# RUN CUSTOM TOOL
# --------------------------------------------------

def run_function(function_name: str, arguments: dict) -> str:
    """Run the custom function selected by the model."""

    if function_name == "word_count":
        text = arguments.get("text", "")
        return word_count(text)

    return f"Error: Unknown function called: {function_name}"


# --------------------------------------------------
# GET AURA'S RESPONSE
# --------------------------------------------------

def get_AURA_response(
    user_message: str,
    previous_response_id: str | None
) -> tuple[str, str, list[str]]:
    """
    Send a message to AURA, run requested tools,
    and return the final answer, response ID, and tools used.
    """
    if client is None:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    request = {
        "model": AURA_PATIENT_MODEL,
        "instructions": SYSTEM_PROMPT,
        "input": user_message,
        "tools": TOOLS,
    }

    if previous_response_id is not None:
        request["previous_response_id"] = previous_response_id

    response = client.responses.create(**request)

    tools_used = []

    while True:
        function_outputs = []

        for item in response.output:
            if item.type == "web_search_call":
                if "Web Search" not in tools_used:
                    tools_used.append("Web Search")

            elif item.type == "function_call":
                function_name = item.name

                try:
                    arguments = json.loads(item.arguments)
                except json.JSONDecodeError:
                    arguments = {}

                result = run_function(
                    function_name=function_name,
                    arguments=arguments
                )

                if function_name == "word_count":
                    tools_used.append("Word Count")

                function_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result
                    }
                )

        if not function_outputs:
            return (
                localize_text(client, AURA_PATIENT_MODEL, response.output_text, user_message),
                response.id,
                tools_used,
            )

        response = client.responses.create(
            model=AURA_PATIENT_MODEL,
            instructions=SYSTEM_PROMPT,
            previous_response_id=response.id,
            input=function_outputs,
            tools=TOOLS,
        )


# --------------------------------------------------
# MAIN CHAT LOOP
# --------------------------------------------------

def main() -> None:
    if client is None:
        print("AURA cannot start chat because OPENAI_API_KEY is not configured.")
        return
    previous_response_id = None

    print("=" * 60)
    print("AURA - Here to Help with Daily Tasks")
    print("Tools available: Web Search and Word Count")
    print("Type 'clear' to clear conversation memory.")
    print("Type 'exit' to stop.")
    print("=" * 60)

    while True:
        user_message = input("\nYou: ").strip()

        if not user_message:
            continue

        if user_message.lower() in {"exit", "quit", "bye"}:
            print("\nAURA: Goodbye. Have a good day!")
            break

        if user_message.lower() == "clear":
            previous_response_id = None
            print("\nAURA: Conversation memory cleared.")
            continue

        try:
            answer, previous_response_id, tools_used = (
                get_AURA_response(
                    user_message=user_message,
                    previous_response_id=previous_response_id,
                )
            )

            if tools_used:
                print(f"\n[Tool used: {', '.join(tools_used)}]")
            else:
                print("\n[Tool used: None]")

            print(f"\nAURA: {answer}")

        except KeyboardInterrupt:
            print("\n\nAURA: Goodbye. Have a good day!")
            break

        except Exception as error:
            print("\nAURA: Sorry, something went wrong.")
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
