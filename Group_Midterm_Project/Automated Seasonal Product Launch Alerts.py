import requests
import smtplib
from datetime import datetime
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

# SHEETY_CUSTOMERS_SHEET="https://api.sheety.co/0b40bafaac4d523f657005ace243791b/untitledSpreadsheet/sheet1"
SHEETY_TEREND_SHEET = "https://api.sheety.co/0b40bafaac4d523f657005ace243791b/seasonalProductLaunch/sheet1"


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "abdulrafaydev100@gmail.com"


def fetch_data_from_sheety():
    response = requests.get(url=SHEETY_TEREND_SHEET)
    data = response.json()
    return data["sheet1"]




   

# print(fetch_data_from_sheety())

def analyze_trends(data):
         current_season = get_current_season()
         filterd_trend=[]
         for trend in data:
             if trend['season']==current_season:
                 filterd_trend.append(trend)
         return filterd_trend

# Function to get the current season
def get_current_season():
    current_month = datetime.now().month
    if current_month in [12, 1, 2]:
        return "Winter"
    elif current_month in [3, 4, 5]:
        return "Spring"
    elif current_month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"  
    


# def create_email_template(trend):
    subject = f"{trend['season']} is here! New arrivals and special offers:"
    # message = f"{trend['season']} is here! Check out our new arrivals and special offers: {', '.join([product['name'] for product in json.loads(trend['products'])])},\nThis is link of product to buy easy: {', '.join([product['link'] for product in json.loads(trend['products'])])}"
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seasonal Product Launch</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }}
        .container {{
            width: 80%;
            margin: auto;
            overflow: hidden;
        }}
        header {{
            background: #333;
            color: #fff;
            padding: 1rem 0;
            text-align: center;
        }}
        header nav ul {{
            list-style: none;
        }}
        header nav ul li {{
            display: inline;
            margin: 0 10px;
        }}
        header nav ul li a {{
            color: #fff;
            text-decoration: none;
        }}
        .hero {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 2rem 0;
            background: #f4f4f4;
        }}
        .hero-content {{
            flex: 1;
        }}
        .hero-content h2 {{
            font-size: 2rem;
            margin-bottom: 1rem;
        }}
        .hero-content p {{
            margin-bottom: 1rem;
        }}
        .hero-content .btn {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #333;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
        }}
        .hero-image {{
            flex: 1;
        }}
        .hero-image img {{
            max-width: 100%;
            height: auto;
        }}
        .features {{
            padding: 2rem 0;
        }}
        .features h2 {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        .feature-list {{
            display: flex;
            justify-content: space-around;
        }}
        .feature-item {{
            flex: 1;
            margin: 0 1rem;
            text-align: center;
        }}
        footer {{
            background: #333;
            color: #fff;
            text-align: center;
            padding: 1rem 0;
            margin-top: 2rem;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Seasonal Product Launch</h1>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#features">Features</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    <section id="home" class="hero">
        <div class="container">
            <div class="hero-content">
                <h2>Introducing Our Latest Product</h2>
                <p>Experience the best of the season with our new, innovative product. Designed to bring joy and convenience to your life.</p>
                <a href="#features" class="btn">Learn More</a>
            </div>
            <div class="hero-image">
                <img src="product-image.jpg" alt="Product Image">
            </div>
        </div>
    </section>
    <section id="features" class="features">
        <div class="container">
            <h2>Product Features</h2>
            <div class="feature-list">
                <div class="feature-item">
                    <h3>Feature One</h3>
                    <p>Description of feature one.</p>
                </div>
                <div class="feature-item">
                    <h3>Feature Two</h3>
                    <p>Description of feature two.</p>
                </div>
                <div class="feature-item">
                    <h3>Feature Three</h3>
                    <p>Description of feature three.</p>
                </div>
            </div>
        </div>
    </section>
    <footer>
        <div class="container">
            <p>&copy; 2024 Seasonal Product Launch. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
"""


    
    return subject, html_content

def send_email(ToEmail,FromEmail,Message,Subject):
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



def main():
    data = fetch_data_from_sheety()
    # print(data["email"][0])
    trends = analyze_trends(data)
    subject=None
    message=None
    seasonal_trends=None
    for trend in trends:
         seasonal_trends=trend
         print(seasonal_trends)
    season=seasonal_trends["season"]
    seasonal_prodcut=seasonal_trends["seasonalProduct"]
    product_image_url=seasonal_trends["productImage"]
    link=seasonal_trends["webLink"]

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seasonal Product Launch</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f9f9f9;
        }}
        .container {{
            width: 90%;
            max-width: 1200px;
            margin: auto;
            overflow: hidden;
        }}
        header {{
            background: #f09f00;
            color: #fff;
            padding: 1rem 0;
            text-align: center;
        }}
        header h1 {{
            margin: 0;
            font-size: 2rem;
        }}
        .hero {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            padding: 2rem 0;
            background: #ffffff;
            border-bottom: 2px solid #f09f00;
        }}
        .hero-content {{
            flex: 1;
            padding: 0 1rem;
        }}
        .hero-content h2 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #f09f00;
        }}
        .hero-content p {{
            margin-bottom: 1.5rem;
            font-size: 1.1rem;
        }}
        .hero-content .btn {{
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: #f09f00;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            font-size: 1rem;
            transition: background 0.3s;
            margin-bottom:3vw;
        }}
        .hero-content .btn:hover {{
            background: #d88e00;
        }}
        .hero-image {{
            flex: 1;
            padding: 0 1rem;
        }}
        .hero-image img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .features {{
            padding: 2rem 0;
            background: #ffffff;
        }}
        .features h2 {{
            text-align: center;
            margin-bottom: 2rem;
            color: #f09f00;
            font-size: 2rem;
        }}
        .feature-list {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            gap: 1rem;
        }}
        .feature-item {{
            flex: 1;
            margin: 0 1rem;
            text-align: center;
            background: #f4f4f4;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .feature-item h3 {{
            margin-bottom: 1rem;
            color: #f09f00;
        }}
        .feature-item p {{
            margin-bottom: 0;
        }}
        footer {{
            background: #f09f00;
            color: #fff;
            text-align: center;
            padding: 1rem 0;
            margin-top: 2rem;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Seasonal Product Launch</h1>
        </div>
    </header>
    <section id="home" class="hero">
        <div class="container">
            <div class="hero-content">
                <h2>Transform Your Moments with Our Latest Innovation!</h2>
                <p>Season: {season}</p>
                <a href="{link}" class="btn">Learn More</a>
            </div>
            <div class="hero-image">
                <img src="{product_image_url}" alt="Product Image">
            </div>
        </div>
    </section>
  
    <footer>
        <div class="container">
            <p>&copy; 2024 Seasonal Product Launch. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
"""


    subject="Seasonal Product Launch "
         
    for i in data:
            send_email(i["email"],GMAIL_USER,html_content,subject)
            # email=i['email']
            # print(f"mail send to {email}")

if __name__ == "__main__":
    main()
