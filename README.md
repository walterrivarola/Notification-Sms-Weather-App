# <h1 align=center> **SMS weather notifications** </h1> 

## **App Description**
An application that notifies you by SMS at what time of day there is a high probability of rain.

## **Libraries used**
* twilio==7.14.0
* pandas==1.3.4
* requests==2.22.0
* tqdm==4.62.3

## **Registration required to access the API and send SMS**
* Weather API = https://www.weatherapi.com/
* Twilio SMS = https://www.twilio.com/

## **Settings**
Edit the twilio_config.py file and add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI, between the quotes

## **API Data source**

+ The API used to generate the necessary logs were extracted directly from the Wheather API (https://www.weatherapi.com/).

## **Outgoing message Example**
In case there is no probability of rain, the following message is sent:
Hi! Today is weather forecast 27/01/2023 from New York indicates no chance of rain.

If there is probability:
Hi! Today is weather forecast 27/01/2023 from New York indicates no chance of rain is:

Hora   Condicion<br>
16     Patchy rain possible<br>
17     Patchy rain possible
