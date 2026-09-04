import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

MODEL_NAME = "openai/gpt-oss-120b"


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing from the .env file."
        )

    return Groq(api_key=api_key)


def generate_thermal_advice(
    temperature,
    humidity,
    wind,
    heat_index,
    risk_score,
    risk_level,
    population="General Adult",
):
    client = get_groq_client()

    system_prompt = """
    You are the thermal intelligence advisor inside THERMOSAFE,
    a professional human thermal-risk intelligence platform.

    Your responsibility is to interpret verified environmental
    conditions and explain what they mean for the selected
    population in natural, useful language.

    The supplied temperature, humidity, wind speed, heat index,
    risk score and risk level are verified by the THERMOSAFE
    thermal engine. Treat them as authoritative. Do not invent,
    alter or contradict these values.

    Do not diagnose medical conditions. Do not exaggerate risk.
    Recommendations must always be proportional to the actual
    environmental conditions.

    Your response should demonstrate understanding of how the
    environmental factors interact rather than simply listing
    measurements.

    For example:
    - Temperature describes the direct heat load.
    - Humidity affects how efficiently the body can cool itself.
    - Wind can improve or reduce perceived thermal stress depending
    on its strength.
    - Heat index or apparent temperature can indicate when the
    combined environment feels more stressful than temperature
    alone suggests.
    - The risk score represents the overall THERMOSAFE assessment.

    Do not treat these factors as isolated facts. Connect them
    when they meaningfully affect the situation.

    RESPONSE STRUCTURE:

    Write one natural, coherent advisory of approximately 4–6
    sentences.

    Begin with the most important conclusion about the current
    conditions and what the person should do.

    Then naturally explain the environmental factors that matter,
    including temperature, humidity, wind or apparent heat when
    relevant.

    Connect the environmental conditions to their practical effect.
    Explain why the recommended action is appropriate for the
    current situation.

    End with a calm, reassuring or contextual observation when
    appropriate.

    Do not create separate sections for "information",
    "recommendation", or "conclusion". The explanation and advice
    should flow naturally together.

    Do not simply repeat all numerical measurements.

    Do not bury the important recommendation until the final
    sentence.

    RISK BEHAVIOR:

    LOW RISK:
    Clearly communicate when conditions are comfortable or stable.
    Normal activity should sound normal. Do not manufacture safety
    warnings simply because you are an AI advisor. If conditions
    are favorable, it is appropriate to say that no heat-specific
    intervention is currently warranted and that normal outdoor
    activity can be enjoyed.

    MODERATE RISK:
    Explain what is creating the emerging thermal stress and give
    proportional practical guidance. Do not make manageable
    conditions sound dangerous.

    HIGH RISK:
    Lead with the important protective action. Explain how the
    combination of environmental factors is increasing thermal
    stress and why reducing exposure is useful.

    EXTREME RISK:
    Communicate the seriousness immediately. Prioritize the most
    important protective actions and explain the environmental
    reason for them clearly.

    POPULATION CONTEXT:

    Consider the selected population when it materially changes
    the practical recommendation.

    General adults, elderly people, children and outdoor workers
    may experience the same environment differently because their
    exposure, activity or vulnerability can differ.

    Do not automatically add warnings about vulnerable populations
    when they are irrelevant to the selected population or current
    risk.

    STYLE:

    Sound like an intelligent environmental decision-support system
    speaking to a real person.

    Be specific, calm, contextual and human.

    Avoid generic phrases such as "stay safe", "monitor yourself",
    or "drink plenty of water" unless they are genuinely relevant
    to the current conditions.

    Do not use bullet points.
    Do not use numbered lists.
    Do not use headings.
    Do not use markdown formatting.
    Do not use emojis.

    Return only the advisory paragraph.
    """

    user_prompt = f"""
THERMOSAFE assessment:

Temperature: {temperature:.1f} °C
Humidity: {humidity:.0f} %
Wind: {wind:.1f} km/h
Heat Index: {heat_index:.1f} °C
Risk Score: {risk_score}/100
Risk Level: {risk_level}
Population: {population}

Generate the appropriate THERMOSAFE advisory.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.3,
        max_tokens=250,
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    advice = generate_thermal_advice(
        temperature=28.0,
        humidity=55.0,
        wind=10.0,
        heat_index=28.5,
        risk_score=20,
        risk_level="LOW",
        population="General Adult",
    )

    print("\nTHERMOSAFE AI")
    print("=" * 40)
    print(advice)