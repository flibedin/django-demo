import time, datetime

# la fecha viene en formato dd/mm/aa
def valida_fecha( fecha ):

    if fecha == '' or fecha == None:
        return None

    # valido la fecha
    try:
        t = time.strptime( fecha, "%d/%m/%Y")
    except ValueError:
        return None

    # retorno la fecha en formato AAAA-MM-DD
    return time.strftime('%Y/%m/%d', t )
