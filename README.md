# The Therapeutic Efficacy of Nonverbal Feedback from Virtual Listeners

Teresa Gao

Prof. Gareth Young

Computer Science (Augmented &amp; Virtual Reality) MSc Thesis

Trinity College Dublin

## Abstract

This dissertation explores the development and evaluation of a novel virtual reality (VR) empathizer designed to provide nonverbal emotional support. Given the increasing accessibility and potential of VR for therapeutic applications, particularly in overcoming barriers associated with traditional in-person therapy, this research investigates the extent to which a virtual listener can simulate empathy and improve psychological well-being. The virtual empathizer was designed to mimic human nonverbal feedback by matching participants’ emotional expressions in real-time. A user study was conducted with various experimental conditions, including a baseline, neutral listener, and mirror condition, to assess the effectiveness of the empathizer. The study measured participants’ emotional responses using psychophysiological data, mood assessments, and subjective feedback. Results indicated no statistically significant differences in the psychological well-being of participants across the different virtual listener conditions, though heart rate changes suggested a notable difference between the neutral listener and other conditions. These findings suggest that while the virtual empathizer has potential, further refinement and exploration are needed to fully understand its impact as a therapeutic tool.

**Keywords:** human–computer interaction (HCI), virtual reality (VR), social psychology, talk therapy, human emotion, psychophysiology


## Setup

`pip install -r requirements.txt`


## Demo

`python run.py` runs the `empathizer` programs, which in turn run the `calibrator` program.

The script requires several command line arguments:

- `-pn` (`--prompt_number`) is `0`, `1`, `2`, or `3`
- `-pv` (`--pos_valence`) is `1` for true and `0` for false
- `-e` (`--empathizer`) is `d` (dot), `n` (neutral), `m` (mirror), or `e` (empathizer)

The `empathizer_` files and other `.py` scripts can be run directly individually for testing purposes.
