class Node:
    pass


def overlap(head1: Node, head2: Node) -> bool:
    p1, p2, p3, p4 = head1, head1, head2, head2

    cycle1, cycle2, overlap = False, False, False

    def selfCycleDetect(pa: Node, pb: Node) -> bool:
        while True:
            if pa.nextNode:
                pa = pa.nextNode
            else:
                return False
            if pb.nextNode and pb.nextNode.nextNode:
                pb = pb.nextNode.nextNode
            else:
                return False
            if pa == pb:
                return True
        return False

    cycle1 = selfCycleDetect(p1, p2)
    cycle2 = selfCycleDetect(p3, p4)

    p1, p4 = head1, head2  # p1: x1; p4: x2
    if not cycle1 and not cycle2:
        while True:
            if p1.nextNode:
                p1 = p1.nextNode
            else:
                break
        while True:
            if p4.nextNode:
                p4 = p4.nextNode
            else:
                break
        return p1 == p4
    elif (not cycle1 and cycle2) or (cycle1 and not cycle2):
        return False
    else:
        pa, pb = p1, p4
        while True:
            pa = pa.nextNode
            pb = pb.nextNode.nextNode
            if pa == pb:
                return True
            if pa == p3:
                return True
    return False
