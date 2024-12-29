import pytest
from unittest.mock import patch, MagicMock
from program import Home

# Mock data for testing
mock_user_data = {
    "id": 1,
    "email": "test@example.com",
    "name": "Test User",
    "fav_music": 1,
    "gender": "Male",
    "avatar": "path/to/avatar.png"
}

@pytest.mark.describe("Tests for loadInfo method in Home class")
class TestLoadInfo:

    @pytest.mark.happy_path
    def test_load_info_happy_path(self, qtbot):
        """Test loadInfo with valid user data."""
        with patch('program.get_user_by_id', return_value=mock_user_data):
            home = Home(user_id=1)
            qtbot.addWidget(home)
            home.loadInfo(user_id=1)
            
            assert home.txt_email.text() == "test@example.com"
            assert home.txt_username.text() == "Test User"
            assert home.cb_fav_music.currentIndex() == 1
            assert home.cb_gender.currentIndex() == 0  # Male

    @pytest.mark.edge_case
    def test_load_info_no_fav_music(self, qtbot):
        """Test loadInfo when user has no favorite music set."""
        user_data_no_fav_music = mock_user_data.copy()
        user_data_no_fav_music["fav_music"] = None
        
        with patch('program.get_user_by_id', return_value=user_data_no_fav_music):
            home = Home(user_id=1)
            qtbot.addWidget(home)
            home.loadInfo(user_id=1)
            
            assert home.cb_fav_music.currentIndex() == -1  # Assuming -1 for no selection

    @pytest.mark.edge_case
    def test_load_info_unknown_gender(self, qtbot):
        """Test loadInfo with an unknown gender."""
        user_data_unknown_gender = mock_user_data.copy()
        user_data_unknown_gender["gender"] = "Unknown"
        
        with patch('program.get_user_by_id', return_value=user_data_unknown_gender):
            home = Home(user_id=1)
            qtbot.addWidget(home)
            home.loadInfo(user_id=1)
            
            assert home.cb_gender.currentIndex() == 2  # Assuming 2 for 'Other'

    @pytest.mark.edge_case
    def test_load_info_empty_user_data(self, qtbot):
        """Test loadInfo with empty user data."""
        empty_user_data = {
            "id": 1,
            "email": "",
            "name": "",
            "fav_music": None,
            "gender": "",
            "avatar": ""
        }
        
        with patch('program.get_user_by_id', return_value=empty_user_data):
            home = Home(user_id=1)
            qtbot.addWidget(home)
            home.loadInfo(user_id=1)
            
            assert home.txt_email.text() == ""
            assert home.txt_username.text() == ""
            assert home.cb_fav_music.currentIndex() == -1
            assert home.cb_gender.currentIndex() == 2  # Assuming 2 for 'Other'

# Note: The `qtbot` fixture is provided by pytest-qt to help with testing PyQt applications.