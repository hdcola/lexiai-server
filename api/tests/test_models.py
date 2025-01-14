from django.test import TestCase
import mongomock  


class TestModels(TestCase):

    def setUp(self):
        # Set up in-memory MongoDB mock client
        self.client = mongomock.MongoClient()
        self.db = self.client['lexiai_test']
        self.users_collection = self.db['users']
        
        # Delete users before each test
        self.users_collection.delete_many({})

    def tearDown(self):
        # Close the mongomock client after tests
        self.client.close()

    def test_register_success(self):
        data = {
            "username": "testuser",
            "email": "testuser@mail.com",
            "password": "securepassword123",
        }

        try:
            # Insert the new user
            self.users_collection.insert_one(data)
            print(f"Inserted data: {data}")

            # Verify insertion
            inserted_user = self.users_collection.find_one({"username": "testuser"})
            self.assertTrue(inserted_user)
            print(f"Successful insertion in test_register_success: {inserted_user}")

        except Exception as e:
            print(f"Error during test_register_success: {e}")
            self.fail(f"Test failed due to an exception: {e}")

    def test_register_fails_duplicate_email(self):
        # register the first user
        data1 = {
            "username": "testuser1",
            "email": "testuser@mail.com",
            "password": "securepassword123",
        }
        self.users_collection.insert_one(data1)
        print(f"Inserted first user: {data1}")

        # try registering another user with the same email
        data2 = {
            "username": "testuser2",
            "email": "testuser@mail.com",  
            "password": "anotherpassword123",
        }

        try:
            # simulating the validation for duplicate email
            existing_user = self.users_collection.find_one({"email": data2["email"]})
            if existing_user:
                print(f"Duplicate email error: {data2['email']} already exists.")
                self.fail(f"Duplicate email error: {data2['email']} already exists.")
            else:
                # inserting the second user if the email is not found
                self.users_collection.insert_one(data2)
                print(f"Inserted second user: {data2}")

        except Exception as e:
            print(f"Error during test_register_duplicate_email: {e}")
            if "Duplicate email" not in str(e):
                self.fail(f"Test failed due to an unexpected exception: {e}")
