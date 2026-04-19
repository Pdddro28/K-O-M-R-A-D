from dataclasses import dataclass

# Region Of Interest:
#
#  x1,y1----------------
#  |                    |
#  |                    |
#  |                    |
#  -------------------x2,y2

@dataclass
class ROI:
    """Recive two points from the frame  to extract the Region Of Interest"""

    x1: int; y1: int
    x2: int; y2: int


rois = [
    ROI(115, 17, 365, 201),
    ROI(436, 34, 754, 97),
]
