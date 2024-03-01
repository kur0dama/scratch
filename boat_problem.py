BOAT: int = 1 << 0
CABBAGE: int = 1 << 1
SHEEP: int = 1 << 2
WOLF: int = 1 << 3

EMPTY: int = 0
FULL: int = BOAT | CABBAGE | SHEEP | WOLF

ILLEGAL_STATES: list[int] = [CABBAGE | SHEEP, SHEEP | WOLF]


def _pprint_state(x: int, wave_direction: int = 0) -> None:
    def f(i: str, s: str) -> str:
        return " " if i == "0" else s

    river_char = "/" if wave_direction else "\\"
    fmt = "{0:04b}"
    LR = tuple(fmt.format(y) for y in (x, x ^ FULL))
    ((LW, LS, LC, LB), (RW, RS, RC, RB)) = LR
    left = f"{f(LW,'W')}{f(LS,'S')}{f(LC,'C')} | {f(LB,'B')}"
    right = f"{f(RB,'B')} | {f(RW,'W')}{f(RS,'S')}{f(RC,'C')}"
    river = river_char * 5
    print(f"{left}  {river}  {right}")


def _pprint(xs: list[int]) -> None:
    i = 0
    for x in xs:
        _pprint_state(x, i)
        i ^= 1


def sim() -> None:
    def illegal(x: int) -> bool:
        return x in ILLEGAL_STATES or (x ^ FULL) in ILLEGAL_STATES

    def inner_loop(x: int, xs: list[int]):
        xs += [x]
        if x ^ FULL == FULL:
            _pprint(xs)
            return
        from_side = x if (x & BOAT > 0) else x ^ FULL
        for obj in [CABBAGE, SHEEP, WOLF]:
            if from_side & obj > 0:
                new_x = x ^ BOAT ^ obj
                if not (illegal(new_x) or new_x in xs):
                    inner_loop(new_x, xs)
        new_x = x ^ BOAT
        if not (illegal(new_x) or new_x in xs):
            inner_loop(new_x, xs)

    inner_loop(FULL, [])


sim()

#   WSC | B  \\\\\    |
#   W C |    /////  B |  S
#   W C | B  \\\\\    |  S
#   W   |    /////  B |  SC
#   WS  | B  \\\\\    |   C
#    S  |    /////  B | W C
#    S  | B  \\\\\    | W C
#       |    /////  B | WSC
