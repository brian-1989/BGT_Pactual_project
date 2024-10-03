from datetime import datetime
import pytz

def create_date():
    bogota_tz = pytz.timezone('America/Bogota')
    now = datetime.now(bogota_tz)
    return now