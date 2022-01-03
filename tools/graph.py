from tools.constants import *


class Object:
    def __init__(self, model, class_name, confidence, xmin, ymin, xmax, ymax):
        self.model = model
        self.class_name = str(class_name)
        self.confidence = float(confidence)
        self.xmin = float(xmin)
        self.ymin = float(ymin)
        self.xmax = float(xmax)
        self.ymax = float(ymax)

    def iou(self, other):
        xA = max(self.xmin, other.xmin)
        yA = max(self.ymin, other.ymin)
        xB = min(self.xmax, other.xmax)
        yB = min(self.ymax, other.ymax)
        interArea = max(0., xB - xA) * max(0., yB - yA)
        boxAArea = (self.xmax - self.xmin) * (self.ymax - self.ymin)
        boxBArea = (other.xmax - other.xmin) * (other.ymax - other.ymin)
        iou = interArea / float(boxAArea + boxBArea - interArea)
        return iou


class Cluster:
    def __init__(self, member, ):
        self.MAX_MEMBERS = MAX_MEMBERS

        self.members = [member]
        self.models = {member.model}

    def update(self, other):
        for member in other.members:
            self.members.append(member)
            self.models.add(member.model)

    def repr(self):
        confidence = sum(member.confidence for member in self.members)
        xmin = sum(member.xmin * member.confidence for member in self.members) / confidence
        ymin = sum(member.ymin * member.confidence for member in self.members) / confidence
        xmax = sum(member.xmax * member.confidence for member in self.members) / confidence
        ymax = sum(member.ymax * member.confidence for member in self.members) / confidence
        confidence /= MAX_MEMBERS
        return Object(model='FUSE', class_name=self.members[0].class_name, confidence=confidence,
                      xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
