from content.models import Language, Word, asure_languages, asure_words
from core.models import (BaseEntity, BaseEntityManager, User, asure_boolean,
                         asure_string, asure_user)
from django.db import models

###############################################################################
#                               validators                                    #
###############################################################################


def asure_vocabularies(vocabularies):
  if vocabularies is None:
    raise ValueError('Vocabulary is required')
  if not isinstance(vocabularies, list):
    raise ValueError('Vocabulary must be a list')
  if len(vocabularies) == 0:
    raise ValueError('Vocabulary must not be empty')
  for vocabulary in vocabularies:
    if not isinstance(vocabulary, Vocabulary):
      raise ValueError('Vocabulary must be a list of Vocabulary objects')


def asure_vocabulary(vocabulary):
  if vocabulary is None:
    raise ValueError('Vocabulary is required')
  if not isinstance(vocabulary, Vocabulary):
    raise ValueError('Vocabulary must be a Vocabulary object')


def asure_packages(packages):
  if packages is None:
    raise ValueError('Package is required')
  if not isinstance(packages, list):
    raise ValueError('Package must be a list')
  if len(packages) == 0:
    raise ValueError('Package must not be empty')
  for package in packages:
    if not isinstance(package, Package):
      raise ValueError('Package must be a list of Package objects')


###############################################################################
#                           Managers                                          #
###############################################################################


class VocabularyContextManager(BaseEntityManager):
  """VocabularyContext manager"""

  def create_word_context(self, name=None, author=None, **kwargs):
    """Creates and saves a new vocabulary context"""

    asure_string(name, 2)
    asure_user(author, "user")

    word_context = self.model(name=name, author=author, **kwargs)
    word_context.save(using=self._db)

    return word_context


class VocabularyManager(BaseEntityManager):
  """Vocabulary manager"""

  def create_vocabulary_with_words(self, domestic_language=None, foreign_language=None, domestic_words=None,
                                   foreign_words=None, author=None, official=None, **kwargs):
    """Creates and saves a new vocabulary with words"""
    asure_languages([domestic_language, foreign_language])
    asure_words(domestic_words, domestic_language)
    asure_words(foreign_words, foreign_language)
    asure_user(author, "user")
    asure_boolean(official)

    vocabulary = self.model(domestic_language=domestic_language, foreign_language=foreign_language,
                            author=author, official=official, **kwargs)
    vocabulary.domestic_words.set(domestic_words)
    vocabulary.foreign_words.set(foreign_words)
    vocabulary.save(using=self._db)

    return vocabulary


class PackageManager(BaseEntityManager):
  """Package manager"""

  def create_package_with_vocabularies(self, name=None, author=None, official=None, description=None,
                                       vocabulary=None, **kwargs):
    """Creates and saves a new package with vocabularies"""
    asure_string(name)
    asure_user(author, "user")
    asure_boolean(official)
    asure_string(description)
    asure_vocabularies(vocabulary)

    package = self.model(name=name, author=author, official=official, **kwargs)
    package.save(using=self._db)

    return package


class FolderManager(BaseEntityManager):
  """Folder manager"""

  def create_folder_with_packages(self, name=None, author=None, official=None, description=None,
                                  package=None, **kwargs):
    """Creates and saves a new folder with packages"""
    asure_string(name)
    asure_user(author, "user")
    asure_boolean(official)
    asure_string(description)
    asure_packages(package)

    folder = self.model(name=name, author=author, official=official, **kwargs)
    folder.save(using=self._db)

    return folder


class LearningManager(BaseEntityManager):
  """Learning manager"""

  def create_learning_with_vocabulary(self, user=None,
                                      vocabulary=None, **kwargs):
    """Creates and saves a new learning with a vocabulary"""
    asure_user(user, "user")
    asure_vocabulary(vocabulary)

    learning = self.model(user=user, vocabulary=vocabulary, **kwargs)
    learning.save(using=self._db)

    return learning


###############################################################################
#                           Models                                            #
###############################################################################


class VocabularyContext(BaseEntity):
  """WordContext model"""
  name = models.CharField(max_length=255, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='composed_word_contexts')
  official = models.BooleanField(default=False)

  objects = VocabularyContextManager()

  def __eq__(self, other):
    return self.name == other.name and self.id == other.id and self.active == other.active

  def __str__(self):
    return f"word context object {self.name} active: {self.active}"


class Vocabulary(BaseEntity):
  """Vocabulary is a collection of words."""
  domestic_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="domestic_vokabularies")
  foreign_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="foreign_vokabularies")
  domestic_words = models.ManyToManyField(Word, related_name='domestic_vocabularies')
  foreign_words = models.ManyToManyField(Word, related_name='foreign_vocabularies')
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="composed_vocabularies")
  official = models.BooleanField(default=False)
  context = models.ForeignKey(VocabularyContext, on_delete=models.CASCADE, related_name='vocabularies', blank=True,
                              null=True)

  objects = VocabularyManager()

  def __eq__(self, other):
    return (self.id == other.id and self.active == other.active and self.domestic_language == other.domestic_language
            and self.foreign_language == other.foreign_language and self.domestic_words == other.domestic_words and
            self.foreign_words == other.foreign_words)

  def __str__(self):
    return f"vocabulary object {self.id} active: {self.active}"


class Package(BaseEntity):
  """Package is a collection of vocabularies."""
  name = models.CharField(max_length=255, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="composed_packages")
  official = models.BooleanField(default=False)
  vocabularies = models.ManyToManyField(Vocabulary, related_name='packages')
  describtion = models.TextField(blank=True, null=True)
  subscribers = models.ManyToManyField(User, related_name='subscribed_packages')

  objects = PackageManager()

  def __eq__(self, other):
    return (self.id == other.id and self.active == other.active and self.name == other.name and
            self.author == other.author)

  def __str__(self):
    return f"package object {self.id} active: {self.active}"


class Folder(BaseEntity):
  """Package is a collection of vocabularies."""
  name = models.CharField(max_length=255, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="composed_folders")
  official = models.BooleanField(default=False)
  packages = models.ManyToManyField(Package, related_name='packages')
  describtion = models.TextField(blank=True, null=True)
  subscribers = models.ManyToManyField(User, related_name='subscribed_folders')

  objects = FolderManager()

  def __eq__(self, other):
    return (self.id == other.id and self.active == other.active and self.name == other.name and
            self.author == other.author)

  def __str__(self):
    return f"package object {self.id} active: {self.active}"


class Learning(BaseEntity):
  """Learning model is a record of a user's learning progress."""
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="learnings")
  vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name="learnings")
  score = models.IntegerField(default=1)
  prev_score = models.IntegerField(default=1)

  def __eq__(self, other):
    return self.id == other.id and self.active == other.active and self.user == other.user
