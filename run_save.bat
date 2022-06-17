@echo off
cls
cd "C:\Users\Skrell\Desktop\home\taff\OpenClassrooms\OC-Projet10-Deploy"
rem set MicrosoftAppId=b83026e4-0ff9-497f-bac4-cb3ac6a2c645 || 
rem set MicrosoftAppPassword=499b495acfdd4b5aa06c2d5db2c56066 || 
set LuisAppId=f7b50eea-aa70-422e-b5ae-df93e43caca3
set LuisAPIKey=bbd8839e0091448b8c90b5f45453a072
set LuisAPIHostName=westeurope.api.cognitive.microsoft.com
set AppInsightsInstrumentationKey=df10c491-90b7-4685-9ed1-ef4db41c40eb
call conda activate bot4
python app.py
pause>nul