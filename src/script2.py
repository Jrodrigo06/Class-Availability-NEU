import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
# Load environment variables from .env file
import logging
from datetime import datetime

load_dotenv()
# Load environment variables from .env file
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
# Check if environment variables are loaded correctly

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("class_monitor.log"), logging.StreamHandler()]
)

# Configuration
URL = "https://bnrordsp.neu.edu/ssb-prod/bwckschd.p_disp_listcrse?term_in=202610&subj_in=MATH&crse_in=2341&crn_in=10359"
CHECK_INTERVAL = 15  # seconds (1 minute)



def send_email_notification(seats_available):
    """Send email notification that the class has available seats."""
    try:
        msg = EmailMessage()
        msg.set_content(f"MATH 2341 class now has {seats_available} seats available.")
        
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logging.info(f"Email notification sent successfully! {seats_available} seats available.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def check_class_availability():
    """Check if the class has available seats by parsing the Northeastern course page."""
    try:
        # Simulate a browser user-agent to avoid being blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Raise an exception for  errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Based on the HTML structure, find the table with meeting times
        # This table contains the "Remaining Seats" column
        meeting_tables = soup.find_all('table', class_='datadisplaytable', summary=lambda s: s and 'scheduled meeting times' in s.lower())
        
        if not meeting_tables:
            logging.warning("Could not find the meeting times table")
            return False
        
        meeting_table = meeting_tables[0]
        
        # Find the header row and locate the "Remaining Seats" column
        headers = meeting_table.find_all('th', class_='ddheader')
        header_texts = [header.text.strip() for header in headers]
        
        # Check if "Remaining Seats" is in the headers
        if "Remaining Seats" not in header_texts:
            logging.warning(f"Could not find 'Remaining Seats' column. Available headers: {header_texts}")
            return False
        
        remaining_index = header_texts.index("Remaining Seats")
        
        # Find all data rows
        rows = meeting_table.find_all('tr')
        
        # Skip the header row (first row)

        cells = rows[1].find_all('td', class_='dddefault')
            
        if remaining_index < len(cells):
                remaining_seats_text = cells[remaining_index].text.strip()
                
                try:
                    remaining_seats = int(remaining_seats_text)
                    logging.info(f"Check completed: {remaining_seats} seats remaining")
                    
                    if remaining_seats > 0:
                        send_email_notification(remaining_seats)
                        return True
                    return False
                except ValueError:
                    logging.error(f"Could not convert '{remaining_seats_text}' to integer")
        
        logging.warning("No data rows found in the meeting times table")
        return False
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False

def main():
    
    notification_sent = False
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"Checking at {current_time}...")
            
            seats_available = check_class_availability()
            
            if seats_available and not notification_sent:
                notification_sent = True
                logging.info("Class is available! Notification sent.")
            elif seats_available and notification_sent:
                logging.info("Class is still available. Notification already sent.")
            elif not seats_available:
                notification_sent = False  # Reset if seats become unavailable again
                logging.info("Class is still full.")
            
            # Sleep until next check
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logging.info("Monitoring stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            # Still sleep before retry
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()