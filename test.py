from datetime import datetime
from datetime import date

d = datetime.now()
da = d.date()
time = datetime.min.time()
da = datetime.combine(da,time)
print(da)