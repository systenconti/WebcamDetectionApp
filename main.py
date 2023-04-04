import cv2
import time
from emailing import send_email
import glob

#create a video object
video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1
while True:
    status = 0
    check, frame = video.read()
    # Create a gray frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    # Compare the first gray frame
    if first_frame is None:
        first_frame = gray_frame_gau
    # create frames without much background noise for optimalization
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 70, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # app looks for countours to detect object
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #prevent from detecting too little objects
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        #create rectangle
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            # save frames while object enters into the frame
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_to_send = all_images[index]

    # compare statuses when object enters and leaves the frame and then trigger action
    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_to_send)
        print("Email was sent")
    # show the video
    cv2.imshow("Video", frame)
    # create a key to break the loop and exit the video
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()