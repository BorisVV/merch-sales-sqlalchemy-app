from datetime import date
def format_date(dateAsString): #"format date =(m-d-Y)"
    # If the text box is left empty.
    if dateAsString == "":
        return ""
    # Otherwise return the string formatted to int.
    else:
        d = list(map(int, dateAsString.split('-')))
        return date(d[0], d[1], d[2])

def format_date_jinja(dt):
    return dt.strfdate('%m-%d-%Y')
