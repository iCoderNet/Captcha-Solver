import cv2
import numpy as np
import pytesseract
import os
import shutil

# --- Harfni markazga joylashtirish ---
def center_letter(img, target_size=(50, 50)):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return cv2.resize(img, target_size)
    x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
    letter_crop = img[y:y+h, x:x+w]
    canvas = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
    x_offset = (target_size[0] - w) // 2
    y_offset = (target_size[1] - h) // 2
    canvas[y_offset:y_offset+h, x_offset:x_offset+w] = letter_crop
    return canvas

# --- Rasmni kattalashtirish ---
def upscale_for_ocr(img, scale=5):
    return cv2.resize(img, (img.shape[1]*scale, img.shape[0]*scale), interpolation=cv2.INTER_LINEAR)

# --- Kontrastni oshirish ---
def preprocess_for_ocr(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return thresh

# --- Pytesseract bilan tanish ---
def recognize_letter(img):
    preprocessed = preprocess_for_ocr(upscale_for_ocr(img))
    text = pytesseract.image_to_string(preprocessed, config='--psm 10')
    return text.strip()

# --- Captcha yechuvchi asosiy funksiya ---
def solve_captcha(image_path, step=25):
    # Papkani tayyorlash
    chars_dir = 'chars'
    if os.path.exists(chars_dir):
        shutil.rmtree(chars_dir)
    os.makedirs(chars_dir)

    # Rasmni o'qish va fonni tozalash
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    img[(img == [211, 211, 211]).all(axis=2)] = [0, 0, 0]
    img[(img != 0).any(axis=2)] = [255, 255, 255]

    captcha_text = ""

    for i in range(width // step):
        x_start = i * step
        x_end = x_start + step
        if x_end > width:
            break

        roi = img[0:height, x_start:x_end]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            side = max(w, h)
            cropped = np.zeros((side, side, 3), dtype=np.uint8)
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(x1 + w, step)
            y2 = min(y1 + h, roi.shape[0])
            roi_part = roi[y1:y2, x1:x2]
            cropped[:roi_part.shape[0], :roi_part.shape[1]] = roi_part
            cropped[(cropped != 0).any(axis=2)] = [255, 255, 255]

            # Harfni markazga joylashtirish
            centered = center_letter(cropped)

            # Harfni tanish
            letter = recognize_letter(centered)
            captcha_text += letter

            # Harfni saqlash
            char_path = os.path.join(chars_dir, f'char_{i}_{letter}.png')
            cv2.imwrite(char_path, centered)

    # Papkani tozalash
    shutil.rmtree(chars_dir)

    print(f"\n✅ Captcha natijasi: {captcha_text}")
    return captcha_text

solve_captcha("c.png")