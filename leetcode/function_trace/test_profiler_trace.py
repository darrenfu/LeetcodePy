import pytest
from function_trace.trace import Sample, Event, convert_base
from function_trace.trace_with_hysteresis import convert_with_hysteresis


N = 2  # hysteresis threshold


def test_simple_nested_call_base_and_hysteresis():
    """
    Test 1:
    main -> main,A -> main

    Base: A ends at t=3.
    Hysteresis (N=2): A only disappears once; if we do not flush at the end,
    no end(A) is emitted.
    """
    samples = [
        Sample(1, ["main"]),
        Sample(2, ["main", "A"]),
        Sample(3, ["main"]),
    ]

    expected_base = [
        Event("start", 1, "main"),
        Event("start", 2, "A"),
        Event("end",   3, "A"),
    ]

    expected_hyst = [
        Event("start", 1, "main"),
        Event("start", 2, "A"),
        # No end(A) because A only disappeared once (missing_count == 1 < N)
    ]

    base_events = convert_base(samples)
    hyst_events = convert_with_hysteresis(samples, N)

    assert base_events == expected_base
    print(type(expected_hyst[0]), type(hyst_events[0]))
    print(expected_hyst[0].__class__.__module__, expected_hyst[0].__class__.__qualname__)
    print(hyst_events[0].__class__.__module__, hyst_events[0].__class__.__qualname__)
    assert hyst_events == expected_hyst


def test_short_glitch_then_real_exit():
    """
    Test 2:
    A is actually continuous, but disappears once due to sampling noise,
    then later really exits.

    t1: main,A
    t2: main        (glitch)
    t3: main,A      (A reappears)
    t4: main        (start of real exit)
    t5: main        (confirm exit)

    Base: emits extra end/start events due to the glitch.
    Hysteresis: smooths the glitch and emits a single end(A) at t=5.
    """
    samples = [
        Sample(1, ["main", "A"]),
        Sample(2, ["main"]),
        Sample(3, ["main", "A"]),
        Sample(4, ["main"]),
        Sample(5, ["main"]),
    ]

    expected_base = [
        Event("start", 1, "main"),
        Event("start", 1, "A"),
        Event("end",   2, "A"),   # misinterpretation of glitch as real end
        Event("start", 3, "A"),
        Event("end",   4, "A"),
    ]

    expected_hyst = [
        Event("start", 1, "main"),
        Event("start", 1, "A"),
        # no extra end/start for the glitch
        Event("end",   5, "A"),
    ]

    base_events = convert_base(samples)
    hyst_events = convert_with_hysteresis(samples, N)

    assert base_events == expected_base
    assert hyst_events == expected_hyst


def test_real_exit_with_delayed_confirmation():
    """
    Test 3:
    A really exits and never comes back, but hysteresis only confirms it
    after N consecutive missing samples.

    t1: main,A
    t2: main      (A gone)
    t3: main      (A still gone)

    Base: end(A) at t=2.
    Hysteresis: end(A) at t=3 (after 2 consecutive misses).
    """
    samples = [
        Sample(1, ["main", "A"]),
        Sample(2, ["main"]),
        Sample(3, ["main"]),
    ]

    expected_base = [
        Event("start", 1, "main"),
        Event("start", 1, "A"),
        Event("end",   2, "A"),
    ]

    expected_hyst = [
        Event("start", 1, "main"),
        Event("start", 1, "A"),
        Event("end",   3, "A"),  # delayed confirmation
    ]

    base_events = convert_base(samples)
    hyst_events = convert_with_hysteresis(samples, N)

    assert base_events == expected_base
    assert hyst_events == expected_hyst


def test_structure_change_main_A_to_main_B():
    """
    Test 4:
    Structural change: main,A -> main,B.

    This is not just a shorter prefix; the frame at depth 1 changed from A to B.
    Both algorithms should eagerly end A and start B at t=2.
    """
    samples = [
        Sample(1, ["main", "A"]),
        Sample(2, ["main", "B"]),
    ]

    expected_events = [
        Event("start", 1, "main"),
        Event("start", 1, "A"),
        Event("end",   2, "A"),
        Event("start", 2, "B"),
    ]

    base_events = convert_base(samples)
    hyst_events = convert_with_hysteresis(samples, N)

    assert base_events == expected_events
    assert hyst_events == expected_events


def test_simple_growth_main_to_main_A_to_main_A_B():
    """
    Test 5:
    Pure stack growth, no truncation, no structure change.

    t1: main
    t2: main,A
    t3: main,A,B

    Base and hysteresis should produce identical start events only.
    """
    samples = [
        Sample(1, ["main"]),
        Sample(2, ["main", "A"]),
        Sample(3, ["main", "A", "B"]),
    ]

    expected_events = [
        Event("start", 1, "main"),
        Event("start", 2, "A"),
        Event("start", 3, "B"),
    ]

    base_events = convert_base(samples)
    hyst_events = convert_with_hysteresis(samples, N)

    assert base_events == expected_events
    assert hyst_events == expected_events


def test_no_change_same_stack_repeated():
    """
    Test 6:
    Stack is identical across samples. Only the first sample should generate
    start events; subsequent samples generate nothing in both algorithms.
    """
    samples = [
        Sample(1, ["main", "A"]),
        Sample(2, ["main", "A"]),
        Sample(3, ["main", "A"]),
    ]

    expected_events = [
        Event("start", 1, "main"),
        Event("start", 1, "A"),
    ]

    base_events = convert_base(samples)
    hyst_events = convert_with_hysteresis(samples, N)

    assert base_events == expected_events
    assert hyst_events == expected_events