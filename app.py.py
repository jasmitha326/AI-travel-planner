import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AI Travel Planning Agent")
st.write(
    "Plan your next trip with a personalized AI-generated itinerary."
)

with st.form("travel_form"):
    destination = st.text_input(
        "Where do you want to travel?",
        placeholder="Example: Gokarna, Goa, Hyderabad"
    )

    col1, col2 = st.columns(2)

    with col1:
        days = st.number_input(
            "Number of days",
            min_value=1,
            max_value=30,
            value=3
        )

        budget = st.number_input(
            "Total budget (INR)",
            min_value=500,
            value=10000,
            step=500
        )

    with col2:
        travelers = st.number_input(
            "Number of travelers",
            min_value=1,
            max_value=20,
            value=2
        )

        travel_style = st.selectbox(
            "Travel interests",
            [
                "Beaches and relaxation",
                "Temples and culture",
                "Adventure and nature",
                "Food and shopping",
                "History and sightseeing",
                "A mixture of everything"
            ]
        )

    transport = st.selectbox(
        "Preferred transport",
        ["Public transport", "Car or taxi", "Two-wheeler", "Not decided"]
    )

    submitted = st.form_submit_button(
        "Generate My Travel Plan",
        type="primary"
    )

if submitted:
    if not destination.strip():
        st.warning("Please enter a destination.")
    elif not os.getenv("GEMINI_API_KEY"):
        st.error(
            "AI API key is missing. Add GEMINI_API_KEY "
            "to your environment variables."
        )
    else:
        prompt = f"""
        You are a helpful AI travel planning assistant.

        Create a practical travel itinerary using these details:
        Destination: {destination}
        Duration: {days} days
        Total group budget: INR {budget}
        Number of travelers: {travelers}
        Interests: {travel_style}
        Transport preference: {transport}

        Include:
        1. A day-by-day itinerary with morning, afternoon and evening.
        2. Suggested places and activities.
        3. An estimated budget breakdown in Indian rupees.
        4. Food and local transport suggestions.
        5. Useful packing and safety tips.
        6. Ways to save money.

        Make sure estimated costs fit the group budget where possible.
        State assumptions and explain if the budget may be insufficient.
        Do not invent live prices, opening hours or bookings.
        Mention that travelers should verify current details.
        Format the answer using clear headings and bullet points.
        """

        try:
            with st.spinner("Your AI agent is planning your trip..."):
                client = genai.Client(
                    api_key=os.environ["GEMINI_API_KEY"]
                )

                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt
                )

            st.subheader(f"Your trip to {destination}")
            st.markdown(response.text)

        except Exception as e:
            st.error(
                "The AI request failed. Check your API key, "
                "model availability, quota and connection."
            )
            st.caption(f"Technical details: {e}")

st.divider()
st.caption(
    "AI-generated estimates are for planning only. "
    "Verify prices, transport and opening hours before traveling."
)
