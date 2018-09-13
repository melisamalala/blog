import unittest
from app.models import Blogpost,User
from flask_login import current_user
from app import db

class TestBlogpost(unittest.TestCase):

    def setUp(self):
        self.user_Melissa = User(username = 'Melissa',
                                 password = 'potato',
                                 email = 'melissa@ms.com')
        self.new_blogpost = Blogpost(id=12345,
                                     title='Blogpost itself',
                                     content="this is a nice blog post",
                                     category_id='funny',
                                     comments="what a nice comment",
                                     user_id = self.user_Melissa)

    def tearDown(self):
        Blogpost.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blogpost,Blogpost))


    def test_check_instance_variables(self):
        self.assertEquals(self.new_blogpost.id,12345)
        self.assertEquals(self.new_blogpost.title,'Blogpost itself')
        self.assertEquals(self.new_blogpost.content,"this is a nice blog post")
        self.assertEquals(self.new_blogpost.category_id,'funny')
        self.assertEquals(self.new_blogpost.comments, 'what a nice comment')
        self.assertEquals(self.new_blogpost.user,self.user_Melissa)


    def test_save_blogpost(self):
        self.new_blogpost.save_blogpost()
        self.assertTrue(len(Blogpost.query.all())>0)


    def test_get_blogpost_by_id(self):

        self.new_blogpost.save_blogpost()
        got_blogposts = Blogpost.get_blogposts(12345)
        self.assertTrue(len(got_blogposts) == 1)