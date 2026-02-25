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

@pytest.mark.parametrize('input_value, expected_result',[
    ('Alice Brown;',1),
    ('Alice Brown;Bob Badonde;',2),
    ('',None)
])
def test_calculate_crew_size(input_value,expected_result):
    """
    Test that calculate_crew_size returns expected values
    """
    actual_result = calculate_crew_size(input_value)
    assert actual_result == expected_result

