import cv2
import numpy as np

IN = '../images/water-bottle.jpg'
OUT = '../images/adj-water-bottle.jpg'
SIZE = 300
font = cv2.FONT_HERSHEY_SIMPLEX
fcolor = (0, 0, 0)

def preprocess(image):
  image = resize(image)

  out = np.zeros((SIZE * 2, SIZE * 3, 3), dtype=np.uint8)
  brightness = [0, -127, 127,   0,  0, 64]
  contrast   = [0,    0,   0, -64, 64, 64]
  for i, b in enumerate(brightness):
    c = contrast[i]
    print('b, c:  ', b, ', ', c)
    row = SIZE * (i // 3)
    col = SIZE * (i % 3)

    print('row, col:  ', row, ', ', col)

    out[row:row + SIZE, col: col + SIZE] = boost_contrast(image, b, c)
    # Comment to remove labels from output images
    msg = 'b %d' % b
    cv2.putText(out, msg, (col, row + SIZE - 22), font, .7, fcolor, 1, cv2.LINE_AA)
    msg = 'c %d' % c
    cv2.putText(out, msg, (col, row + SIZE - 4), font, .7, fcolor, 1, cv2.LINE_AA)

  cv2.imwrite(OUT, out)

def boost_contrast(image, brightness=0, contrast=0):
  if brightness != 0:
    if brightness > 0:
      shadow = brightness
      highlight = 255
    else:
      shadow = 0
      highlight = 255 + brightness
    alpha_b = (highlight - shadow) / 255
    gamma_b = shadow
    buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
  else:
    buf = image.copy()

  if contrast != 0:
    f = 131 * (contrast + 127) / (127 * (131 - contrast))
    alpha_c = f
    gamma_c = 127 * (1 - f)
    buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

  return buf

def resize(image):
  # Downsample, preserve aspect ratio
  scale = 30
  w = int(image.shape[1] * scale / 100)
  h = int(image.shape[0] * scale / 100)
  image = cv2.resize(image, (w, h), 0, 0, cv2.INTER_AREA)

  # Center crop to desired dimensions
  center = (image.shape[0] / 2, image.shape[1] / 2)
  x = int(center[1] - SIZE / 2)
  y = int(center[0] - SIZE / 2)
  return image[y:y+SIZE, x:x+SIZE]

preprocess(cv2.imread(IN))
