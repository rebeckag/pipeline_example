import pytest
from example.example import HelloSayer

__author__ = 'regu0004'

@pytest.yield_fixture(params=[
    "en",
    "sv",
    "foo"
])
def greeting(request):
    name = "Foo Bar"
    greeter = HelloSayer(request.param)
    yield greeter.say_hello_to(name)
    print(greeter.say_goodbye_to(name).encode("utf-8"))

def test_hello_sayer(greeting):
    print(greeting.encode("utf-8"))