from django.utils.timezone import now as timezone_now

from api.models.core import ImagesizatorFile


def delete_expired_files():
    try:
        files_query = ImagesizatorFile.objects.filter(
            expiration_date__lt=timezone_now(),
            is_static=False
        )

        for file in files_query:
            file.delete()

        return True
    except Exception as e:
        print("Error deleting:", e)

    return False
