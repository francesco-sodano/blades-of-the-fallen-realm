"""Tests verifying all packages and module stubs are importable."""

import importlib


def test_import_engine_modules() -> None:
    """Verify all engine modules are importable."""
    modules = [
        "blades_of_the_fallen_realm.engine",
        "blades_of_the_fallen_realm.engine.game",
        "blades_of_the_fallen_realm.engine.camera",
        "blades_of_the_fallen_realm.engine.input_handler",
        "blades_of_the_fallen_realm.engine.collision",
        "blades_of_the_fallen_realm.engine.renderer",
        "blades_of_the_fallen_realm.engine.animation",
    ]
    for mod in modules:
        importlib.import_module(mod)


def test_import_entity_modules() -> None:
    """Verify all entity modules are importable."""
    modules = [
        "blades_of_the_fallen_realm.entities",
        "blades_of_the_fallen_realm.entities.base_entity",
        "blades_of_the_fallen_realm.entities.player",
        "blades_of_the_fallen_realm.entities.enemy",
        "blades_of_the_fallen_realm.entities.mount",
        "blades_of_the_fallen_realm.entities.pickup",
    ]
    for mod in modules:
        importlib.import_module(mod)


def test_import_character_modules() -> None:
    """Verify all character modules are importable."""
    modules = [
        "blades_of_the_fallen_realm.characters",
        "blades_of_the_fallen_realm.characters.theron",
        "blades_of_the_fallen_realm.characters.sylara",
        "blades_of_the_fallen_realm.characters.drunn",
    ]
    for mod in modules:
        importlib.import_module(mod)


def test_import_enemy_modules() -> None:
    """Verify all enemy modules are importable."""
    modules = [
        "blades_of_the_fallen_realm.enemies",
        "blades_of_the_fallen_realm.enemies.bogwort_grunt",
        "blades_of_the_fallen_realm.enemies.bogwort_archer",
        "blades_of_the_fallen_realm.enemies.bogwort_witch",
        "blades_of_the_fallen_realm.enemies.snarlfang_rider",
        "blades_of_the_fallen_realm.enemies.ironhide_brute",
        "blades_of_the_fallen_realm.enemies.ironhide_ravager",
        "blades_of_the_fallen_realm.enemies.stone_troll",
        "blades_of_the_fallen_realm.enemies.bosses",
        "blades_of_the_fallen_realm.enemies.bosses.hollow_king",
        "blades_of_the_fallen_realm.enemies.bosses.gravelord_thusk",
        "blades_of_the_fallen_realm.enemies.bosses.gorath",
        "blades_of_the_fallen_realm.enemies.bosses.dark_wardens_fist",
        "blades_of_the_fallen_realm.enemies.bosses.voice_of_shadow",
    ]
    for mod in modules:
        importlib.import_module(mod)


def test_import_level_modules() -> None:
    """Verify all level modules are importable."""
    modules = [
        "blades_of_the_fallen_realm.levels",
        "blades_of_the_fallen_realm.levels.base_level",
        "blades_of_the_fallen_realm.levels.level1_stormwatch",
        "blades_of_the_fallen_realm.levels.level2_ironroot",
        "blades_of_the_fallen_realm.levels.level3_broken_shore",
        "blades_of_the_fallen_realm.levels.level4_bastion_keep",
        "blades_of_the_fallen_realm.levels.level5_shadow_gate",
        "blades_of_the_fallen_realm.levels.camp_scene",
    ]
    for mod in modules:
        importlib.import_module(mod)


def test_import_ui_modules() -> None:
    """Verify all UI modules are importable."""
    modules = [
        "blades_of_the_fallen_realm.ui",
        "blades_of_the_fallen_realm.ui.hud",
        "blades_of_the_fallen_realm.ui.main_menu",
        "blades_of_the_fallen_realm.ui.pause_menu",
        "blades_of_the_fallen_realm.ui.game_over",
    ]
    for mod in modules:
        importlib.import_module(mod)


def test_import_utils_modules() -> None:
    """Verify all utils modules are importable."""
    modules = [
        "blades_of_the_fallen_realm.utils",
        "blades_of_the_fallen_realm.utils.spritesheet",
        "blades_of_the_fallen_realm.utils.tilemap",
        "blades_of_the_fallen_realm.utils.debug",
    ]
    for mod in modules:
        importlib.import_module(mod)


def test_engine_package_import_camera() -> None:
    """Verify Camera is importable from the engine package."""
    from blades_of_the_fallen_realm.engine import Camera

    assert Camera is not None


def test_engine_package_import_game() -> None:
    """Verify Game and GameState are importable from the engine package."""
    from blades_of_the_fallen_realm.engine import Game, GameState

    assert Game is not None
    assert GameState is not None


def test_engine_package_import_input_handler() -> None:
    """Verify InputHandler is importable from the engine package."""
    from blades_of_the_fallen_realm.engine import InputHandler

    assert InputHandler is not None


def test_engine_package_import_renderer() -> None:
    """Verify Renderer is importable from the engine package."""
    from blades_of_the_fallen_realm.engine import Renderer

    assert Renderer is not None


def test_engine_package_import_animation() -> None:
    """Verify AnimationController and AnimationData are importable from the engine package."""
    from blades_of_the_fallen_realm.engine import AnimationController, AnimationData

    assert AnimationController is not None
    assert AnimationData is not None


def test_entities_package_import_base_entity() -> None:
    """Verify BaseEntity is importable from the entities package."""
    from blades_of_the_fallen_realm.entities import BaseEntity

    assert BaseEntity is not None
