import cv2

from math import floor
from time import time
from keyboard import is_pressed

from face_util import *
from calibrator import run_calibration, frame_width, frame_height, black_background_path, font, font_scale, color, margin, text_thickness, dot_radius


def run_empathizer_empathy(prompt, total_seconds=90, frame_delay=10):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    neutral_landmarks = run_calibration(cap, prompt)

    i = 0
    i_delta = 1
    landmarks_buffer = []
    start = time()
    while cap.isOpened() and time() - start < total_seconds:
        frame = cv2.imread(black_background_path)

        success, webcam_frame = cap.read()
        if not success:
            continue
        webcam_frame = cv2.flip(webcam_frame, 1)

        results = get_landmarks_from_frame(webcam_frame)
        landmarks = calculate_landmarks(results)
        landmarks_buffer.append(landmarks)
        if len(landmarks_buffer) < frame_delay:
            if i < 0 or i >= len(neutral_landmarks) - 1:
                i_delta *= -1
            i += i_delta
            draw_landmarks(frame, landmarks=neutral_landmarks[i])
        else:
            draw_landmarks(frame, landmarks_buffer.pop(0))

        frame = cv2.circle(
            img=frame,
            center=(int(frame_width/2), int(frame_height/2)),
            radius=dot_radius,
            color=color,
            thickness=dot_radius*2,
        )
        frame = cv2.putText(
            frame,
            prompt,
            (margin, margin),
            font,
            font_scale,
            color,
            text_thickness,
        )
        frame = cv2.putText(
            frame,
            f'{total_seconds - floor(time() - start)} second(s) left ...',
            (margin, margin * 2),
            font,
            font_scale,
            color,
            text_thickness,
        )

        cv2.imshow('Empathizer', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            continue # ignore keypress

    frame = cv2.imread(black_background_path)
    frame = cv2.putText(
        frame,
        f'Please open the browser and complete the POMS and Likert questionnaires.',
        (margin, margin),
        font,
        font_scale,
        color,
        text_thickness,
    )
    cv2.imshow('Empathizer', frame)
    cv2.waitKey()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    prompt = 'Talk about something that you are looking forward to.'

    run_empathizer_empathy(
        prompt,
        total_seconds=10,
        frame_delay=15,
    )
