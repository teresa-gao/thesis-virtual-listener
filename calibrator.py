import cv2

from keyboard import is_pressed

from face_util import *


face_width = 165
face_height = 215
frame_width = 1280
frame_height = 720
black_background_path = 'black.png' # 1280 x 720 pixels

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.75
margin = int(font_scale * 50)
offset_from_center = -275
color = (0, 0, 255) # BGR
text_thickness = 1
dot_radius = 3

calibration_frames = 30


def run_calibration(cap, prompt):
    '''
    Prepare study by centering face of participant before webcam and
    calculating face node positions for neutral expression.
    '''

    # DISPLAY WELCOME INSTRUCTIONS

    frame = cv2.imread(black_background_path)
    frame = cv2.putText(
        frame,
        'Press the spacebar to begin calibration.',
        (margin, margin),
        font,
        font_scale,
        color,
        text_thickness
    )
    cv2.imshow('Welcome', frame)
    cv2.waitKey()
    cv2.destroyAllWindows()


    # ALIGN FACE FOR CALIBRATION

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
        frame = cv2.flip(frame, 1) # flip horizontally to mirror user
        frame = cv2.resize(frame, (frame_width, frame_height))

        frame = cv2.circle(
            img=frame,
            center=(int(frame_width/2), int(frame_height/2)),
            radius=dot_radius,
            color=color,
            thickness=dot_radius*2,
        )
        frame = cv2.ellipse(
            img=frame,
            center=(int(frame_width/2), int(frame_height/2)),
            axes=(face_width, face_height),
            angle=360,
            startAngle=0,
            endAngle=360,
            color=color,
            thickness=3,
        )
        frame = cv2.putText(
            frame,
            'Align your face inside the circle and look at the red dot.',
            (margin, margin),
            font,
            font_scale,
            color,
            text_thickness,
        )
        frame = cv2.putText(
            frame,
            'Press the spacebar when ready to calibrate.',
            (margin, margin * 2),
            font,
            font_scale,
            color,
            text_thickness,
        )

        cv2.imshow('Calibration', frame)

        if cv2.waitKey(5) & 0xFF == 27 or is_pressed(' '):
            break


    # RUN CALIBRATION

    cv2.waitKey(250) # prevent closing out of new loop with previous spacebar press
    face_landmarks_list = []
    while cap.isOpened() and len(face_landmarks_list) < calibration_frames:
        success, frame = cap.read()
        if not success:
            continue
        frame = cv2.flip(frame, 1) # flip horizontally to mirror user
        frame = cv2.resize(frame, (frame_width, frame_height))
        results = get_landmarks_from_frame(frame)
        face_landmarks = calculate_landmarks(results)
        face_landmarks_list.append(face_landmarks)

        frame = cv2.circle(
            img=frame,
            center=(int(frame_width/2), int(frame_height/2)),
            radius=dot_radius,
            color=color,
            thickness=dot_radius*2,
        )
        frame = cv2.ellipse(
            img=frame,
            center=(int(frame_width/2), int(frame_height/2)),
            axes=(face_width, face_height),
            angle=360,
            startAngle=0,
            endAngle=360,
            color=color,
            thickness=3,
        )

        cv2.imshow('Calibration', frame)

        if cv2.waitKey(5) & 0xFF == 27 or is_pressed(' '):
            continue

    neutral_face_landmarks = face_landmarks_list # average_face_landmarks(face_landmarks_list)


    # DISPLAY EXPERIMENT INSTRUCTIONS

    frame = cv2.imread(black_background_path)
    frame = cv2.putText(
        frame,
        'Calibration complete.',
        (int(frame_width / 2) + offset_from_center, margin),
        font,
        font_scale,
        color,
        text_thickness
    )
    frame = cv2.putText(
        frame,
        'You will now be given a prompt to answer aloud.',
        (int(frame_width / 2) + offset_from_center, margin * 3),
        font,
        font_scale,
        color,
        text_thickness
    )
    frame = cv2.putText(
        frame,
        'While doing so, look at the red dot and',
        (int(frame_width / 2) + offset_from_center, margin * 5),
        font,
        font_scale,
        color,
        text_thickness
    )
    frame = cv2.putText(
        frame,
        'try to limit the movement of your head.',
        (int(frame_width / 2) + offset_from_center, margin * 6),
        font,
        font_scale,
        color,
        text_thickness
    )
    frame = cv2.putText(
        frame,
        'Please continue responding for the full',
        (int(frame_width / 2) + offset_from_center, margin * 7),
        font,
        font_scale,
        color,
        text_thickness
    )
    frame = cv2.putText(
        frame,
        '60 seconds that you are given to answer.',
        (int(frame_width / 2) + offset_from_center, margin * 8),
        font,
        font_scale,
        color,
        text_thickness
    )
    frame = cv2.putText(
        frame,
        'YOUR PROMPT IS:',
        (int(frame_width / 2) + offset_from_center, margin * 10),
        font,
        font_scale,
        color,
        text_thickness
    )
    frame = cv2.putText(
        frame,
        f'"{prompt}"',
        (int(frame_width / 2) + offset_from_center, margin * 11),
        font,
        font_scale,
        color,
        text_thickness
    )
    frame = cv2.putText(
        frame,
        'Press the spacebar to begin.',
        (int(frame_width / 2) + offset_from_center, margin * 13),
        font,
        font_scale,
        color,
        text_thickness
    )
    cv2.imshow('Calibration', frame)
    cv2.waitKey()
    cv2.destroyAllWindows()

    return neutral_face_landmarks


if __name__ == '__main__':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    run_calibration(cap, '"Talk about something that you are looking forward to."')

    cv2.destroyAllWindows()
