import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from src.controllers.recipecontroller import RecipeController


@pytest.fixture
def sut():
    mocked_items_dao = MagicMock()
    sut = RecipeController(mocked_items_dao)
    return sut


three_recipes = {
    "mid ready recipe": 0.7,
    "least ready recipe": 0.65,
    "most ready recipe": 0.75
}

@pytest.mark.unit
@pytest.mark.parametrize(
    'recipes, take_best, expected_outcome',
    [
        ({}, False, None),
        ({'single recipe': 0.1}, False, 'single recipe'),
        (three_recipes, True, 'most ready recipe'),
        (three_recipes, False, 'mid ready recipe'),
    ])
def test_get_recipe(sut, recipes, take_best,expected_outcome):
    """
    Tests the get_recipe method. This test includes
    4 parametrized test cases:
    1. there are no available recipes, should return None
    2. there is one available recipe, the recipe should be returned
    3. there are three available recipes with readiness values
       0.7, 0.65 and 0.75, and take_best is set to True.
       The recipe with readiness 0.75, named 'most ready recipe', should be the one returned.
    4. there are three available recipes with readiness values
       0.7, 0.65 and 0.75 and take_best is set to False.
       The recipe with readiness 0.7, named 'mid ready recipe', should be the one returned
    """

    user_diet = MagicMock()

    with patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes', return_value = recipes), \
        patch('random.randint', return_value = 1):
        result =  sut.get_recipe(user_diet, take_best)


        assert result == expected_outcome
