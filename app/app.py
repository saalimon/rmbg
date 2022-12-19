import os
from flask import Flask, request, render_template, session
import cv2
import numpy as np

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = "/uploads/"
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Set of allowed file extensions


def rm_text(img_path):
    image = cv2.imread(img_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a binary image
    threshold, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Find the contours of the text in the image
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Create a mask with the same size as the image
    mask = np.zeros_like(image)

    # Fill the contours in the mask with white
    cv2.fillPoly(mask, contours, (255, 255, 255))

    # Invert the mask to create a negative mask
    mask = cv2.bitwise_not(mask)

    # Remove the text from the image using the mask
    result = cv2.bitwise_and(image, mask)
    return result


@app.route('/')
def hello():
    return render_template('base.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if 'file' not in request.files:
        return 'No file provided'
    file = request.files['file']
    if file.filename.split('.')[1].lower() not in ALLOWED_EXTENSIONS:
        return 'Invalid file extension'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    session['uploaded_img_file_path'] = os.path.join(
        app.config['UPLOAD_FOLDER'], file.filename)
    # return redirect(url_for('displayImage'))
    return render_template('base.html')


@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    # img_text_removed = rm_text(img_file_path)
    # cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'sign-remove.jpg'),
    #             cv2.cvtColor(img_text_removed, cv2.COLOR_BGR2RGB))
    # # Display image in Flask application web page
    # return render_template('show_image.html', user_image=os.path.join(app.config['UPLOAD_FOLDER'], 'sign-remove.jpg'))
    return render_template('show_image.html', user_image=img_file_path)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
