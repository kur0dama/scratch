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
    def illegal(west: int, east: int) -> bool:
        return west in ILLEGAL_STATES or east in ILLEGAL_STATES

    def move_boat(west: int, east: int) -> GameState:
        return (west ^ BOAT, east ^ BOAT)

    def move_obj(west: int, east: int, obj: int) -> GameState:
        return (west ^ BOAT ^ obj, east ^ BOAT ^ obj)

    def inner_loop(west: int, east: int, states: list[GameState]):
        states += [(west, east)]
        if east == FULL:
            _print_states(states)
            return
        from_side = west if (west & BOAT > 0) else east
        for obj in [CABBAGE, SHEEP, WOLF]:
            if from_side & obj > 0:
                new_state = move_obj(west, east, obj)
                if not (illegal(*new_state) or new_state in states):
                    inner_loop(*new_state, states)
        new_state = move_boat(west, east)
        if not (illegal(*new_state) or new_state in states):
            inner_loop(*move_boat(west, east), states)

    inner_loop(FULL, EMPTY, [])


sim()

#   WSC | B  \\\\\    |
#   W C |    /////  B |  S
#   W C | B  \\\\\    |  S
#   W   |    /////  B |  SC
#   WS  | B  \\\\\    |   C
#    S  |    /////  B | W C
#    S  | B  \\\\\    | W C
#       |    /////  B | WSC
