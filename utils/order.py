import datetime

def create_order_number(data) -> str:
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr, mt, dt)
    current_date = d.strftime("%Y%m%d")     # 20210305
    order_number = current_date + str(data.id)
    return order_number