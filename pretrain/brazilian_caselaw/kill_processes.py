import os


os.system("kill $(ps aux | grep scraper_brazilian_court | awk '{print $2}')")