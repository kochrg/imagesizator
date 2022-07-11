import os
from stat import S_IRWXG, S_IRWXU
from tempfile import NamedTemporaryFile
from api.models import Parameters


def get_parameter_value(key):
    try:
        parameter = Parameters.objects.get(key=key)

        return parameter.value
    except Parameters.DoesNotExist:
        print("Error obteniendo el parametro: " + str(key))

    return False


def add_parameter_if_not_exists(key, value):
    """
    Add a parameter if it not exists in database.
    """
    parameter = get_parameter_value(key)

    if parameter is not None:
        if not parameter:
            print("Añadiendo el parámetro:", key)
            Parameters(
                key=key,
                value=value
            ).save()
            return True

    return False


def diff_month(d1, d2):
    # Get months between two dates. D2 <= D1
    if d1 == d2:
        return 0
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def get_publish_file_path(temporal):
    path = "/public/temp/"
    if not temporal:
        path = "/public/static/"
    return path


def get_named_temporary_file(prefix, suffix, publish=False, temporal=True):
    if publish:
        # Return image public url
        publish_path = os.getcwd() + get_publish_file_path(temporal)

        temporary_file = NamedTemporaryFile(
            "r+b",
            prefix=prefix,
            suffix=suffix,
            dir=publish_path,
            delete=False
        )

        # chmod 770 (Grant rwx access to www-data.www-data 'user and group')
        os.chmod(temporary_file.name, S_IRWXU + S_IRWXG)
        return temporary_file
    else:
        temporary_file = NamedTemporaryFile("r+b", prefix=prefix, suffix=suffix)

        return temporary_file