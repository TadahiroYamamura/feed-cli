@echo off
cd %~dp0

python app.py google /japan_data_vision/articles_download.csv
python app.py yahoo /japan_data_vision/articles_download.csv
