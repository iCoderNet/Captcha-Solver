# Captcha Solver

Bu loyiha captcha rasmidagi harflarni avtomatik tanish uchun yozilgan. Rasm bo‘laklarga ajratiladi, har bir harf markazga joylashtiriladi, va pytesseract yordamida taniladi.

##### Captcha:
![Captcha Image](c.png)

## Ishni bajarish bosqichlari:
### Rasmni o‘qish 
- Captcha rasm fayli `cv2.imread` bilan o‘qiladi.

### Fonni tozalash 
- Kulrang fondagi burchak chiqziq rangi `[211, 211, 211]` qora rangga o‘zgartiriladi. Qolgan rangli piksellar oq rangga o'tkaziladi.

### Bo‘laklarga ajratish
- Rasm har 25px bo‘lakka ajratiladi (step=25). Chunki har bir harf 25px da joylashgani uchun.

### Kontur orqali harfni topish 
- Har bir bo‘lakda eng katta kontur aniqlanadi va kvadrat qilib kesiladi.

### Harfni markazga joylashtirish 
- Harf tasviri kvadrat fon ichida markazga ko‘chiriladi. Chunki `pytesseract` yordamida tanish uchun harf markazga joylashilishi kerak.

### OCR bilan tanish
- Harf pytesseract yordamida taniladi (--psm 10 — bitta harf).

### Natijani yig‘ish 
- Harflar ketma-ket birlashtirilib captcha_text hosil qilinadi.

### Kesh papka 
- Harflar chars/ papkaga saqlanadi, ish tugagach o‘chiriladi.

## Ishga tushirish
```python 
from captcha_solver import solve_captcha
solve_captcha("c2.png") 
```

## Natija
```
✅ Captcha natijasi: J7K9 
```

## Talablar
- OpenCV (cv2)
- NumPy
- Pytesseract