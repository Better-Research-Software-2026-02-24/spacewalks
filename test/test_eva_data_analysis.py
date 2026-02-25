import pytest
from eva_data_analysis import text_to_duration, calculate_crew_size

def test_text_to_duration_integer():
    """
    Test that text_to_duration returns expected values 
    for typical integer-hour durations
    """
    assert text_to_duration('10:00') == 10

def test_text_to_duration_float():
    """
    Test that text_to_duration returns expected values 
    for durations with non-zero minutes components
    """
    assert text_to_duration('10:20') == pytest.approx(10.333333)

def test_calculate_crew_size():
    """
    Test that calculate_crew_size returns expected values
    """
    actual_result = calculate_crew_size('Alice Brown;')
    expected_result = 1
    assert actual_result == expected_result

    actual_result = calculate_crew_size('Alice Brown;Bob Badonde;')
    expected_result = 2
    assert actual_result == expected_result

def test_calculate_crew_size_edge_cases():
    """
    Test that calculate_crew_size returns expected values 
    for edge cases i.e. empty string
    """
    actual_result = calculate_crew_size('')
    expected_result = None
    assert actual_result == expected_result

