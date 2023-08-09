import base64
import cv2

from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings
from tempfile import NamedTemporaryFile
from PIL import Image

from api.models.core import Parameters, ImagesizatorFile


class ImagesizatorImageFile(ImagesizatorFile):
    width = models.IntegerField(
        default=0,
    )
    height = models.IntegerField(
        default=0,
    )
    proportion = models.CharField(
        max_length=10,
        null=True
    )

    class Meta:
        verbose_name = "Imagesizator image file"
        verbose_name_plural = "Imagesizator image files"

    def __str__(self):
        return self.path

    @property
    def string_image(self):
        # Encode:
        # bytes_string --> string
        return base64.b64encode(self.bytes_string).decode('utf8')

    def set_final_image_width_and_height(self, o_width, o_height, to_width, to_height, keep_proportion='none'):
        """
        Return a tuple with the final width and height of the image.
        keep_proportion = 'landscape': resize to_height, width proportionally.
                        'portrait': resize to_width, height proportionally.
                        'none' (default): resize to_width and to_heigth no matter proportions.
        """
        self.width = to_width
        self.height = to_height

        if keep_proportion == 'portrait':
            self.proportion = keep_proportion
            self.height = int(to_width * o_height / o_width)
        elif keep_proportion == 'landscape':
            self.proportion = keep_proportion
            self.width = int(to_height * o_width / o_height)
        # else resize ommiting ratio

        return (int(self.width), int(self.height))

    def opencv_image_resize(self, to_width, to_height, suffix, keep_proportion='none'):
        # Need to save the image from request because cv2.imread only works with a path
        with NamedTemporaryFile("wb", prefix="ocv_img_temp_file_", dir=settings.TRASH_FOLDER, suffix=suffix) as f:
            print("Before write")
            f.write(self.bytes_string)
            processed_image = cv2.imread(f.name)
            print("Image read")
            final_w_h = self.set_final_image_width_and_height(
                processed_image.shape[1],  # original width
                processed_image.shape[0],  # original height
                to_width,
                to_height,
                keep_proportion
            )
            print("Resizing")
            processed_image = cv2.resize(processed_image, final_w_h)

            # Saving resized image to a temporal file and make it public
            # NOTE: must be used cv2.imwrite as the function used for save the image,
            # other saving methods didn't work (fails when trying to save the image),
            # use of processed_image.tobytes() and avoid save the file also failed (memory buffer).
            # TODO: check if there is a faster way.

            resized_image_file = self.set_named_temporary_file(
                suffix,
                'ocv_resized_',
            )
            print("Writing image to new file")
            cv2.imwrite(resized_image_file.name, processed_image)

            print("Configuring bytes_string")
            self.bytes_string = resized_image_file.read()
            f.close()

            return resized_image_file, self.string_image, final_w_h

    def pillow_image_resize(self, to_width, to_height, suffix, keep_proportion='none'):
        image_thumbnail = Image.open(
            ContentFile(self.bytes_string, "temp_image" + suffix)
        )
        final_w_h = self.set_final_image_width_and_height(
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

        resized_image_file = self.set_named_temporary_file(
            suffix,
            'pil_resized_',
        )
        image_thumbnail.save(resized_image_file.name)

        self.bytes_string = resized_image_file.read()

        return resized_image_file, self.string_image, final_w_h