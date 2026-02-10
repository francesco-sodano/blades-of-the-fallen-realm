"""Tests for the AnimationController and AnimationData classes."""

import pygame

from blades_of_the_fallen_realm.engine.animation import (
    AnimationController,
    AnimationData,
)


def _make_frames(count: int) -> list[pygame.Rect]:
    """Create *count* dummy frame rects for testing."""
    return [pygame.Rect(i * 32, 0, 32, 32) for i in range(count)]


# ---------------------------------------------------------------------------
# AnimationData defaults
# ---------------------------------------------------------------------------


def test_animation_data_defaults() -> None:
    """AnimationData should have sensible defaults."""
    data = AnimationData(frames=_make_frames(3), frame_duration=100.0)
    assert data.loop is True
    assert data.one_shot is False
    assert data.callbacks == {}


# ---------------------------------------------------------------------------
# play() switches animation
# ---------------------------------------------------------------------------


def test_play_switches_animation() -> None:
    """play() should set current_animation and reset counters."""
    ctrl = AnimationController(
        {
            "IDLE": AnimationData(frames=_make_frames(2), frame_duration=100.0),
            "WALK": AnimationData(frames=_make_frames(4), frame_duration=80.0),
        }
    )
    ctrl.play("IDLE")
    assert ctrl.current_animation == "IDLE"
    assert ctrl.current_frame == 0

    ctrl.play("WALK")
    assert ctrl.current_animation == "WALK"
    assert ctrl.current_frame == 0


def test_play_same_animation_is_noop() -> None:
    """Calling play() with the same state should not reset the animation."""
    ctrl = AnimationController(
        {"IDLE": AnimationData(frames=_make_frames(4), frame_duration=100.0)}
    )
    ctrl.play("IDLE")
    ctrl.update(150.0)  # advance to frame 1
    assert ctrl.current_frame == 1

    ctrl.play("IDLE")  # same state — should be a no-op
    assert ctrl.current_frame == 1


# ---------------------------------------------------------------------------
# update() advances frames correctly
# ---------------------------------------------------------------------------


def test_update_advances_frames() -> None:
    """update() should advance to the next frame after frame_duration elapses."""
    ctrl = AnimationController(
        {"IDLE": AnimationData(frames=_make_frames(4), frame_duration=100.0)}
    )
    ctrl.play("IDLE")

    ctrl.update(50.0)
    assert ctrl.current_frame == 0  # not enough time

    ctrl.update(50.0)
    assert ctrl.current_frame == 1  # exactly one frame duration

    ctrl.update(250.0)
    assert (
        ctrl.current_frame == 3
    )  # skip ahead by two more frames (100+100 consumed, 50 remaining)


def test_update_without_play_is_noop() -> None:
    """update() before play() should not crash."""
    ctrl = AnimationController(
        {"IDLE": AnimationData(frames=_make_frames(2), frame_duration=100.0)}
    )
    ctrl.update(200.0)  # no current_animation set — should be safe


# ---------------------------------------------------------------------------
# One-shot animations stop at last frame
# ---------------------------------------------------------------------------


def test_one_shot_stops_at_last_frame() -> None:
    """A one-shot animation should stop at the last frame."""
    ctrl = AnimationController(
        {
            "DEATH": AnimationData(
                frames=_make_frames(3),
                frame_duration=100.0,
                loop=False,
                one_shot=True,
            )
        }
    )
    ctrl.play("DEATH")
    ctrl.update(500.0)  # more than enough to play through all frames
    assert ctrl.current_frame == 2
    assert ctrl.is_finished() is True


def test_one_shot_does_not_advance_past_last_frame() -> None:
    """Further updates should keep a finished one-shot on the last frame."""
    ctrl = AnimationController(
        {
            "DEATH": AnimationData(
                frames=_make_frames(3),
                frame_duration=100.0,
                loop=False,
                one_shot=True,
            )
        }
    )
    ctrl.play("DEATH")
    ctrl.update(1000.0)
    ctrl.update(1000.0)
    assert ctrl.current_frame == 2
    assert ctrl.is_finished() is True


# ---------------------------------------------------------------------------
# Looping animations restart from frame 0
# ---------------------------------------------------------------------------


def test_looping_animation_wraps_around() -> None:
    """A looping animation should restart from frame 0 after the last frame."""
    ctrl = AnimationController(
        {"WALK": AnimationData(frames=_make_frames(3), frame_duration=100.0, loop=True)}
    )
    ctrl.play("WALK")
    ctrl.update(300.0)  # plays through all 3 frames → wraps to 0
    assert ctrl.current_frame == 0
    assert ctrl.is_finished() is False


def test_looping_animation_is_never_finished() -> None:
    """is_finished() should always return False for a looping animation."""
    ctrl = AnimationController(
        {"IDLE": AnimationData(frames=_make_frames(2), frame_duration=100.0, loop=True)}
    )
    ctrl.play("IDLE")
    ctrl.update(5000.0)
    assert ctrl.is_finished() is False


# ---------------------------------------------------------------------------
# Frame callbacks fire at the correct frame
# ---------------------------------------------------------------------------


def test_frame_callbacks_triggered() -> None:
    """Callbacks registered for a frame index should fire when that frame is reached."""
    triggered: list[int] = []

    ctrl = AnimationController(
        {
            "ATTACK1": AnimationData(
                frames=_make_frames(4),
                frame_duration=100.0,
                loop=False,
                one_shot=True,
                callbacks={
                    1: lambda: triggered.append(1),
                    3: lambda: triggered.append(3),
                },
            )
        }
    )
    ctrl.play("ATTACK1")
    ctrl.update(400.0)  # play through all 4 frames

    assert 1 in triggered
    assert 3 in triggered


def test_callback_not_triggered_before_frame() -> None:
    """A callback should not fire before its frame index is reached."""
    triggered: list[int] = []

    ctrl = AnimationController(
        {
            "ATTACK1": AnimationData(
                frames=_make_frames(4),
                frame_duration=100.0,
                loop=False,
                one_shot=True,
                callbacks={2: lambda: triggered.append(2)},
            )
        }
    )
    ctrl.play("ATTACK1")
    ctrl.update(150.0)  # only reaches frame 1
    assert 2 not in triggered


# ---------------------------------------------------------------------------
# get_current_frame returns the correct Rect
# ---------------------------------------------------------------------------


def test_get_current_frame_returns_correct_rect() -> None:
    """get_current_frame() should return the Rect for the active frame."""
    frames = _make_frames(3)
    ctrl = AnimationController(
        {"IDLE": AnimationData(frames=frames, frame_duration=100.0)}
    )
    ctrl.play("IDLE")
    assert ctrl.get_current_frame() == frames[0]

    ctrl.update(100.0)
    assert ctrl.get_current_frame() == frames[1]


# ---------------------------------------------------------------------------
# is_finished() returns correct status
# ---------------------------------------------------------------------------


def test_is_finished_false_initially() -> None:
    """is_finished() should be False right after play()."""
    ctrl = AnimationController(
        {
            "DEATH": AnimationData(
                frames=_make_frames(3),
                frame_duration=100.0,
                one_shot=True,
                loop=False,
            )
        }
    )
    ctrl.play("DEATH")
    assert ctrl.is_finished() is False


def test_is_finished_true_only_for_completed_one_shot() -> None:
    """is_finished() should return True only when a one-shot finishes."""
    ctrl = AnimationController(
        {
            "DEATH": AnimationData(
                frames=_make_frames(3),
                frame_duration=100.0,
                one_shot=True,
                loop=False,
            ),
            "IDLE": AnimationData(
                frames=_make_frames(2),
                frame_duration=100.0,
                loop=True,
            ),
        }
    )
    ctrl.play("IDLE")
    ctrl.update(5000.0)
    assert ctrl.is_finished() is False

    ctrl.play("DEATH")
    ctrl.update(5000.0)
    assert ctrl.is_finished() is True
