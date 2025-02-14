import cv2


def blend_images(src, watermark, offset, ratio_src, ratio_watermark):

    # Resize the images
    watermark = cv2.resize(watermark, (int(watermark.shape[1] * ratio_watermark),
                                       int(watermark.shape[0] * ratio_watermark)))
    src = cv2.resize(src, (int(src.shape[1] * ratio_src),
                           int(src.shape[0] * ratio_src)))

    # Define the offset to paste the watermark
    x_end = offset[1] + watermark.shape[1]
    y_end = offset[0] + watermark.shape[0]

    # Extract the region of interest from the background
    roi = src[offset[0]:y_end, offset[1]:x_end]

    # Generate the mask
    watermark_gray = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(watermark_gray, 250, 255, cv2.THRESH_BINARY)

    # Apply the mask on the background
    bg = cv2.bitwise_or(roi, roi, mask=mask)

    # Inverse the mask in order to get back the colors of the foreground
    mask_inv = cv2.bitwise_not(mask)
    fg = cv2.bitwise_and(watermark, watermark, mask=mask_inv)

    # Blend the background with the foreground
    final_roi = cv2.add(bg, fg)

    # Insert the ROI in the original image
    src[offset[0]:y_end, offset[1]:x_end] = final_roi

    return src
