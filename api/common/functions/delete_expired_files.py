import logging

from django.utils.timezone import now as timezone_now

from api.models.core import ImagesizatorFile


def delete_expired_files():
    try:
        logging.log(1, "before query")
        files_query = ImagesizatorFile.objects.filter(
            expiration_date__lt=timezone_now(), is_static=False
        )
        logging.log(1, "after query")
        for file in files_query:
            logging.log(1, "Deleting file:", file.file_name)
            file.delete()

        return True
    except Exception as e:
        logging.log(1, "Error deleting:", e)

    return False
