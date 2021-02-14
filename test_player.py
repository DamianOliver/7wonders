# Copyright 2020 Damian Piech

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from game import *

BRICKS = Card("Brick Factory", C.RAW_R, provides_resources = [(R.BRICK,)])
TOWEL_FACTORY = Card("Towel Factory", C.MFG_R, provides_resources = [(R.SILK,),(R.SILK,)])
STONES_N_BRICKS = Card("Stones + Bricks 'r' Us", C.RAW_R, provides_resources = [(R.STONE, R.BRICK)])
COAL_MINE = Card("Coal Mine", C.RAW_R, provides_resources = [(R.COAL,)])
TEMPLE = Card("Temple", C.CIVIC, points = 4, cost = [R.COAL])

@pytest.fixture
def player():
    return Player(1)

def test_Player__available_resource_tuples__handles_simple_resource(player):
    # when
    resource_provides = player.available_resources_tuples([BRICKS])

    # then
    assert len(resource_provides) == 1
    assert resource_provides.count((R.BRICK,)) == 1

def test_Player__available_resource_tuples__handles_card_with_multiple_resource(player):
    # when
    resource_provides = player.available_resources_tuples([TOWEL_FACTORY])

    # then
    assert len(resource_provides) == 2
    assert resource_provides.count((R.SILK,)) == 2

def test_Player__available_resource_tuples__handles_card_with_resource_choice(player):
    # when
    resource_provides = player.available_resources_tuples([STONES_N_BRICKS])

    # then
    assert len(resource_provides) == 1
    assert resource_provides.count((R.STONE, R.BRICK)) == 1

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
    assert resource_provides.count((R.STONE, R.BRICK)) == 1
    assert resource_provides.count((R.SILK,)) == 2
    assert resource_provides.count((R.BRICK,)) == 1

def test_Player__has_resources__with_single_resource(player):
    # given
    resource_provides = [(R.COAL,)]

    # expect
    assert player.has_resources([R.COAL], resource_provides)

def test_Player__has_resources__with_multiple_resources(player):
    # given
    resource_provides = [(R.COAL,), (R.SILK,)]

    # expect
    assert player.has_resources([R.COAL, R.SILK], resource_provides)

def test_Player__has_resources__with_resource_tuple_False(player):
    # given
    resource_provides = [(R.COAL, R.SILK)]

    # expect
    assert False == player.has_resources([R.COAL, R.SILK], resource_provides)

def test_Player__has_resources__with_resource_multiple_tuples(player):
    # given
    resource_provides = [(R.COAL, R.SILK), (R.COAL, R.SILK)]

    # expect
    assert player.has_resources([R.COAL, R.SILK], resource_provides)

def test_Player__has_resources__with_multiple_costs(player):
    # given
    resource_provides = [(R.COAL,), (R.COAL,)]

    # expect
    assert player.has_resources([R.COAL, R.COAL], resource_provides)

def test_Player__has_resources__with_multiple_costs(player):
    # given
    resource_provides = [(R.COAL,), (R.COAL,)]

    # expect
    assert player.has_resources([R.COAL, R.COAL], resource_provides)

def test_Player__has_resources__combo1(player):
    # given
    resource_provides = [(R.COAL,), (R.COAL,), (R.SILK, R.BRICK), (R.STONE,)]

    # expect
    assert player.has_resources([R.COAL, R.COAL, R.SILK, R.STONE], resource_provides)

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
