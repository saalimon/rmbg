# Import the necessary libraries
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory
# from werkzeug.utils import secure_filename

# Set up the Flask app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # If the form has been submitted
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        # Save the file to a temporary location
        # filename = secure_filename(file.filename)
        file.save(file.filename)

        # Read the image
        image = cv2.imread(file.filename)

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

        # Save the result
        cv2.imwrite("result.png", result)

        # Return the result image to the user
        return send_from_directory('./', 'result.png')

    # If the form has not been submitted, render the file upload form
    return render_template('index.html')


# Run the app
if __name__ == '__main__':
    app.run("0.0.0.0", port=5000)
