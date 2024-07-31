import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime



# Load environment variables from .env file
load_dotenv()

# sheety api url 
API_URL="https://api.sheety.co/0b40bafaac4d523f657005ace243791b/cleintsInventory/sheet1"

# fetching api data 
def fetch_data():
    global inventory_list
    response= requests.get(API_URL)
    if response.status_code==200:
        # api response 
        data= response.json()
        inventory_list=data.get("sheet1",[])
        return inventory_list        
    
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    
# gmail send from this fun 
def GmailSend(ToEmail,FromEmail,Message,Subject):
    msg=MIMEMultipart()
    msg["From"]=FromEmail
    msg["To"]=ToEmail
    msg["Subject"]=Subject
    body=Message

    msg.attach(MIMEText(body, 'html'))
    try:
        # Connect to SMTP server
        mail_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mail_server.ehlo()
        
        # Login to SMTP server
        mail_server.login(FromEmail, os.getenv("EMAIL_PASSWORD"))
        
        # Send email message
        mail_server.send_message(msg)
        
        # Quit SMTP server
        mail_server.quit()
        
        print(f"Mail sent to {ToEmail} successfully")
    except Exception as e:
        print(f"Error occurred while sending email to {ToEmail}: {e}")


     

# My email coming from .env file  
fromEmail = os.getenv("FROM_EMAIL")






# invoice send on email 
def Invoice_send(item):
      subject = "Order Invoice By CoderzSnippets"
      if item["orderGiven"]:
            end_date_str = item["workEndExpected"]

            try:
                work_end_date = datetime.strptime(end_date_str, '%m/%d/%Y').strftime('%m/%d/%Y')
            except ValueError:
                print(f"Invalid date format for {item['clientName']}: {end_date_str}")
                
                

            if work_end_date == current_date_str:
              
                email = item["clientEmailAddress"]
                id = item["id"]
                end = item["workEndExpected"]
                web_name = item["orderDescription"]
                total = item["totalPayment (pkr)"] - item["advancedPayment (pkr)"]

                # Tax rate (0.8%)
                tax_rate = 0.008

                # Calculate tax
                tax = total * tax_rate
                tax_total = total + tax

                # Prepare HTML email template
                html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f4;
        }}
        .invoice {{
            width: 100%;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .invoice-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .invoice-header-left img {{
            width: 150px;
        }}
        .invoice-header-left h1 {{
            margin: 0;
            font-size: 24px;
            color: #333333;
        }}
        .invoice-header-left p {{
            margin: 5px 0;
            color: #666666;
        }}
        .invoice-header-right {{
            text-align: right;
        }}
        .invoice-header-right h2 {{
            margin: 0;
            font-size: 28px;
            color: #E64A19;
        }}
        .invoice-header-right p {{
            margin: 5px 0;
            color: #666666;
        }}
        .invoice-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        .invoice-table th,
        .invoice-table td {{
            border: 1px solid #000;
            padding: 10px;
            text-align: center;
        }}
        .invoice-table th {{
            background-color: #E64A19;
            color: #fff;
            font-weight: bold;
        }}
        .invoice-total {{
            text-align: right;
            margin-top: 20px;
        }}
        .invoice-total p {{
            margin: 5px 0;
            font-size: 16px;
            color: #333333;
        }}
        .invoice-footer {{
            text-align: center;
            padding-top: 20px;
            color: #999999;
            font-size: 14px;
        }}
        .invoice-footer a {{
            color: #999999;
            text-decoration: none;
        }}
        .invoice-footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="invoice">
        <div class="invoice-header">
            <div class="invoice-header-left">
                <img src="https://img.icons8.com/?size=256&id=FJJcVgL6wWOP&format=png" alt="Company Logo">
                <h1>CODERZ SNIPPETS</h1>
                <p>Banoqabil Student Karachi</p>
                <p>Email: {fromEmail}</p>
                <p>Phone: 03120372325</p>
            </div>
            <div class="invoice-header-right">
                <h2>Invoice</h2>
                <p>Invoice Number: #{id}</p>
                <p>Date: {end}</p>
            </div>
        </div>
        <table class="invoice-table">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                    <th>Total Pages</th>
                    <th>Advanced Payment</th>
                    <th>Unit Price</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{web_name}</td>
                    <td>1</td>
                    <td>{item["numberOfPages"]}</td>
                    <td>{item["advancedPayment (pkr)"]}</td>
                    <td>{item["totalPayment (pkr)"]}</td>
                    <td>{total}</td>
                </tr>
            </tbody>
        </table>
        <div class="invoice-total">
            <p>Subtotal: {total}</p>
            <p>Tax (0.8%): {tax}</p>
            <p>Total: {tax_total}</p>
        </div>
        <div class="invoice-footer">
            <p>Thank you for your support</p>
        </div>
    </div>
</body>
</html>
"""
                GmailSend("upwork8000@gmail.com", fromEmail, html_template, subject)
                print(f"Email sent to {item['clientName']}")
# follow up send on email 
def follow_up(item):
    subject = "Follow up Message bu coderz snippets"
    current_date_str = datetime.now().strftime('%m/%d/%Y')

    client_desc_time = item.get("clientDecisionTime", "")

    try:
        client_end_time = datetime.strptime(client_desc_time, '%m/%d/%Y').strftime('%m/%d/%Y')
    except ValueError:
        print(f"Invalid date format for {item['clientName']}: {client_desc_time}")
        return  # Exit function if date format is invalid

    # Compare the formatted client decision time with current date
    if client_end_time == current_date_str:
                email = item["clientEmailAddress"]
               
                name = item["clientName"]
                
                html_template =f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #de330c;
            color: #ffffff;
            width:100vw;
            height:100vh;
            text-decoration:none;
        }}
        .container {{
            width: 80%;
            margin: auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #e26c50;
            color:white;
        }}
        .header {{
            text-align: center;
        }}
        .logo {{
            width: 150px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://img.icons8.com/?size=256&id=FJJcVgL6wWOP&format=png" alt="Company Logo" class="logo" />
        </div>
        <h2>Hello {name},</h2>
        <p>I hope this message finds you well.</p>
        <p>Just following up regarding our website development project. As per our records, you took action on {item["clientDecisionTime"]}. We understand that website creation can be a time-consuming process, and we're here to support you every step of the way.</p>
        <p>Please let us know if you need any further assistance or have any questions. We look forward to your response and are eager to continue working with you.</p>
        <p>Best regards,<br/>
        Abdul Rafay<br/>
        Email: {fromEmail}<br/>
        Phone: 0312-0372325</p>
    </div>
    <div class="footer">
        <p>Thank you for choosing our website development services!</p>
    </div>
</body>
</html>
"""
                GmailSend(email, fromEmail, html_template, subject)
                print(f"Email sent to {item['clientName']}")



if __name__ == "__main__":
    inventory = fetch_data()
  #  loop to get data from sheety api call 
    for item in inventory:
        Invoice_send(item)
        follow_up(item)
       
        