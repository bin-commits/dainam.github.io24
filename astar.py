from heapq import heappush, heappop

CAPACITY = 4


# =========================
# GOAL
# =========================

def is_goal(state):

    for tube in state:

        if len(tube) == 0:
            continue

        if len(tube) != CAPACITY:
            return False

        if len(set(tube)) != 1:
            return False

    return True


# =========================
# HEURISTIC
# =========================

def heuristic(state):

    score = 0

    for tube in state:

        if len(tube) <= 1:
            continue

        transitions = 0

        for i in range(
            len(tube) - 1
        ):

            if tube[i] != tube[i + 1]:
                transitions += 1

        score += transitions

    return score


# =========================
# NHÓM MÀU TRÊN ĐỈNH
# =========================

def top_group_size(tube):

    if len(tube) == 0:
        return 0

    color = tube[-1]

    count = 1

    for i in range(
        len(tube) - 2,
        -1,
        -1
    ):

        if tube[i] == color:
            count += 1
        else:
            break

    return count


# =========================
# MOVE GENERATOR
# =========================

def generate_moves(state):

    result = []

    tube_count = len(state)

    for source in range(tube_count):

        if len(state[source]) == 0:
            continue

        color = state[source][-1]

        for target in range(tube_count):

            if source == target:
                continue

            target_tube = state[target]

            if len(target_tube) >= CAPACITY:
                continue

            if (
                len(target_tube) > 0
                and target_tube[-1] != color
            ):
                continue

            new_state = [
                list(t)
                for t in state
            ]

            # CHỈ MOVE 1 BÓNG
            ball = new_state[source].pop()

            new_state[target].append(
                ball
            )

            result.append(
                (
                    tuple(
                        tuple(t)
                        for t in new_state
                    ),
                    (
                        source,
                        target
                    )
                )
            )

    return result


# =========================
# SOLVER
# =========================

def solve(start_state):

    pq = []

    visited = set()

    heappush(
        pq,
        (
            heuristic(start_state),
            0,
            start_state,
            []
        )
    )

    while pq:

        (
            f,
            g,
            state,
            path
        ) = heappop(pq)

        if is_goal(state):
            return path

        if state in visited:
            continue

        visited.add(state)

        for (
            next_state,
            move
        ) in generate_moves(
            state
        ):

            if next_state in visited:
                continue

            g_new = g + 1

            h_new = heuristic(
                next_state
            )

            heappush(
                pq,
                (
                    g_new + h_new,
                    g_new,
                    next_state,
                    path + [move]
                )
            )

    return []