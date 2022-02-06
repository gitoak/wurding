from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):

  def test_create_user_with_name_successful(self):
    """Test creating a new user with a name is successful"""
    name = 'testuser'
    password = 'Testpass@123'
    user = get_user_model().objects.create_user(
      name=name,
      password=password
    )

    self.assertEqual(user.name, name)
    self.assertTrue(user.check_password(password))
    self.assertFalse(user.is_staff)
    self.assertFalse(user.is_superuser)

  def test_crete_staff_user_successful(self):
    """Test creating a new staff user"""
    user = get_user_model().objects.create_staff_user(
      name='teststaffuser',
      password='Testpass@123'
    )

    self.assertTrue(user.is_staff)
    self.assertFalse(user.is_superuser)

  def test_create_superuser_successful(self):
    """Test creating a new superuser"""
    user = get_user_model().objects.create_superuser(
      name='testsuperuser',
      password='Testpass@123'
    )

    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)

  def test_create_user_with_no_name(self):
    """Test creating a new user with no name"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(
        name=None,
        password='Testpass@123'
      )

  def test_create_user_with_no_password(self):
    """Test creating a new user with no password"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(
        name='testname',
        password=None
      )

  def test_crete_user_with_short_password(self):
    """Test creating a new user with a short password"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(
        name='testname',
        password='Test@1'
      )

  def test_create_user_with_short_name(self):
    """Test creating a new user with a short name"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(
        name='T',
        password='Testpass@123'
      )
