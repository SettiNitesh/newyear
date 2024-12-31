import streamlit as st
import pywhatkit as kit
import re

def validate_indian_number(number):
    """Validate if the number is an Indian mobile number."""
    pattern = r'^(\+91|91)?[6-9]\d{9}$'
    return bool(re.match(pattern, number))

def format_indian_number(number):
    """Ensure the phone number is in the correct format with +91."""
    if not number.startswith("+91"):
        if number.startswith("91"):
            number = "+" + number
        else:
            number = "+91" + number
    return number

def send_wishes(phone_number, message):
    """Send New Year wishes to the given phone number."""
    try:
        if not validate_indian_number(phone_number):
            st.error(f"Invalid Indian phone number: {phone_number}")
            return False

        phone_number = format_indian_number(phone_number)

        kit.sendwhatmsg_instantly(
            phone_no=phone_number,
            message=message,
            wait_time=10,
            tab_close=True,
            close_time=3
        )
        return True
    except Exception as e:
        st.error(f"Failed to send message to {phone_number}. Error: {str(e)}")
        return False

def main():
    st.title("New Year Wishes Sender")

    # Input fields for phone numbers and the message
    phone_numbers = st.text_area("Enter Indian phone numbers (one per line):", height=150)
    default_message = (
        "🎉✨ **Happy New Year 2025!** 🎆🎊\n\n"
        "🌟 May this year bring you:\n"
        "💖 Endless joy, 🏆 Great success, and 🌈 New opportunities!\n\n"
        "Let’s step into 2025 with:\n"
        "💪 Hope, 😊 Positivity, and 🙏 A heart full of gratitude.\n\n"
        "🎁 Wishing you and your loved ones:\n"
        "🌻 Health, 🥳 Happiness, and 💰 Prosperity!\n\n"
        "🥂 Cheers to new beginnings and brighter days ahead! 🎇🎉"
    )
    message = st.text_area("Enter your New Year message:", default_message)

    progress = st.empty()

    if st.button("Send Wishes"):
        if not all([phone_numbers.strip(), message.strip()]):
            st.error("All fields are required.")
            return

        numbers = [num.strip() for num in phone_numbers.strip().splitlines() if num.strip()]
        total = len(numbers)

        # Loop through each number and send the message
        for idx, number in enumerate(numbers, 1):
            progress.text(f"Processing {idx}/{total}: {number}")
            success = send_wishes(number, message)
            if success:
                st.success(f"✓ Sent to {number}")

if __name__ == "__main__":
    main()
