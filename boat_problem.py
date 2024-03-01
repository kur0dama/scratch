BOAT: int = 1 << 0
CABBAGE: int = 1 << 1
SHEEP: int = 1 << 2
WOLF: int = 1 << 3

EMPTY: int = 0
FULL: int = BOAT | CABBAGE | SHEEP | WOLF

ILLEGAL_STATES: list[int] = [CABBAGE | SHEEP, SHEEP | WOLF]

GameState = tuple[int, int]


def _pprint_state(state: GameState, wave_direction: int = 0) -> None:
    def f(i: str, s: str) -> str:
        return " " if i == "0" else s

    river_char = "/" if wave_direction else "\\"
    fmt = "{0:04b}"
    LR = tuple(fmt.format(x) for x in state)
    ((LW, LS, LC, LB), (RW, RS, RC, RB)) = LR
    left = f"{f(LW,'W')}{f(LS,'S')}{f(LC,'C')} | {f(LB,'B')}"
    right = f"{f(RB,'B')} | {f(RW,'W')}{f(RS,'S')}{f(RC,'C')}"
    river = river_char * 5
    print(f"{left}  {river}  {right}")


def _print_states(states: list[GameState]) -> None:
    i = 0
    for state in states:
        _pprint_state(state, i)
        i ^= 1


def sim() -> None:
    def illegal(state: GameState) -> bool:
        return any(s in ILLEGAL_STATES for s in state)

    def move_boat(state: GameState) -> GameState:
        return tuple(s ^ BOAT for s in state)

    def move_obj(state: GameState, obj: int) -> GameState:
        return tuple(s ^ BOAT ^ obj for s in state)

    def inner_loop(state: GameState, cache: list[GameState]):
        cache += [state]
        if state[1] == FULL:
            _print_states(cache)
            return
        from_side = state[0] if (state[0] & BOAT > 0) else state[1]
        for obj in [CABBAGE, SHEEP, WOLF]:
            if from_side & obj > 0:
                new_state = move_obj(state, obj)
                if not (illegal(new_state) or new_state in cache):
                    inner_loop(new_state, cache)
        new_state = move_boat(state)
        if not (illegal(new_state) or new_state in cache):
            inner_loop(new_state, cache)

    inner_loop((FULL, EMPTY), [])


sim()

#   WSC | B  \\\\\    |
#   W C |    /////  B |  S
#   W C | B  \\\\\    |  S
#   W   |    /////  B |  SC
#   WS  | B  \\\\\    |   C
#    S  |    /////  B | W C
#    S  | B  \\\\\    | W C
#       |    /////  B | WSC
