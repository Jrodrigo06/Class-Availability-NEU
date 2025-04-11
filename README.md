# Web Scraper for Classes

A Python-based web scraper that checks availability of seats in a class at Northeastern University and sends email notifications when seats become available.

## Description

This project scrapes the Northeastern University course page for a specific class and checks if there are any available seats. If seats are available, it sends an email notification to a preconfigured email address.

## Installation

### Prerequisites:
- Python 3.8 or higher
- An active Gmail account (for email notifications)

### Steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/web-scraper-for-classes.git
    ```

2. Navigate into the project directory:
    ```bash
    cd web-scraper-for-classes
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    source venv/bin/activate  # macOS/Linux
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Create a `.env` file to store your email credentials:
    ```plaintext
    EMAIL_SUBJECT="Class Availability Notification"
    EMAIL_FROM="your-email@gmail.com"
    EMAIL_PASSWORD="your-email-password"
    EMAIL_TO="receiver-email@example.com"
    ```

## Usage

1. Run the script to start checking for seat availability:
    ```bash
    python script2.py
    ```

2. The script will run indefinitely, checking for seat availability and sending email notifications when seats are available.
