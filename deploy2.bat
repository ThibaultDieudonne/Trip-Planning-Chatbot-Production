@echo off
cls
cd "C:\Users\Skrell\Desktop\home\taff\OpenClassrooms\OC-Projet10-Deploy"
rem set MicrosoftAppId=f7b50eea-aa70-422e-b5ae-df93e43caca3  b6cc7642-85f0-4bd9-bf16-4ae24c7192db
rem set MicrosoftAppPassword=bbd8839e0091448b8c90b5f45453a072  751b7d36c78246119ac8b5e8c2336d86
set LuisAppId=f7b50eea-aa70-422e-b5ae-df93e43caca3
set LuisAPIKey=bbd8839e0091448b8c90b5f45453a072
set LuisAPIHostName=westeurope.api.cognitive.microsoft.com
set AppInsightsInstrumentationKey=df10c491-90b7-4685-9ed1-ef4db41c40eb
call conda activate bot6
pip install -r requirements.txt
rem gunicorn --bind=0.0.0.0 --timeout 600 app:run
python -m aiohttp.web -H 0.0.0.0 -P 8000 app:run
pause>nul