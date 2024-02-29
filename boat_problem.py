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


class Game:
    def __init__(self) -> None:
        self.west: int = FULL
        self.east: int = EMPTY
        self.save_states: list[GameState] = [(self.west, self.east)]

    def _get_boat_side(self) -> int:
        return self.west if (self.west & BOAT > 0) else self.east

    def _set_states(self, west: int, east: int) -> None:
        self.west = west
        self.east = east
        self._log_states()

    def _log_states(self) -> None:
        self.save_states += [(self.west, self.east)]

    def _is_illegal(self, west, east) -> bool:
        return west in ILLEGAL_STATES or east in ILLEGAL_STATES

    def _is_repeat(self, west, east) -> bool:
        return (west, east) in self.save_states

    def _shift_boat(self) -> bool:
        new_west = self.west ^ BOAT
        new_east = self.east ^ BOAT
        if self._is_illegal(new_west, new_east):
            return False
        self._set_states(new_west, new_east)
        return True

    def _shift_obj(self, obj: int) -> bool:
        new_west = self.west ^ BOAT ^ obj
        new_east = self.east ^ BOAT ^ obj
        is_illegal_state = self._is_repeat(new_west, new_east)
        is_repeat_state = self._is_illegal(new_west, new_east)
        if is_illegal_state or is_repeat_state:
            return False
        self._set_states(new_west, new_east)
        return True

    def run(self) -> None:
        i = 0
        while True:
            from_side = self._get_boat_side()
            for obj in [CABBAGE, SHEEP, WOLF]:
                if from_side & obj > 0:
                    if self._shift_obj(obj):
                        break
            if self.east == FULL:
                for state in self.save_states:
                    _pprint_state(state, i)
                    i ^= 1
                return
            self._shift_boat()


Game().run()

#     WSC | B  \\\\\    |
#     W C |    /////  B |  S
#     W C | B  \\\\\    |  S
#     W   |    /////  B |  SC
#     WS  | B  \\\\\    |   C
#      S  |    /////  B | W C
#      S  | B  \\\\\    | W C
#         |    /////  B | WSC
