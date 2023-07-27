from django.utils.timezone import now as timezone_now

from api.models import ImagesizatorTemporaryFile


def delete_expired_files():
    try:
        files_query = ImagesizatorTemporaryFile.objects.filter(
            expiration_date__lt=timezone_now()
        )

        for file in files_query:
            file.delete()

        return True
    except Exception as e:
        print("Error deleting:", e)

    return False
