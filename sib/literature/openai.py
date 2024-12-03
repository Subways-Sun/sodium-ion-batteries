"""Module using OpenAI API to classify literature."""

from openai import OpenAI
client = OpenAI()

def classify(openai_model, user_message):
    """Function to chat with the AI"""
    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": "You are a scientific paper classifier. Your task is to classify the given abstract of a scientific paper into one of the following categories: 'relevant cathode', 'relevant anode', 'relevant cathode anode', or 'irrelevant'. The classification is based on whether the abstract is relevant to the field of sodium ion battery electrodes, and if so, whether it discusses cathode, anode, or both. If the abstract is unrelated to the field, or contains only the synthesis of materials but not their performance, or is a review article, classify it as 'irrelevant'. Do not include quotation marks in your response."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return completion.choices[0].message

# help me generate a system message for gpt-4o. Each user message is an abstract of a scientific paper. I need the model to classify the paper into "relevant", "irrelevant", "cathode", "anode", based on whether the given abstract is relevant to the field of sodium ion battery electrodes, and if so, does the abstract talk about cathode, anode, or both. The response message should be single words, for example, if an abstract is related to cathode, the response should be "relevant cathode", if related to anode, "relevant anode", if both, "relevant cathode anode", if the abstact is unrelated to the field, or it is a review article, "irrelevant". If the response is "irrelevant", there should't be any further classification of cathode or anode
