import smtplib
from tabulate import tabulate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import psycopg2
import datetime
import pytz

# Get the current time in the Pacific Time Zone (PST/PDT)
timezone = pytz.timezone('US/Pacific')
current_time = datetime.datetime.now(timezone)

# Get the current date and date one day before the current date
current_date = current_time.strftime('%A, %B %d')
yesterday_date = (current_time - datetime.timedelta(days=1)).strftime('%A, %B %d')

DATABASE_URL = "postgres://eczvjchosxwpcs:96191a4fb8fc12e2fce2ec7315115b4b634614653acbb6f481d6a4a8d2170192@ec2-100-26-39-41.compute-1.amazonaws.com:5432/dfkh38d1dqeie4"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cur = conn.cursor()
cur.execute("SELECT '(' || SUBSTRING(user_identifier FROM 3 FOR 3) || ') ' || SUBSTRING(user_identifier FROM 6 FOR 3) || '-' || SUBSTRING(user_identifier FROM 9 FOR 4) AS user_identifier, user_message, bot_message, TO_CHAR(created_at, 'MM/DD/YYYY') AS created_at FROM public.customer_dialogue_tb WHERE created_at >= NOW() - INTERVAL '24 hours';")
daily_res = cur.fetchall()
cur.close()
dailyCount = len(daily_res)

#Weekly
weekly = conn.cursor()
weekly.execute("SELECT '(' || SUBSTRING(user_identifier FROM 3 FOR 3) || ') ' || SUBSTRING(user_identifier FROM 6 FOR 3) || '-' || SUBSTRING(user_identifier FROM 9 FOR 4) AS user_identifier, user_message, bot_message FROM public.customer_dialogue_tb WHERE created_at >= date_trunc('week', CURRENT_DATE) AND created_at < date_trunc('week', CURRENT_DATE) + INTERVAL '1 week';")
details_res = weekly.fetchall()
weekly.close()
weeklyCount = len(details_res)

#Monthly
monthly = conn.cursor()
monthly.execute("SELECT '(' || SUBSTRING(user_identifier FROM 3 FOR 3) || ') ' || SUBSTRING(user_identifier FROM 6 FOR 3) || '-' || SUBSTRING(user_identifier FROM 9 FOR 4) AS user_identifier, user_message, bot_message, TO_CHAR(created_at, 'MM/DD/YYYY') AS created_at FROM public.customer_dialogue_tb WHERE created_at >= date_trunc('month', CURRENT_DATE) AND created_at < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month';")
monthly_res = monthly.fetchall()
monthly.close()
monthlyCount = len(monthly_res)
conn.close()


message_rows = {}
for row in daily_res:
    phone_number = row[0]
    customer_message = row[1]
    bot_message = row[2]
    created_date = row[3]

    if phone_number not in message_rows:
        message_rows[phone_number] = []

    message_rows[phone_number].append([customer_message, bot_message,created_date])

#SEND SMS
account_sid = 'AC416bfb8094e2df7da7971e277b5ff764'
auth_token = '22e9cbc7691ae507e6f54c2a9f73731f'
client = Client(account_sid, auth_token)
message_body = f"{current_date}\nDaily Sam's performance\n\nMessages: {dailyCount}\nWeekly Total: {weeklyCount}\nMonthly Total: {monthlyCount}\n\nInteractions\n"

#SEND EMAIL
sender_email = "ssamthemessenger@gmail.com"
to_emails = ["ssamthemessenger@gmail.com"]
cc_emails = ["mohammadhuzaifa72@gmail.com"]
password = "kqtozidepgzdpobb"

HTML = """ 
<!DOCTYPE html>
<html>
<head>
        <title>Daily sSam's performance</title>
        <meta content="summary_large_image" name="twitter:card" />
        <meta content="website" property="og:type" />
        <meta content="" property="og:description" />
        <meta content="" property="og:title" />
        <meta content="" name="description" />
        <meta charset="utf-8" />
        <meta content="width=device-width" name="viewport" />
        <link href="https://fonts.googleapis.com/css?family=Oswald" rel="stylesheet" type="text/css" />
        <style>
            .bee-row-1 .bee-col-1 .bee-block-1,
            .bee-row-2 .bee-col-1,
            .bee-row-2 .bee-col-1 .bee-block-1,
            .bee-row-2 .bee-col-1 .bee-block-5,
            .bee-row-7 .bee-col-1 .bee-block-1 {{
                padding: 10px;
            }}

            .bee-row-1 .bee-col-1,
            .bee-row-2 .bee-col-1,
            .bee-row-2 .bee-col-2,
            .bee-row-3 .bee-col-1,
            .bee-row-4 .bee-col-1,
            .bee-row-4 .bee-col-2,
            .bee-row-5 .bee-col-1,
            .bee-row-6 .bee-col-1,
            .bee-row-7 .bee-col-1 {{
                border-bottom: 0 solid transparent;
                border-left: 0 solid transparent;
                border-right: 0 solid transparent;
                border-top: 0 solid transparent;
            }}

            .bee-html-block {{
                text-align: center;
                position: relative;
            }}

            .bee-row-1,
            .bee-row-1 .bee-row-content,
            .bee-row-2,
            .bee-row-2 .bee-row-content,
            .bee-row-3,
            .bee-row-4,
            .bee-row-5,
            .bee-row-6,
            .bee-row-7,
            .bee-row-7 .bee-row-content {{
                background-repeat: no-repeat;
            }}

            body {{
                background-color: #ecfbff;
                color: #000;
                font-family: Oswald, Arial, Helvetica Neue, Helvetica, sans-serif;
            }}

            a {{
                color: #0068a5;
            }}

            .bee-row-2 .bee-row-content {{
                background-color: #143059;
            }}

            .bee-row-2 .bee-col-1 .bee-block-2,
            .bee-row-2 .bee-col-1 .bee-block-4 {{
                padding-left: 20px;
            }}

            .bee-row-2 .bee-col-1 .bee-block-3 {{
                padding-bottom: 10px;
                padding-left: 10px;
                padding-right: 10px;
            }}

            .bee-row-2 .bee-col-2 {{
                padding-bottom: 5px;
                padding-top: 5px;
            }}

            .bee-row-2 .bee-col-2 .bee-block-1,
            .bee-row-2 .bee-col-2 .bee-block-4 {{
                padding: 5px;
            }}

            .bee-row-2 .bee-col-2 .bee-block-2 {{
                padding: 20px;
            }}

            .bee-row-2 .bee-col-2 .bee-block-3 {{
                width: 100%;
                padding: 10px;
            }}

            .bee-row-3 .bee-row-content,
            .bee-row-4 .bee-row-content,
            .bee-row-5 .bee-row-content,
            .bee-row-6 .bee-row-content {{
                background-color: #fff;
                background-repeat: no-repeat;
            }}

            .bee-row-3 .bee-col-1 {{
                padding: 5px;
            }}

            .bee-row-3 .bee-col-1 .bee-block-1 {{
                padding: 20px 30px 10px;
            }}

            .bee-row-4 .bee-col-1 {{
                padding: 5px;
                max-width: 200px;
            }}
            @media only screen and (min-device-width: 560px) {{
                .bee-row-4 .bee-col-1 {{
                    padding: 30px !important;
                }}
            }}
            @media (min-width: 560px) {{
                .bee-row-4 .bee-col-1 {{
                    padding: 30px !important;
                }}
            }}

            .bee-row-5 .bee-col-1 {{
                padding-left: 5px;
                padding-right: 5px;
            }}

            .bee-row-6 .bee-col-1 .bee-block-1 {{
                padding: 10px;
            }}

            * {{
                box-sizing: border-box;
            }}

            body,
            p {{
                margin: 0;
            }}

            .bee-desktop_hide {{
                display: none;
            }}

            .bee-row-content {{
                max-width: 540px;
                margin: 0 auto;
                display: flex;
                justify-content: center;
            }}

            .bee-row-content .bee-col-w6 {{
                flex: 6;
            }}

            .bee-row-content .bee-col-w12 {{
                flex: 12;
            }}

            .bee-image img {{
                display: block;
                width: 100%;
            }}

            .bee-divider,
            .bee-image {{
                overflow: auto;
            }}

            .bee-divider .bee-center,
            .bee-image .bee-center {{
                margin: 0 auto;
            }}

            .bee-text {{
                overflow-wrap: anywhere;
            }}

            @media only screen and (max-device-width: 560px) {{
                .bee-desktop_hide,
                .bee-row-content:not(.no_stack) {{
                    display: block;
                }}
            }}
            @media (max-width: 560px) {{
                .bee-desktop_hide,
                .bee-row-content:not(.no_stack) {{
                    display: block;
                }}
            }}

            .bee-performance-item {{
                padding: 0 10px 10px;
            }}
            @media only screen and (min-device-width: 560px) {{
                .bee-performance-item {{
                    padding: 0 26px 20px !important;
                }}
            }}
            @media (min-width: 560px) {{
                .bee-performance-item {{
                    padding: 0 26px 20px !important;
                }}
            }}
            .primary-label {{
				font-size: 24px;
				font-weight: bold;
				letter-spacing: 1.5px;
			}}
			.primary-label.large-label {{
				/*font-size: calc(40px - 0.5vw);*/
				font-size: 40px;
				margin-top: 10%;
				color: #29873f;
			}}
			.secondary-label {{
				font-size: 16px;
				position: absolute;
				width: 100%;
				text-align: center;
				bottom: 16%;
			}}

			@media only screen and (max-device-width: 480px) {{
				.primary-label {{
					font-size: unset !important;
				}}
				.primary-label.large-label {{
					font-size: 30px !important;
				}}
				.secondary-label {{
					font-size: 14px !important;
				}}
			}}

			@media only screen and (max-device-width: 320px) {{
				.primary-label {{
					font-size: unset;
				}}
				.primary-label.large-label {{
					font-size: 30px;
				}}
				.secondary-label {{
					font-size: 14px !important;
				}}
			}}
        </style>
    </head>
    <body>
        <div class="bee-page-container">
            <div class="bee-row bee-row-1">
                <div class="bee-row-content">
                    <div class="bee-col bee-col-1 bee-col-w12">
                        <div class="bee-block bee-block-1 bee-divider">
                            <div class="spacer" style="height: 0px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bee-row bee-row-2">
                <div class="bee-row-content no_stack">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; border: 0; max-width: 600px !important;">
                        <tr>
                            <td align="left" style="vertical-align: middle;">
                                <div class="bee-col bee-col-1 bee-col-w6">
                                    <div class="bee-block bee-block-1 bee-text">
                                        <div class="bee-text-content" style="font-size: 12px; line-height: 120%; color: #393d47; font-family: inherit;">
                                            <p style="font-size: 12px; line-height: 14px;"></p>
                                        </div>
                                    </div>
                                    <div class="bee-block bee-block-2 bee-text">
                                        <div class="bee-text-content" style="line-height: 120%; font-size: 12px; color: #ffffff; font-family: inherit;">
                                            <p style="font-size: 14px; line-height: 16px;">
                                                <span style="font-size: 24px; line-height: 40px;">
                                                    <span style="font-weight: bold; line-height: 14px;">
                                                        Daily sSam's  
                                                    </span>
                                                    <span style="font-size: 20px; line-height: 10px;">
                                                        Performance
                                                    </span>
                                                </span>
                                            </p>
                                        </div>
                                    </div>
                                    <div class="bee-block bee-block-3 bee-divider">
                                        <div class="spacer" style="height: 0px;"></div>
                                    </div>
                                    <!-- <div class="bee-block bee-block-4 bee-text">
                                        <div class="bee-text-content" style="line-height: 120%; font-size: 12px; color: #ffffff; font-family: inherit;">
                                            <p style="font-size: 14px; line-height: 16px; text-align: left;">
                                                <span style="font-size: 18px; line-height: 21px;">
                                                    
                                                </span>
                                            </p>
                                        </div>
                                    </div> -->
                                    <div class="bee-block bee-block-5 bee-text">
                                        <div class="bee-text-content" style="font-size: 12px; line-height: 120%; color: #393d47; font-family: inherit;">
                                            <p style="font-size: 12px; line-height: 14px;"></p>
                                        </div>
                                    </div>
                                </div>
                            </td>
                            <td align="right" style="vertical-align: middle;">
                                <div class="bee-col bee-col-2 bee-col-w6">
                                    <div class="bee-block bee-block-1 bee-divider">
                                        <div class="spacer" style="height: 0px;"></div>
                                    </div>
                                    <!-- <div class="bee-block bee-block-2 bee-divider bee-desktop_hide">
                                        <div class="spacer" style="height: 0px;"></div>
                                    </div> -->
                                    <div class="bee-block bee-block-3 bee-image">
                                        <img alt="GIFT: 30% OFF" class="bee-center bee-autowidth" src="https://ssam-service.s3.amazonaws.com/images/ssam-logo.png" style="max-width: 150px;" />
                                    </div>
                                    <div class="bee-block bee-block-4 bee-divider">
                                        <div class="spacer" style="height: 0px;"></div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <div class="bee-col bee-col-1 bee-col-w6" style="padding-top: 0;">
                                    <div class="bee-block bee-block-4 bee-text">
                                        <div class="bee-text-content" style="line-height: 120%; font-size: 12px; color: #ffffff; font-family: inherit;">
                                            <p style="font-size: 14px; line-height: 16px; text-align: left;">
                                                <span style="font-size: 14px;">
                                                    Created -  {} 
                                                </span>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            <div class="bee-row bee-row-4">
                <div class="bee-row-content no_stack">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; border: 0; max-width: 600px !important;">
                        <tr>
                            <td align="center" style="width: 33.3%;">
                                <div class="bee-col bee-col-1 bee-col-w6" style="padding-bottom: 10px !important;">
                                    <div class="bee-block bee-block-1 bee-html-block">
                                        <div class="our-class" style="width: 100%; height: 0; border: 1px solid black; border-radius: 50%; border-color: #29873f; padding-bottom: 100%; min-width: 80px;">
                                            <div class="primary-label large-label">
                                                {}
                                            </div>
                                            <div class="secondary-label">
                                                Daily
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </td>
                            <td align="center" style="width: 33.3%;">
                                <div class="bee-col bee-col-1 bee-col-w6" style="padding-bottom: 10px !important;">
                                    <div class="bee-block bee-block-1 bee-html-block">
                                        <div class="our-class" style="width: 100%; height: 0; border: 1px solid black; border-radius: 50%; border-color: #29873f; padding-bottom: 100%; min-width: 80px;">
                                            <div class="primary-label large-label">
                                                {}
                                            </div>
                                            <div class="secondary-label">
                                                Weekly total
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </td>
                            <td align="center" style="width: 33.3%;">
                                <div class="bee-col bee-col-1 bee-col-w6" style="padding-bottom: 10px !important;">
                                    <div class="bee-block bee-block-1 bee-html-block">
                                        <div class="our-class" style="width: 100%; height: 0; border: 1px solid black; border-radius: 50%; border-color: #29873f; padding-bottom: 100%; min-width: 80px;">
                                            <div class="primary-label large-label">
                                                {}
                                            </div>
                                            <div class="secondary-label">
                                                Mothly total
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                        
                    </table>
                </div>
            </div>
            <div class="bee-row bee-row-3">
                <div class="bee-row-content">
                    <div class="bee-col bee-col-1 bee-col-w12">
                        <div class="bee-block bee-block-1 bee-text">
                            <div class="bee-text-content" style="line-height: 120%; font-size: 12px; color: #000000; font-family: inherit;">
                                <p style="font-size: 14px; line-height: 16px;">
                                    <span style="font-size: 22px; line-height: 28px;">
                                        Interactions
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bee-row bee-row-5">
                <div class="bee-row-content">
                    <div class="bee-col bee-col-1 bee-col-w12">
                        <div class="bee-block bee-block-1 bee-html-block">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; border: 0; max-width: 600px !important;">
                                                           
                            <!--begin individual job-->
                            <tr>
                                <td class="bee-performance-item" style="border: 0; font-weight: normal; background-color: #ffffff; mso-line-height-rule: exactly; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top">
                                    <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
                                       """.format(current_date,dailyCount,weeklyCount,monthlyCount)
for phone_number, messages in message_rows.items():
    message_body += f"{phone_number}:\n"
    HTML += """
			<tr>
				<td
					style="
						/* border-left: 4px solid #ff6969; */
						padding-left: 20px;
						mso-line-height-rule: exactly;
						-ms-text-size-adjust: 100%;
						-webkit-text-size-adjust: 100%;
						text-align: left;
						font-size: 14px;
						font-family: 'Lato', Roboto, Helvetica;
						line-height: 150%;
						color: #000000;
						word-break: break-word;
					"
					valign="top"
				>
					<a href="#" rel="noopener" style="color: #ff6969; font-size: 16px; font-weight: bold;" target="_blank">
						    Number:	{}
					</a>""".format(phone_number)
    for i, (customer_message, bot_message, created_date) in enumerate(messages):
        message_body += f"Customer Message: {customer_message}\nBot Message: {bot_message}\nCreated Date: {created_date}"
        HTML += """ 
					<br />
					<b>customer_message</b>: {} 
					<br />
					<b>bot_message</b>:  {}
					<br />
					<b>created_datetime</b>:  {} 
					<br />""".format(customer_message,bot_message,created_date)
    HTML +="""
			</td>
			</tr>
			<br />"""
HTML += """
			</table>
			</td>
			</tr>
			<!--end individual job-->
                           
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="bee-row bee-row-6">
                <div class="bee-row-content">
                    <div class="bee-col bee-col-1 bee-col-w12">
                        <div class="bee-block bee-block-1 bee-divider">
                            <div class="spacer" style="height: 0px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="bee-row bee-row-7">
                <div class="bee-row-content">
                    <div class="bee-col bee-col-1 bee-col-w12">
                        <div class="bee-block bee-block-1 bee-divider">
                            <div class="spacer" style="height: 0px;"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
 """

print(message_body)

message = client.messages.create(
    body=message_body,
    from_='+15177013732',
    to='+17078151463'
)

msg = MIMEMultipart()
msg['Subject'] = "Daily updates"
msg['From'] = sender_email
msg['To'] = ", ".join(to_emails)
msg['Cc'] = ", ".join(cc_emails)

html_body = MIMEText(HTML, 'html')
msg.attach(html_body)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, password)
    smtp.sendmail(sender_email, to_emails + cc_emails, msg.as_string())