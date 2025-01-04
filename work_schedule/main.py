from icecream import ic
from datetime import datetime

from work_schedule.store.db.db import DB

ic.includeContext = True

# date_string = datetime.now().strftime("%Y-%m-%d")
# date_format = '%Y-%m-%d'
#
# date_object = datetime.strptime(date_string, date_format)





db = DB()
try:
    ic(db.get_full_data_driver_by_id(1))
except Exception as e:
    print(e)