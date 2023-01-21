from abc import abstractmethod
from random import randint


class StateMachine:
    def __init__(self):
        self.reset()

    def set_complete(self) -> None:
        self._complete = True

    def set_result(self, new_result) -> None:
        self._result = new_result

    def set_next_state(self, next_state) -> None:
        self._state = next_state

    def reset(self):
        self._state = self.state_initial
        self._result = None
        self._complete = False

    def get_current_state(self):
        return self._state.__name__

    def final_state(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.set_complete()
            print("Set StateMachine to 'complete'")
        return wrapper

    def is_complete(self) -> bool:
        return self._complete

    def step(self) -> None:
        state_func = self._state
        state_func(self._result)

    def run(self):
        while True:
            self.step()
            if self.is_complete():
                break

    @abstractmethod
    def state_initial(self):
        ...


class SimpleStateMachine(StateMachine):
    def __init__(self):
        super().__init__()
    
    def state_initial(self, val):
        print("In state 'state_initial'")
        print(f" - val is {val}")
        self.set_next_state(self.state_two)
        self.set_result(0)

    def state_two(self, val):
        print("In state 'state_two'")
        print(f" - val is {val}")
        i = randint(1, 10)
        print(f" - add {i}")
        val += i
        if val < 5:
            self.set_next_state(self.state_three)
        elif val >= 5:
            self.set_next_state(self.state_four)
        self.set_result(val)

    def state_three(self, val):
        print("In state 'state_three'")
        print(f" - val is {val}")
        print(" - add 5")
        val += 5
        self.set_next_state(self.state_final)
        self.set_result(val)

    def state_four(self, val):
        print("In state 'state_four'")
        print(f" - val is {val}")
        print(" - subtract 3")
        val -= 3
        self.set_next_state(self.state_final)
        self.set_result(val)

    @StateMachine.final_state
    def state_final(self, val):
        print("In state 'state_final'")
        print(f" - final val is {val}")


def main():
    ssm = SimpleStateMachine()
    ssm.run()

main()
