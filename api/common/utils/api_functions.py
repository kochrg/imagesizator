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


def get_file_expiration_date(request):
    expiration = 60*60*24  # Default: 24hs.
    try:
        expiration = int(request.data["expiration"])
    except Exception as e:
        print(e)
        user_default = int(get_parameter_value('default_expiration_time'))  # seconds
        if user_default:
            expiration = user_default

    return expiration


def get_final_image_width_and_height(o_width, o_height, to_width, to_height, keep_proportion='none'):
    """
    Return a tuple with the final width and height of the image.
    keep_proportion = 'landscape': resize to_height, width proportionally.
                      'portrait': resize to_width, height proportionally.
                      'none' (default): resize to_width and to_heigth no matter proportions.
    """
    final_width = to_width
    final_height = to_height

    if keep_proportion == 'portrait':
        final_height = int(to_width * o_height / o_width)
    elif keep_proportion == 'landscape':
        final_width = int(to_height * o_width / o_height)
    # else resize ommiting ratio

    return (int(final_width), int(final_height))
