import pytest
from game import *

BRICKS = Card("Brick Factory", "Raw Resource", provides_resources = [("brick",)])
TOWEL_FACTORY = Card("Towel Factory", "Manufactored Resource", provides_resources = [("silk",),("silk",)])
STONES_N_BRICKS = Card("Stones + Bricks 'r' Us", "Raw Resource", provides_resources = [("stone", "brick")])
COAL_MINE = Card("Coal Mine", "Raw Resource", provides_resources = [("coal",)])
TEMPLE = Card("Temple", "Civic", points = 4, cost = ["coal"])

@pytest.fixture
def player():
    return Player(1)

def test_Player__available_resource_tuples__handles_simple_resource(player):
    # when
    resource_provides = player.available_resources_tuples([BRICKS])

    # then
    assert len(resource_provides) == 1
    assert resource_provides.count(("brick",)) == 1

def test_Player__available_resource_tuples__handles_card_with_multiple_resource(player):
    # when
    resource_provides = player.available_resources_tuples([TOWEL_FACTORY])

    # then
    assert len(resource_provides) == 2
    assert resource_provides.count(("silk",)) == 2

def test_Player__available_resource_tuples__handles_card_with_resource_choice(player):
    # when
    resource_provides = player.available_resources_tuples([STONES_N_BRICKS])

    # then
    assert len(resource_provides) == 1
    assert resource_provides.count(("stone", "brick")) == 1

def test_Player__available_resource_tuples__handles_card_no_resources_provided(player):
    # when
    resource_provides = player.available_resources_tuples([TEMPLE])

    # then
    assert len(resource_provides) == 0

def test_Player__available_resource_tuples__handles_multiple_cards(player):
    # when
    resource_provides = player.available_resources_tuples(
        [TEMPLE, STONES_N_BRICKS, TOWEL_FACTORY, BRICKS])

    # then
    assert len(resource_provides) == 4
    assert resource_provides.count(("stone", "brick")) == 1
    assert resource_provides.count(("silk",)) == 2
    assert resource_provides.count(("brick",)) == 1

def test_Player__has_resources__with_single_resource(player):
    # given
    resource_provides = [("coal",)]

    # expect
    assert player.has_resources(["coal"], resource_provides)

def test_Player__has_resources__with_multiple_resources(player):
    # given
    resource_provides = [("coal",), ("silk",)]

    # expect
    assert player.has_resources(["coal", "silk"], resource_provides)

def test_Player__has_resources__with_resource_tuple_False(player):
    # given
    resource_provides = [("coal", "silk")]

    # expect
    assert False == player.has_resources(["coal", "silk"], resource_provides)

def test_Player__has_resources__with_resource_multiple_tuples(player):
    # given
    resource_provides = [("coal", "silk"), ("coal", "silk")]

    # expect
    assert player.has_resources(["coal", "silk"], resource_provides)

def test_Player__has_resources__with_multiple_costs(player):
    # given
    resource_provides = [("coal",), ("coal",)]

    # expect
    assert player.has_resources(["coal", "coal"], resource_provides)

def test_Player__has_resources__with_multiple_costs(player):
    # given
    resource_provides = [("coal",), ("coal",)]

    # expect
    assert player.has_resources(["coal", "coal"], resource_provides)

def test_Player__has_resources__combo1(player):
    # given
    resource_provides = [("coal",), ("coal",), ("silk", "bricks"), ("stone",)]

    # expect
    assert player.has_resources(["coal", "coal", "silk", "stone"], resource_provides)

def test_Player__play_card(player):
    # when
    player.play_card(TOWEL_FACTORY)

    # then
    assert len(player.cards) == 1
    assert player.cards[0] == TOWEL_FACTORY

def test_Player__play_multiple(player):
    # when
    player.play_card(TOWEL_FACTORY)
    player.play_card(STONES_N_BRICKS)

    # then
    assert len(player.cards) == 2
    assert player.cards.count(TOWEL_FACTORY) == 1
    assert player.cards.count(STONES_N_BRICKS) == 1

def test_Player__play_card_with_cost(player):
    # given
    player.play_card(COAL_MINE)

    # when
    player.play_card(TEMPLE)

    # then
    assert len(player.cards) == 2
    assert player.cards.count(COAL_MINE) == 1
    assert player.cards.count(TEMPLE) == 1
