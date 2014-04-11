#LOL
import unittest
from main import app, User, db
from subprocess import call

class FinalProjectTestCase(unittest.TestCase):
    def setUp(self):
        """
        create test database connection
        """
        import os
        try:
            os.remove('test.db')
        except OSError:
            pass
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()
    
    def test_user_model(self):
        """
        test the user model for the db
        """
        u = User("uname", "pwd")
        db.session.add(u)
        db.session.commit()

        self.assertEqual(User.query.filter_by(username="name").first(), None)
        self.assertTrue(User.query.filter_by(username="uname").first().check_password("pwd"))
        self.assertFalse(User.query.filter_by(username="uname").first().check_password("password"))  

if __name__ == '__main__':
    unittest.main()
