from content.models import Language, Word
from django.contrib.auth import get_user_model
from django.test import TestCase
from game.models import Vocabulary


class VocabularyTests(TestCase):

  def setUp(self):
    self.user = get_user_model().objects.create_superuser(
        name='testuser',
        password='testpassword',
    )
    self.language = Language.objects.create_language(
        name='English',
        author=self.user,
        official=True,
    )
    self.language2 = Language.objects.create_language(
        name='Spanish',
        author=self.user,
        official=True,
    )
    self.words = [
        Word.objects.create_word(
            language=self.language,
            name='testword1',
            author=self.user,
            description='testdefinition1',
            official=True),
        Word.objects.create_word(
            language=self.language,
            name='testword2',
            author=self.user,
            description='testdefinition2',
            official=True),
        Word.objects.create_word(
            language=self.language,
            name='testword3',
            author=self.user,
            description='testdefinition3',
            official=True),
    ]
    self.words2 = [
        Word.objects.create_word(
            language=self.language2,
            name='testword4',
            author=self.user,
            description='testdefinition4',
            official=True),
        Word.objects.create_word(
            language=self.language2,
            name='testword5',
            author=self.user,
            description='testdefinition5',
            official=True),
        Word.objects.create_word(
            language=self.language2,
            name='testword6',
            author=self.user,
            description='testdefinition6',
            official=True),
    ]

  def test_create_vocabulary_successful(self):
    """Test vocabulary creation successful"""
    vocab = Vocabulary.objects.create_vocabulary_with_words(
        author=self.user,
        official=True,
        domestic_language=self.language,
        foreign_language=self.language2,
        domestic_words=self.words,
        foreign_words=self.words2,
    )
    self.assertEqual(vocab.author, self.user)
    self.assertEqual(vocab.official, True)
    self.assertEqual(vocab.domestic_language, self.language)
    self.assertEqual(vocab.foreign_language, self.language2)
    self.assertEqual(vocab.domestic_words.count(), 3)
    self.assertEqual(vocab.foreign_words.count(), 3)

  def test_create_vocabulary_without_author(self):
    """Test vocabulary creation without author"""
    with self.assertRaises(ValueError):
      Vocabulary.objects.create_vocabulary_with_words(
          official=True,
          domestic_language=self.language,
          foreign_language=self.language2,
          domestic_words=self.words,
          foreign_words=self.words2,
      )

  def test_create_vocabulary_without_official(self):
    """Test vocabulary creation without official"""
    with self.assertRaises(ValueError):
      Vocabulary.objects.create_vocabulary_with_words(
          author=self.user,
          domestic_language=self.language,
          foreign_language=self.language2,
          domestic_words=self.words,
          foreign_words=self.words2,
      )

  def test_create_vocabulary_without_domestic_language(self):
    """Test vocabulary creation without domestic language"""
    with self.assertRaises(ValueError):
      Vocabulary.objects.create_vocabulary_with_words(
          author=self.user,
          official=True,
          foreign_language=self.language2,
          domestic_words=self.words,
          foreign_words=self.words2,
      )

  def test_create_vocabulary_without_foreign_language(self):
    """Test vocabulary creation without foreign language"""
    with self.assertRaises(ValueError):
      Vocabulary.objects.create_vocabulary_with_words(
          author=self.user,
          official=True,
          domestic_language=self.language,
          domestic_words=self.words,
          foreign_words=self.words2,
      )

  def test_create_vocabulary_without_domestic_words(self):
    """Test vocabulary creation without domestic words"""
    with self.assertRaises(ValueError):
      Vocabulary.objects.create_vocabulary_with_words(
          author=self.user,
          official=True,
          domestic_language=self.language,
          foreign_language=self.language2,
          foreign_words=self.words2,
      )

  def test_create_vocabulary_without_foreign_words(self):
    """Test vocabulary creation without foreign words"""
    with self.assertRaises(ValueError):
      Vocabulary.objects.create_vocabulary_with_words(
          author=self.user,
          official=True,
          domestic_language=self.language,
          foreign_language=self.language2,
          domestic_words=self.words,
      )
