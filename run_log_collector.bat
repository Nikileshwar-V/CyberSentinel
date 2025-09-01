@echo off
:: Runs the log reader script with admin privileges
powershell -Command "Start-Process python 'logs/win_log_reader.py' -Verb runAs"
