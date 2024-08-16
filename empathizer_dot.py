import cv2

from time import time
from math import floor
from keyboard import is_pressed

from calibrator import run_calibration, frame_width, frame_height, black_background_path, font, font_scale, color, margin, text_thickness, dot_radius


def run_empathizer_dot(prompt, total_seconds=90, frame_delay=0):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    _ = run_calibration(cap, prompt)

    start = time()
    while time() - start < total_seconds:
        frame = cv2.imread(black_background_path)
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
            f'{total_seconds - floor(time() - start)} seconds left ...',
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
        f'Please open the browser and complete the POMS questionnaire.',
        (margin, margin),
        font,
        font_scale,
        color,
        text_thickness,
    )
    cv2.imshow('Empathizer', frame)
    cv2.waitKey()


if __name__ == '__main__':
    prompt = 'Talk about something that you are looking forward to.'

    run_empathizer_dot(
        prompt,
        total_seconds=5
    )
