"""Spritesheet-based animation controller with state-driven frame playback."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

import pygame


@dataclass
class AnimationData:
    """Data for a single animation sequence on a spritesheet.

    Attributes:
        frames: List of frame rectangles on the spritesheet.
        frame_duration: Milliseconds per frame.
        loop: Whether the animation loops after reaching the last frame.
        one_shot: Plays once and stops at the last frame.
        callbacks: Mapping of frame index to a callback function
            (e.g., hitbox activation).
    """

    frames: list[pygame.Rect]
    frame_duration: float
    loop: bool = True
    one_shot: bool = False
    callbacks: dict[int, Callable[[], None]] = field(default_factory=dict)


class AnimationController:
    """Manages spritesheet-based animations keyed by state strings.

    Typical state names include ``IDLE``, ``WALK``, ``ATTACK1``, ``JUMP``,
    ``HIT``, ``DEATH``, etc.  Each state maps to an :class:`AnimationData`
    instance that describes which frames to play and how.
    """

    def __init__(self, animations: dict[str, AnimationData]) -> None:
        """Initialize the animation controller.

        Args:
            animations: Mapping of state name to animation data.
        """
        self.animations: dict[str, AnimationData] = animations
        self.current_animation: str = ""
        self.current_frame: int = 0
        self.elapsed: float = 0.0
        self._finished: bool = False

    def play(self, state_name: str) -> None:
        """Switch to the named animation and reset the frame counter.

        If *state_name* is already playing the call is a no-op so that
        callers can invoke ``play`` every tick without resetting the
        animation.

        Args:
            state_name: Key into the animations dictionary.
        """
        if state_name == self.current_animation:
            return
        self.current_animation = state_name
        self.current_frame = 0
        self.elapsed = 0.0
        self._finished = False

    def update(self, dt: float) -> None:
        """Advance the animation based on elapsed time.

        Args:
            dt: Delta time in milliseconds since the last update.
        """
        if not self.current_animation:
            return

        anim = self.animations[self.current_animation]

        if self._finished:
            return

        self.elapsed += dt

        while self.elapsed >= anim.frame_duration:
            self.elapsed -= anim.frame_duration
            previous_frame = self.current_frame
            next_frame = self.current_frame + 1

            if next_frame >= len(anim.frames):
                if anim.one_shot:
                    self.current_frame = len(anim.frames) - 1
                    self._finished = True
                    self.elapsed = 0.0
                    break
                elif anim.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(anim.frames) - 1
                    self._finished = True
                    self.elapsed = 0.0
                    break
            else:
                self.current_frame = next_frame

            # Fire callback for the new frame if one is registered.
            if (
                self.current_frame != previous_frame
                and self.current_frame in anim.callbacks
            ):
                anim.callbacks[self.current_frame]()

    def get_current_frame(self) -> pygame.Rect:
        """Return the rectangle for the current frame on the spritesheet.

        Returns:
            The :class:`pygame.Rect` for the current frame.

        Raises:
            RuntimeError: If no animation has been started via :meth:`play`.
        """
        if not self.current_animation:
            raise RuntimeError(
                "No animation is playing. Call play() before get_current_frame()."
            )
        anim = self.animations[self.current_animation]
        return anim.frames[self.current_frame]

    def is_finished(self) -> bool:
        """Return whether the current animation has finished.

        A looping animation is never considered finished.  A one-shot
        animation is finished once it has played through all frames and
        stopped on the last one.

        Returns:
            ``True`` if the animation is a one-shot that has completed.
        """
        return self._finished
