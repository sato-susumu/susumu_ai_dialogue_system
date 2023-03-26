from enum import Enum


class Emotion(Enum):
    # ref: https://vrm.dev/vrm1/changed.html#vrmc-vrm-expression
    HAPPY = 'happy'
    SAD = 'sad'
    SURPRISED = 'surprised'
    ANGRY = 'angry'
    RELAXED = 'relaxed'
