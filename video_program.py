import cv2, pandas
from datetime import datetime

first_frame = None
motion_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    motion = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #reducerea cantitatii de detalii nesemnificative care ar putea fi interpretate ca mișcare
    gray = cv2.GaussianBlur(gray, (21,21), 0) 

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1] #al doilea item al tuplului returnat
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=3)

    contours = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    #filtrare
    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            motion = 1
            (x, y, w, h)= cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    motion_list.append(motion)

    motion_list = motion_list[-2:]

    if motion_list[-1] == 1 and motion_list[-2] == 0:
        times.append(datetime.now())
    elif motion_list[-1] == 0 and motion_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Gray frame", gray)
    cv2.imshow("Delta frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if motion == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = pandas.concat([df, pandas.DataFrame({"Start": [times[i]], "End": [times[i+1]]})], ignore_index=True)
df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows