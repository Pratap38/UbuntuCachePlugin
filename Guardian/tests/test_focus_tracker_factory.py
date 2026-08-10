from Guardian.Focus.FocusTrackerFactory import FocusTrackerFactory
from Guardian.Focus.FocusTrackerWayland import FocusTrackerWayland
from Guardian.models.DesktopEnvironment import DesktopEnv


def test_wayland_factory():
    tracker = FocusTrackerFactory.create(
        DesktopEnv.WAYLAND
    )

    assert isinstance(
        tracker,
        FocusTrackerWayland
    )


def test_x11_factory():
    try:
        FocusTrackerFactory.create(
            DesktopEnv.x11
        )
    except NotImplementedError:
        return

    raise AssertionError(
        "X11 tracker should not be created before X11 "
        "focus tracking is implemented."
    )


def test_unknown_factory():
    try:
        FocusTrackerFactory.create(
            DesktopEnv.UNKNOWN
        )
    except RuntimeError:
        return

    raise AssertionError(
        "Unknown desktop environment should be rejected."
    )


if __name__ == "__main__":
    test_wayland_factory()
    test_x11_factory()
    test_unknown_factory()

    print("FocusTrackerFactory tests: PASS")