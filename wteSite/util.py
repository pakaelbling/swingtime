def date_transform_query(date):
    minutes = date.hour * 60 + date.minute
    offsetFrom11 =  minutes- 11*60
    return offsetFrom11

def date_transform_point(date, wait):
    return date_transform_query(date) - wait