import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
API_KEY = "demo-retail-key"
HEADERS = {"X-API-Key": API_KEY}

st.set_page_config(
    page_title="Smart Retail AI",
    page_icon="🛍️",
    layout="wide",
)

st.title("🛍️ Smart Retail & Customer Intelligence Platform")
st.write(
    "AI-powered product classification, face recognition, "
    "sentiment analysis, and customer support."
)

product_tab, face_tab, sentiment_tab, chatbot_tab, dashboard_tab = st.tabs(
    [
        "Product Classifier",
        "Face Recognition",
        "Sentiment Analysis",
        "Chatbot",
        "Dashboard",
    ]
)


def upload_image(endpoint, image_file):
    files = {
        "file": (
            image_file.name,
            image_file.getvalue(),
            image_file.type,
        )
    }

    response = requests.post(
        f"{API_URL}{endpoint}",
        files=files,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


with product_tab:
    st.header("Product Image Classification")

    product_image = st.file_uploader(
        "Upload a product image",
        type=["jpg", "jpeg", "png"],
        key="product_image",
    )

    if product_image and st.button("Classify Product"):
        st.image(product_image, width=250)

        try:
            result = upload_image("/classify-product", product_image)
            st.success(f"Predicted category: {result['category']}")
            st.metric("Confidence", f"{result['confidence'] * 100:.2f}%")
        except requests.RequestException as error:
            st.error(f"Could not contact the backend: {error}")


with face_tab:
    st.header("Customer Face Recognition")

    face_image = st.file_uploader(
        "Upload a customer face image",
        type=["jpg", "jpeg", "png"],
        key="face_image",
    )

    if face_image and st.button("Recognize Customer"):
        st.image(face_image, width=250)

        try:
            result = upload_image("/recognize-face", face_image)

            if result["status"] == "returning_customer":
                st.success(f"Returning customer: {result['customer_id']}")
            else:
                st.warning("Unknown customer")

            st.metric("Match distance", result["distance"])
        except requests.RequestException as error:
            st.error(f"Could not contact the backend: {error}")


with sentiment_tab:
    st.header("Customer Review Sentiment")

    review_text = st.text_area(
        "Enter a customer review",
        placeholder="The delivery was fast and the product is excellent.",
    )

    if st.button("Analyze Sentiment"):
        if not review_text.strip():
            st.warning("Please enter a review first.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/analyze-sentiment",
                    json={"text": review_text},
                    headers=HEADERS,
                    timeout=30,
                )
                response.raise_for_status()
                result = response.json()

                st.success(f"Sentiment: {result['sentiment'].title()}")
                st.metric("Confidence", f"{result['confidence'] * 100:.2f}%")
            except requests.RequestException as error:
                st.error(f"Could not contact the backend: {error}")


with chatbot_tab:
    st.header("Retail Support Chatbot")

    message = st.text_input(
        "Ask a question",
        placeholder="What are your store hours?",
    )

    if st.button("Send Message"):
        if not message.strip():
            st.warning("Please enter a message first.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/chatbot",
                    json={"message": message},
                    headers=HEADERS,
                    timeout=30,
                )
                response.raise_for_status()
                result = response.json()

                st.info(result["reply"])
                st.caption(
                    f"Intent: {result['intent']} | "
                    f"Confidence: {result['confidence'] * 100:.2f}%"
                )
            except requests.RequestException as error:
                st.error(f"Could not contact the backend: {error}")


with dashboard_tab:
    st.header("Retail Intelligence Dashboard")

    if st.button("Refresh Dashboard"):
        try:
            response = requests.get(
                f"{API_URL}/dashboard/stats",
                headers=HEADERS,
                timeout=30,
            )
            response.raise_for_status()
            stats = response.json()

            first_column, second_column, third_column = st.columns(3)
            first_column.metric("Total Visits", stats["total_visits"])
            second_column.metric(
                "Returning Customers",
                stats["returning_customers"],
            )
            third_column.metric("Unknown Visitors", stats["unknown_visits"])

            st.subheader("Sentiment Results")
            sentiment_data = pd.DataFrame(
                list(stats["sentiment_counts"].items()),
                columns=["Sentiment", "Count"],
            )

            if sentiment_data.empty:
                st.info("No sentiment results yet.")
            else:
                st.bar_chart(sentiment_data.set_index("Sentiment"))

            st.subheader("Chatbot Requests")
            chatbot_data = pd.DataFrame(
                list(stats["chats_by_intent"].items()),
                columns=["Intent", "Count"],
            )

            if chatbot_data.empty:
                st.info("No chatbot messages yet.")
            else:
                st.bar_chart(chatbot_data.set_index("Intent"))
        except requests.RequestException as error:
            st.error(f"Could not contact the backend: {error}")