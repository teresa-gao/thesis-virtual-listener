from argparse import ArgumentParser

from calibrator import run_calibration
from empathizer_dot import run_empathizer_dot
from empathizer_neutral import run_empathizer_neutral
from empathizer_empathy import run_empathizer_empathy


duration = 60
empathizer_delay = 15

positive_valence_prompts = [
    'Talk about something that you are excited about.',
    'Talk about the last thing that made you smile.',
    'Talk about a recent good day that you had.',
    'Talk about something that makes you feel happy.',
]

negative_valence_prompts = [
    'Talk about something that you are worried about.',
    'Talk about the last thing that made you cry.',
    'Talk about a recent bad day that you had.',
    'Talk about something that makes you feel sad.',
]

empathizers = {
    'd': (run_empathizer_dot,     0),                # dot only
    'n': (run_empathizer_neutral, 0),                # neutral face
    'm': (run_empathizer_empathy, 0),                # mirrored face
    'e': (run_empathizer_empathy, empathizer_delay), # empathizer
}


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-pn', '--prompt_number', help='Number between 0 and 3 (inclusive)', type=int, required=True)
    parser.add_argument('-pv', '--pos_valence', help='1 for true, 0 for false', type=int, required=True)
    parser.add_argument('-e', '--empathizer', help='d", "n", "m", or "e" (without quotation marks)',required=True)

    args = parser.parse_args()
    empathizer, frame_delay = empathizers[args.empathizer]
    if args.pos_valence:
        empathizer(positive_valence_prompts[args.prompt_number], total_seconds=duration, frame_delay=frame_delay)
    else:
        empathizer(negative_valence_prompts[args.prompt_number], total_seconds=duration, frame_delay=frame_delay)
