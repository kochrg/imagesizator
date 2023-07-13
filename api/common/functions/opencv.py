import base64
import cv2

from tempfile import NamedTemporaryFile

from api.common.utils.api_functions import \
    get_named_temporary_file, \
    get_final_image_width_and_height


def opencv_image_resize(publish, temporal, image, to_width, to_height, keep_proportion, suffix):

    string_image = False
    # Need to save the image from request because cv2.imread only works with a path
    with NamedTemporaryFile("wb", suffix=suffix) as f:
        f.write(image)
        processed_image = cv2.imread(f.name)
        
        final_w_h = get_final_image_width_and_height(
            processed_image.shape[1],  # original width
            processed_image.shape[0],  # original height
            to_width,
            to_height,
            keep_proportion
        )
        processed_image = cv2.resize(processed_image, final_w_h)

        # Saving resized image to a temporal file and make it public
        # NOTE: must be used cv2.imwrite as the function used for save the image,
        # other saving methods didn't work (fails when trying to save the image),
        # use of processed_image.tobytes() and avoid save the file also (memory buffer).
        # TODO: check if there is a faster way.

        resized_image_file = get_named_temporary_file(
            'ocv_resized_',
            suffix,
            publish,
            temporal
        )
        cv2.imwrite(resized_image_file.name, processed_image)

        img_bytes = resized_image_file.read()
        string_image = base64.b64encode(img_bytes).decode('utf8')
        f.close()

        return resized_image_file, string_image, final_w_h


