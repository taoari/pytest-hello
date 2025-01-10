import pytest
import parametrize_from_file

# Example test case using parametrize_from_file
@parametrize_from_file
def test_double(input, expected, request):
    output = input * 2
    info = {'input': input, 'expected': expected, 'output': output}
    request.node.user_properties.extend(info.items())
    assert output == expected

