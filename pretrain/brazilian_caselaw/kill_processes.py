import os


os.system("kill -9 $(ps aux | grep scraper_for_brazilian_court_decisions_for_year | awk '{print $2}')")