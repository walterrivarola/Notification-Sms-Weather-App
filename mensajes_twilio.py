import os
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,PHONE_NUMBER, API_KEY_WAPI
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import pandas as pd
import requests
from tqdm import tqdm #Libreria para barra de carga

from datetime import datetime

query = 'Ciudad del Este'
api_key = API_KEY_WAPI
url_clima=f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days=1&aqi=no&alerts=no'

response = requests.get(url_clima).json()

response['forecast']['forecastday'][0].keys()

#We extract each of the fields of the 24 records
#of each hour from the WeatherAPI
def get_forecast(response,i):
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    temperatura = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    lluvia = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_lluvia = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return fecha, hora, condicion, temperatura, lluvia, prob_lluvia

datos = []
cant_registro = len(response['forecast']['forecastday'][0]['hour'])
for i in tqdm(range(cant_registro)):
    datos.append(get_forecast(response,i))

#We generate our DataFrame
col = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'Prob_lluvia']
df = pd.DataFrame(datos,columns = col)

#We generate a new DataFrame that will contain the conditions that will be saved for sending SMS
df_lluvia = df[(df['Lluvia']==1) & (df['Hora']>6) & (df['Hora']<22)]#Guardamos los registros que van desde 06:00 a 22:00 
df_lluvia = df_lluvia[['Hora', 'Condicion']]#Reducimos a dos columnas, que son los que me interesa utilizar
df_lluvia.set_index('Hora', inplace=True)

#We verify if there is a probability of rain or not, checking if there is any data in the DataFrame
if df_lluvia.empty:
    mensaje = '\Hi! \n\n\n Today is weather forecast ' + df['Fecha'][0] + ' from ' + query + ' indicates no chance of rain'
else:
    mensaje = '\Hi! \n\n\n Today is weather forecast ' + df['Fecha'][0] + ' from ' + query + ' is: \n\n\n ' + str(df_lluvia)

# SMS message from Twilio
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body=mensaje,
         from_=PHONE_NUMBER,
         to='+595973448101'
     )

print('Message sent' + message.sid)