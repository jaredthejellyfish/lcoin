import secrets
import os

from lcoin_wallet import mail

from flask import url_for, current_app

from PIL import Image

from flask_mail import Message

from PIL import Image


def resize_image(image: Image, length: int) -> Image:
    """
    Resize an image to a square. Can make an image bigger to make it fit or smaller if it doesn't fit. It also crops
    part of the image.

    :param self:
    :param image: Image to resize.
    :param length: Width and height of the output image.
    :return: Return the resized image.
    """

    """
    Resizing strategy : 
     1) We resize the smallest side to the desired dimension (e.g. 1080)
     2) We crop the other side so as to make it fit with the same length as the smallest side (e.g. 1080)
    """
    if image.size[0] < image.size[1]:
        # The image is in portrait mode. Height is bigger than width.

        # This makes the width fit the LENGTH in pixels while conserving the ration.
        resized_image = image.resize(
            (length, int(image.size[1] * (length / image.size[0]))))

        # Amount of pixel to lose in total on the height of the image.
        required_loss = (resized_image.size[1] - length)

        # Crop the height of the image so as to keep the center part.
        resized_image = resized_image.crop(
            box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))

        # We now have a length*length pixels image.
        return resized_image
    else:
        # This image is in landscape mode or already squared. The width is bigger than the heihgt.

        # This makes the height fit the LENGTH in pixels while conserving the ration.
        resized_image = image.resize(
            (int(image.size[0] * (length / image.size[1])), length))

        # Amount of pixel to lose in total on the width of the image.
        required_loss = resized_image.size[0] - length

        # Crop the width of the image so as to keep 1080 pixels of the center part.
        resized_image = resized_image.crop(
            box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))

        # We now have a length*length pixels image.
        return resized_image


def save_picture(form_picture):
    random_hex = secrets.token_hex(7)

    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    i = Image.open(form_picture)
    i = resize_image(i, 125)

    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    if user:
        token = user.get_reset_token()
        msg = Message('Password Reset Request',
                    sender='noreply@lcoin.com',
                    recipients=[user.email])
        msg.body = f'''To reset your password visit the following link:
                       {url_for('users.reset_token', token = token, _external=True)}
                        
                       If you did not make this request simply ignore this email and no changes will be made.'''
        mail.send(msg)
    else:
        return
