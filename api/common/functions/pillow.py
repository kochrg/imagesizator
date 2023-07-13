import base64

from django.core.files.base import ContentFile
from PIL import Image

from api.common.utils.api_functions import \
    get_final_image_width_and_height, \
    get_named_temporary_file


# User must be logged to use this endpoint.
# Use 'Authorization: Token the_token' header.
def pillow_image_resize(publish, temporal, image, to_width, to_height, keep_proportion, suffix):
    image_thumbnail = Image.open(
        ContentFile(image, "temp_image" + suffix)
    )
    final_w_h = get_final_image_width_and_height(
        image_thumbnail.width,
        image_thumbnail.height,
        to_width,
        to_height,
        keep_proportion
    )
    image_thumbnail.thumbnail(final_w_h)

    # Saving resized image to a temporal file
    # NOTE: must be used image_thumbnail.save() as the function used
    # for save the image, other saving methods didn't work (fails when saving).
    # Using image_thumbnail.tobytes() to avoid save the file
    # (using memory buffer) fails too.
    # TODO: check if there is a faster way.

    resized_image_file = get_named_temporary_file(
        'pil_resized_',
        suffix,
        publish,
        temporal
    )
    image_thumbnail.save(resized_image_file.name)

    img_bytes = resized_image_file.read()
    string_image = base64.b64encode(img_bytes).decode('utf8')

    return resized_image_file, string_image, final_w_h
