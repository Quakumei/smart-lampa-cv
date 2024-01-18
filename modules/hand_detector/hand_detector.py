import numpy as np
import sys
import time
from multiprocessing import Pipe

import torch
import cv2

from .blazebase import resize_pad, denormalize_detections
from .blazepalm import BlazePalm
from .blazehand_landmark import BlazeHandLandmark
from .visualization import draw_detections, draw_landmarks, draw_roi, HAND_CONNECTIONS

WINDOW = "Lamp cam"


def detect_hand(button_pipe: Pipe = None, debug: bool = True):
    tracking_enabled = False
    if debug:
        cv2.namedWindow(WINDOW)
    gpu = torch.device("cpu")
    torch.set_grad_enabled(False)

    palm_detector = BlazePalm().to(gpu)
    palm_detector.load_weights("blazepalm.pth")
    palm_detector.load_anchors("anchors_palm.npy")
    palm_detector.min_score_thresh = 0.89

    hand_regressor = BlazeHandLandmark().to(gpu)
    hand_regressor.load_weights("blazehand_landmark.pth")

    capture = cv2.VideoCapture(0)
    mirror_img = True

    if capture.isOpened():
        hasFrame, frame = capture.read()
        frames_ct = 0
        start_time = time.time()
        elapsed_time = start_time
    else:
        hasFrame = False

    last_middles = []
    while hasFrame:
        # 01 Preprocess
        # Improves quality but great slowdown
        # frame = cv2.GaussianBlur(frame,(5,5),cv2.BORDER_DEFAULT)
        # frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
        if mirror_img:
            frame = np.ascontiguousarray(frame[:, ::-1, ::-1])
        else:
            frame = np.ascontiguousarray(frame[:, :, ::-1])
        img1, img2, scale, pad = resize_pad(frame)

        # 02 Get predictions
        normalized_palm_detections = palm_detector.predict_on_image(img1)
        palm_detections = denormalize_detections(normalized_palm_detections, scale, pad)

        xc, yc, scale, theta = palm_detector.detection2roi(palm_detections.cpu())
        img, affine2, box2 = hand_regressor.extract_roi(frame, xc, yc, theta, scale)
        flags2, handed2, normalized_landmarks2 = hand_regressor(img.to(gpu))
        landmarks2 = hand_regressor.denormalize_landmarks(
            normalized_landmarks2.cpu(), affine2
        )

        # 03 Calculate points average
        hand_middles = np.mean(np.array(landmarks2.cpu()), axis=1)

        if tracking_enabled:
            # TODO: Tracking logic
            # TODO: Listen somehow for button press and toggle tracking_enabled
            pass

        if debug:
            for i in range(len(flags2)):
                landmark, flag = landmarks2[i], flags2[i]
                if flag > 0.5:
                    draw_landmarks(frame, landmark[:, :2], HAND_CONNECTIONS, size=2)
            for hand_middle in last_middles:
                x, y = [int(x) for x in hand_middle[:2]]
                frame = cv2.circle(
                    frame, (x, y), radius=3, color=(100, 0, 100), thickness=3
                )
            for hand_middle in hand_middles:
                x, y = [int(x) for x in hand_middle[:2]]
                frame = cv2.circle(
                    frame, (x, y), radius=5, color=(255, 0, 255), thickness=5
                )
                frame = cv2.line(
                    frame,
                    (frame.shape[1] // 2, frame.shape[0] // 2),
                    (x, y),
                    color=(0, 255, 0),
                    thickness=1,
                )

            fps = frames_ct / elapsed_time
            cv2.putText(
                frame,
                f"FPS (rough): {fps:.1f}",
                (0, 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                1,
            )
            cv2.putText(
                frame,
                f"Time per frame: {1000 * elapsed_time/(frames_ct+1):.0f} ms",
                (0, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                1,
            )
            cv2.putText(
                frame,
                f"Button pipe: {button_pipe}",
                (0, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                1,
            )
            cv2.putText(
                frame,
                f"Tracking enbaled: {tracking_enabled}",
                (0, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                1,
            )
            frame = cv2.circle(
                frame,
                (frame.shape[1] // 2, frame.shape[0] // 2),
                radius=3,
                color=(0, 255, 0),
                thickness=3,
            )
            cv2.imshow(WINDOW, frame[:, :, ::-1])
            key = cv2.waitKey(1)
            if key == 27:
                break

        last_middles = hand_middles
        hasFrame, frame = capture.read()
        frames_ct += 1
        elapsed_time = time.time() - start_time
        if frames_ct % 1000 == 10:
            print("Cam is Working...")

    capture.release()
    if debug:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_hand(debug=True)
