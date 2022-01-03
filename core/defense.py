from tools.graph import *
from tools.constants import *
import itertools


def fuse(candidates):
    # Step 1: Group candidate objects by class
    cls2candidates = {}
    for candidate in candidates:
        if candidate.class_name not in cls2candidates:
            cls2candidates[candidate.class_name] = []
        cls2candidates[candidate.class_name].append(candidate)

    # Step 2: Per-class object detection fusion
    fusion_results = []
    for class_name, candidates in cls2candidates.items():
        fusion_results += _fuse(candidates)
    return fusion_results


def _fuse(candidates):
    candidates = sorted(candidates, key=lambda candidate: -candidate.confidence)

    edges, edges_set = [], []
    for v1, v2 in itertools.combinations(candidates, r=2):
        iou = v1.iou(v2)
        if v1.model == v2.model or iou < IOU_THRESHOLD:
            continue
        edges.append((v1, v2, iou))
        edges_set.append({v1, v2})
    edges = sorted(edges, key=lambda e: -e[2])

    candidate2cluster = {candidate: Cluster(member=candidate) for candidate in candidates}
    for edge in edges:
        cluster1 = candidate2cluster[edge[0]]
        cluster2 = candidate2cluster[edge[1]]
        is_disjoint = cluster1.models.isdisjoint(cluster2.models)
        is_connectable = True
        for m1, m2 in itertools.product(cluster1.members, cluster2.members):
            if {m1, m2} not in edges_set:
                is_connectable = False
                break
        if is_disjoint and is_connectable:
            cluster1.update(cluster2)
            for member in cluster2.members:
                candidate2cluster[member] = cluster1

    return [cluster.repr() for cluster in set(candidate2cluster.values())]
