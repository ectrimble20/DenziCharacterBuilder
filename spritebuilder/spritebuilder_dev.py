import pygame
from spritebuilder.state.menustate import MenuState
from spritebuilder.state.builderstate import BuilderState
from spritebuilder.config import Config


class SpriteBuilderDev(object):
    """
    SpriteBuilder

    V2 - Dev

    This has been re-written as a State handler rather than the primary execution point.  This is so I can run
    different types of operations independently of one another.
    """

    def __init__(self):
        self.config = Config()
        self._display = pygame.display.set_mode((self.config.SB_SCREEN_WIDTH, self.config.SB_SCREEN_HEIGHT))
        self._running = False
        self._states = {}
        self._active_state = None
        self._delta_time = 0
        self._clock = pygame.time.Clock()
        self._trigger_state_change = False
        self._trigger_state_change_to = None
        self._initialize_states()

    def run(self):
        if self._active_state:
            self._running = True
        else:
            raise RuntimeError("Cannot run at this time, no active state")
        while self._running:
            self._display.fill((0, 0, 0))
            self._active_state.handle_input()
            self._active_state.handle_updates(self._delta_time)
            self._active_state.handle_draw(self._display)
            pygame.display.update()
            self._delta_time = self._clock.tick(self.config.SB_FPS)
            if self._trigger_state_change:  # check for and handle external state change trigger
                self._change_state()
        pygame.quit()

    def stop(self):
        # public exit interface
        self._running = False

    def _change_state(self):
        """
        Facilitates changing states, fails silently if invalid state key or no state key provided.
        :return:
        """
        if self._trigger_state_change_to:  # ensure we got a state to change to
            if self._trigger_state_change_to in self._states.keys():
                self._active_state.on_exit()
                self._active_state = self._states[self._trigger_state_change_to]
                self._active_state.on_enter()
                self._trigger_state_change = False
                self._trigger_state_change_to = None

    def _initialize_states(self):
        menu_state = MenuState(self)
        builder_state = BuilderState(self)
        self._states["main_menu"] = menu_state
        self._states["builder"] = builder_state
        self._active_state = self._states["main_menu"]
