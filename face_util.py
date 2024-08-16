import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_containers = mp.tasks.components.containers


class LandmarkList(): # workaround to instantiate pseudo landmark list
    def __init__(self, landmark_list):
        self.landmark = landmark_list

lip_pairs = { # averaged to avoid open mouth
    (191, 95),
    (80, 88),
    (81, 178),
    (82, 87),
    (13, 14),
    (312, 317),
    (311, 402),
    (310, 318),
    (415, 324)
}

lipless_landmark_indices = { # indices of landmarks to draw
    61, 76, 62, 78, # left lip corner
    291, 306, 292, 308, # right lip corner
    33, 130, 226, # left eye corner
    263, 359, 446, # right eye corner
    2, 48, 64, 97, 98, 278, 294, 326, 327, # nose
    63, 66, 66, 70, 105, 107, # right eyebrow
    293, 296, 300, 334, 336, # left eyebrow
}

facemesh_connections_list = [
    mp_face_mesh.FACEMESH_LEFT_EYE,
    mp_face_mesh.FACEMESH_RIGHT_EYE,
    mp_face_mesh.FACEMESH_FACE_OVAL,
]
for facemesh_connections in facemesh_connections_list:
    for index1, index2 in facemesh_connections:
        lipless_landmark_indices.add(index1)
        lipless_landmark_indices.add(index2)


def get_landmarks_from_frame(frame):
    return mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True).process(frame)

def calculate_landmarks(results, return_as_landmark_list=True):
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks: # should only have 1
            lipless_landmarks = []

            for i in range(len(face_landmarks.landmark)):
                if i in lipless_landmark_indices:
                    landmark = face_landmarks.landmark[i]
                    x = landmark.x
                    y = landmark.y
                    z = landmark.z
                    lipless_landmarks.append(mp_containers.NormalizedLandmark(x, y, z))

            for lipcoord1_index, lipcoord2_index in lip_pairs:
                lipcoord1 = face_landmarks.landmark[lipcoord1_index]
                lipcoord2 = face_landmarks.landmark[lipcoord2_index]
                x = (lipcoord1.x + lipcoord2.x)/2
                y = (lipcoord1.y + lipcoord2.y)/2
                z = (lipcoord1.z + lipcoord2.z)/2
                lipless_landmarks.append(mp_containers.NormalizedLandmark(x, y, z))

            if return_as_landmark_list:
                return LandmarkList(lipless_landmarks)
            return lipless_landmarks

# def average_face_landmarks(face_landmarks_list):
#     number_of_landmarks = len(face_landmarks_list[0])
#     summed_x_coords = [0] * number_of_landmarks
#     summed_y_coords = [0] * number_of_landmarks
#     summed_z_coords = [0] * number_of_landmarks

#     for face_landmarks in face_landmarks_list:
#         for i in range(len(face_landmarks)):
#             summed_x_coords[i] += face_landmarks[i].x
#             summed_y_coords[i] += face_landmarks[i].y
#             summed_z_coords[i] += face_landmarks[i].z

#     averaged_landmarks = []
#     for i in range(len(summed_x_coords)):
#         average_x = summed_x_coords[i] / len(face_landmarks_list)
#         average_y = summed_y_coords[i] / len(face_landmarks_list)
#         average_z = summed_z_coords[i] / len(face_landmarks_list)
#         averaged_landmarks.append(mp_containers.NormalizedLandmark(average_x, average_y, average_z))

#     return LandmarkList(averaged_landmarks)

def draw_landmarks(empathizer_frame, landmarks):
    mp_drawing.draw_landmarks(
        image=empathizer_frame,
        landmark_list=landmarks,
        landmark_drawing_spec=mp_drawing.DrawingSpec(
            color=(255, 255, 255),
            thickness=2,
            circle_radius=2,
        )
    )
