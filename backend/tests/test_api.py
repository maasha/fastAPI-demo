import pytest
from app.db_models import UserDB


class TestCreateUser:
    """Tests for POST /users endpoint"""
    
    def test_create_user_success(self, client, mock_db, sample_user_data):
        """Test creating a user successfully"""
        # Mock the database refresh to set the ID
        def mock_refresh(obj):
            obj.id = 1
        mock_db.refresh.side_effect = mock_refresh
        
        response = client.post("/users", json=sample_user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_user_data["name"]
        assert data["age"] == sample_user_data["age"]
        assert data["address"] == sample_user_data["address"]
        assert data["id"] == 1
        
        # Verify database methods were called
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_create_user_invalid_age(self, client):
        """Test creating user with invalid age"""
        response = client.post("/users", json={
            "name": "Test User",
            "age": -5,  # Invalid age
            "address": "123 Test St"
        })
        assert response.status_code == 422  # Validation error


class TestGetAllUsers:
    """Tests for GET /users endpoint"""
    
    def test_get_all_users_success(self, client, mock_db):
        """Test getting all users"""
        # Mock the query to return a list of users
        mock_users = [
            UserDB(id=1, name="User 1", age=25, address="Address 1"),
            UserDB(id=2, name="User 2", age=30, address="Address 2"),
        ]
        mock_db.query.return_value.all.return_value = mock_users
        
        response = client.get("/users")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "User 1"
        assert data[1]["name"] == "User 2"
    
    def test_get_all_users_empty(self, client, mock_db):
        """Test getting users when database is empty"""
        mock_db.query.return_value.all.return_value = []
        
        response = client.get("/users")
        
        assert response.status_code == 200
        assert response.json() == []


class TestGetUser:
    """Tests for GET /users/{user_id} endpoint"""
    
    def test_get_user_success(self, client, mock_db, sample_user_db):
        """Test getting a single user by ID"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user_db
        
        response = client.get("/users/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["age"] == 30
    
    def test_get_user_not_found(self, client, mock_db):
        """Test getting a user that doesn't exist"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        response = client.get("/users/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateUser:
    """Tests for PUT /users/{user_id} endpoint"""
    
    def test_update_user_success(self, client, mock_db, sample_user_db):
        """Test updating a user successfully"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user_db
        
        update_data = {"age": 35}
        response = client.put("/users/1", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["age"] == 35
        
        # Verify database methods were called
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    def test_update_user_partial(self, client, mock_db, sample_user_db):
        """Test partial update of user"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user_db
        
        update_data = {"name": "Jane Doe"}
        response = client.put("/users/1", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"
    
    def test_update_user_not_found(self, client, mock_db):
        """Test updating a user that doesn't exist"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        response = client.put("/users/999", json={"age": 40})
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_update_user_invalid_data(self, client, mock_db, sample_user_db):
        """Test updating user with invalid data"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user_db
        
        response = client.put("/users/1", json={"age": -10})
        
        assert response.status_code == 422  # Validation error


class TestDeleteUser:
    """Tests for DELETE /users/{user_id} endpoint"""
    
    def test_delete_user_success(self, client, mock_db, sample_user_db):
        """Test deleting a user successfully"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user_db
        
        response = client.delete("/users/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "deleted successfully" in data["message"].lower()
        
        # Verify database methods were called
        mock_db.delete.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_delete_user_not_found(self, client, mock_db):
        """Test deleting a user that doesn't exist"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        response = client.delete("/users/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestHealthEndpoints:
    """Tests for health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "Hello World" in response.json()["message"]
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_about_endpoint(self, client):
        """Test about endpoint"""
        response = client.get("/about")
        
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data

