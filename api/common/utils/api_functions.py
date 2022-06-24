from api.models import Parameters


def get_parameter_value(key):
    try:
        parameter = Parameters.objects.get(key=key)

        return parameter.value
    except Parameters.DoesNotExist:
        print("Error obteniendo el parametro: " + str(key))

    return False


def diff_month(d1, d2):
    # Get months between two dates. D2 <= D1
    if d1 == d2:
        return 0
    return (d1.year - d2.year) * 12 + d1.month - d2.month