from content.models import Language, Word, WordContext
from django.contrib.auth import get_user_model
from django.test import TestCase


class LanguageTests(TestCase):

  def setUp(self):
    self.user = get_user_model().objects.create_superuser(
        name='testsuperuser',
        password='testsuperuser',
    )

  def test_create_language_successful(self):
    """Test language creation successful"""
    language = Language.objects.create_language(
        name='English',
        author=self.user,
        official=True,
    )
    self.assertEqual(language.name, 'English')
    self.assertEqual(language.author, self.user)
    self.assertEqual(language.official, True)

  def test_create_language_with_no_name(self):
    """Test language creation with no name"""
    with self.assertRaises(ValueError):
      Language.objects.create_language(
          author=self.user,
          official=True,
      )

  def test_create_language_with_no_author(self):
    """Test language creation with no author"""
    with self.assertRaises(ValueError):
      Language.objects.create_language(
          name='English',
          official=True,
      )

  def test_create_language_with_no_official(self):
    """Test language creation with no official"""
    with self.assertRaises(ValueError):
      Language.objects.create_language(
          name='English',
          author=self.user,
      )


class WordTests(TestCase):

  def setUp(self):
    self.user = get_user_model().objects.create_superuser(
        name='testsuperuser',
        password='testsuperuser',
    )
    self.language = Language.objects.create_language(
        name='English',
        author=self.user,
        official=True,
    )

  def test_create_word_successful(self):
    """Test word creation successful"""
    word = Word.objects.create_word(
        language=self.language,
        description='test description',
        name='test',
        author=self.user,
        official=True,
    )
    self.assertEqual(word.language, self.language)
    self.assertEqual(word.description, 'test description')
    self.assertEqual(word.name, 'test')
    self.assertEqual(word.author, self.user)
    self.assertEqual(word.official, True)

  def test_create_word_with_no_language(self):
    """Test word creation with no language"""
    with self.assertRaises(ValueError):
      Word.objects.create_word(
          description='test description',
          name='test',
          author=self.user,
          official=True,
      )

  def test_create_word_with_no_description(self):
    """Test word creation with no description"""
    with self.assertRaises(ValueError):
      Word.objects.create_word(
          language=self.language,
          name='test',
          author=self.user,
          official=True,
      )

  def test_create_word_with_no_name(self):
    """Test word creation with no name"""
    with self.assertRaises(ValueError):
      Word.objects.create_word(
          language=self.language,
          description='test description',
          author=self.user,
          official=True,
      )

  def test_create_word_with_no_author(self):
    """Test word creation with no author"""
    with self.assertRaises(ValueError):
      Word.objects.create_word(
          language=self.language,
          description='test description',
          name='test',
          official=True,
      )

  def test_create_word_with_no_official(self):
    """Test word creation with no official"""
    with self.assertRaises(ValueError):
      Word.objects.create_word(
          language=self.language,
          description='test description',
          name='test',
          author=self.user,
      )


class WordContextTests(TestCase):
  def setUp(self):
    self.user = get_user_model().objects.create_superuser(
        name='testsuperuser',
        password='testsuperuser',
    )
    self.language = Language.objects.create_language(
        name='English',
        author=self.user,
        official=True,
    )

  def test_create_context_successful(self):
    """test that context gets created successful"""
    word_context = WordContext.objects.create_word_context(
        name='test context',
        author=self.user,
    )

    self.assertEqual(word_context.name, 'test context')
    self.assertEqual(word_context.author, self.user)

  def test_create_context_noname(self):
    """test that context gets not created with no name"""
    with self.assertRaises(ValueError):
      WordContext.objects.create_word_context(
          author=self.user,
      )

  def test_create_context_noauthor(self):
    """test that context gets not created with no author"""
    with self.assertRaises(ValueError):
      WordContext.objects.create_word_context(
          name='test context',
      )

  def test_create_context_shortname(self):
    """test that context gets not created with short name"""
    with self.assertRaises(ValueError):
      WordContext.objects.create_word_context(
          name='t',
          author=self.user,
      )

  def test_adding_context_to_word(self):
    """test that context gets added to word"""
    word = Word.objects.create_word(
        language=self.language,
        description='test description',
        name='test',
        author=self.user,
        official=True,
    )
    word_context = WordContext.objects.create_word_context(
        name='test context',
        author=self.user,
    )
    word.set_context(word_context)
    self.assertEqual(word.context, word_context)
