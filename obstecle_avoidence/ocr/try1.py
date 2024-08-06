import cv2
import pytesseract
from PIL import Image
import numpy as np
from PIL import ImageEnhance


# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

from tqdm import tqdm

def preprocess_image(image_path):
    # Load your image
    image = cv2.imread(image_path)

    # Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Scale the image
    scale_percent = 300 # percent of original size
    width = int(binary.shape[1] * scale_percent / 100)
    height = int(binary.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(binary, dim, interpolation = cv2.INTER_AREA)

    # Enhance the contrast of the image
    pil_img = Image.fromarray(resized)
    enhancer = ImageEnhance.Contrast(pil_img)
    enhanced_im = enhancer.enhance(4.0)
    contrast_img = np.asarray(enhanced_im)

    # Remove noise from the image
    blur = cv2.GaussianBlur(contrast_img,(5,5),0)

    # Deskew the image
    coords = np.column_stack(np.where(blur > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = blur.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Add a progress bar for the deskewing process
    with tqdm(total=h, desc="Deskewing", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for i in range(h):
            deskewed = cv2.warpAffine(blur[i], M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            pbar.update(1)

    return deskewed


def ocr_image(image):
    # OCR
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def main():
    image_path = '/home/austine/Downloads/ocr.jpeg'  # replace with your image path
    preprocessed_image = preprocess_image(image_path)
    text = ocr_image(preprocessed_image)
    print(text)

if __name__ == "__main__":
    main()
