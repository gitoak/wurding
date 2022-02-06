from core.models import (BaseEntity, BaseEntityManager, User, asure_boolean,
                         asure_string, asure_user)
from django.db import models

###############################################################################
#                               validators                                    #
###############################################################################


def asure_language(language):
  """check if language is submitted"""
  if not language:
    raise ValueError('language is not submitted')
  if not isinstance(language, Language):
    raise ValueError('language is not a Language')


def asure_word(word, language=None):
  """check if word is submitted"""
  if not word:
    raise ValueError('word is not submitted')
  if not isinstance(word, Word):
    raise ValueError('word is not a Word')
  if language is not None:
    if not isinstance(language, Language):
      raise ValueError('language is not a Language')
    if not word.language == language:
      raise ValueError('word is not in the given language')


def asure_languages(languages):
  """check if languages is submitted"""
  if not languages:
    raise ValueError('languages is not submitted')
  if not isinstance(languages, list):
    raise ValueError('languages is not a list')
  if not len(languages) == 2:
    raise ValueError('languages is too short')
  for language in languages:
    if not isinstance(language, Language):
      raise ValueError('language is not a Language')
  if languages[0] == languages[1]:
    raise ValueError('languages are the same')


def asure_words(words, language=None):
  """check if words is submitted"""
  if not words:
    raise ValueError('words is not submitted')
  if not isinstance(words, list):
    raise ValueError('words is not a list')
  if not len(words) > 0:
    raise ValueError('words must be at least 1')
  for word in words:
    if not isinstance(word, Word):
      raise ValueError('word is not a Word')
    if language is not None:
      if not isinstance(language, Language):
        raise ValueError('language is not a Language')
    if not word.language == language:
      raise ValueError('word is not in the given language')

###############################################################################
#                           Managers                                          #
###############################################################################


class LanguageManager(BaseEntityManager):
  """Language manager"""

  def create_language(self, name=None, author=None, official=None, **kwargs):
    """Creates and saves a new language"""

    asure_string(name, 1)
    asure_user(author, "user")
    asure_boolean(official)

    language = self.model(name=name, author=author, official=official, **kwargs)
    language.save(using=self._db)

    return language


class WordManager(BaseEntityManager):
  """Word manager"""

  def create_word(self, name=None, language=None, description=None, author=None, official=None, **kwargs):
    """Creates and saves a new word"""

    asure_string(name, 1)
    asure_language(language)
    asure_string(description)
    asure_user(author, "user")
    asure_boolean(official)

    word = self.model(name=name, language=language, description=description, author=author, official=official, **kwargs)
    word.save(using=self._db)

    return word

  def create_word_with_synonyms(self, name=None, language=None, description=None, synonyms=None, author=None,
                                official=None, category=None, **kwargs):
    """Creates and saves a new word with synonyms"""

    asure_string(name, 1)
    asure_language(language)
    asure_string(description)
    for synonym in synonyms:
      asure_word(synonym, language)
    asure_user(author, "user")
    asure_boolean(official)
    asure_string(category)

    word = self.create_word(name=name, language=language, description=description,
                            author=author, official=official, **kwargs)
    for synonym in synonyms:
      word.synonyms.add(synonym)
    word.save(using=self._db)

    return word


class WordContextManager(BaseEntityManager):
  """WordContext manager"""

  def create_word_context(self, name=None, author=None, **kwargs):
    """Creates and saves a new word context"""

    asure_string(name, 2)
    asure_user(author, "user")

    word_context = self.model(name=name, author=author, **kwargs)
    word_context.save(using=self._db)

    return word_context


###############################################################################
#                           Models                                            #
###############################################################################

class Language(BaseEntity):
  """Language model"""
  name = models.CharField(max_length=255, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='composed_languages')
  subscribers = models.ManyToManyField(User, related_name='subscribed_languages')
  official = models.BooleanField(default=False)

  objects = LanguageManager()

  def add_subscriber(self, user):
    """Add a subscriber to the language"""
    if not isinstance(user, User):
      raise ValueError('The given user must be a user object')
    self.subscribers.add(user)

  def __eq__(self, other):
    return self.name == other.name and self.id == other.id and self.active == other.active

  def __str__(self):
    return f"language object {self.name} active: {self.active}"


class WordContext(BaseEntity):
  """WordContext model"""
  name = models.CharField(max_length=255, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='composed_word_contexts')
  official = models.BooleanField(default=False)

  objects = WordContextManager()

  def __eq__(self, other):
    return self.name == other.name and self.id == other.id and self.active == other.active

  def __str__(self):
    return f"word context object {self.name} active: {self.active}"


class Word(BaseEntity):
  """Word model"""
  name = models.CharField(max_length=255, unique=True)
  language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='words')
  synonyms = models.ManyToManyField('self', blank=True)
  description = models.TextField(blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='composed_words')
  official = models.BooleanField(default=False)
  type = models.CharField(max_length=511, blank=True)   # adj, noun, verb, ...
  gender = models.CharField(max_length=1, blank=True)   # only aplicable if noun
  practices = models.IntegerField(default=0)
  succesful_practices = models.IntegerField(default=0)
  context = models.ForeignKey(WordContext, on_delete=models.CASCADE, related_name='words', blank=True, null=True)

  objects = WordManager()

  def add_synonym(self, word):
    """Adds a synonym to this word"""
    if not isinstance(word, Word):
      raise ValueError('The given word must be a Word object')
    self.synonyms.add(word)
    self.save()

    return self

  def remove_synonym(self, word):
    """Removes a synonym from this word"""
    if not isinstance(word, Word):
      raise ValueError('The given word must be a Word object')
    self.synonyms.remove(word)
    self.save()

    return self

  def add_practice(self, successful):
    """Adds a practice to this word"""
    self.practices += 1
    if successful:
      self.successful_practices += 1
    self.save()

    return self

  def set_context(self, word_context):
    """sets a word context"""
    if not isinstance(word_context, WordContext):
      raise ValueError('The given word context must be a WordContext object')
    self.context = word_context
    self.save()

    return self

  def ration(self):
    """Returns the ration of successful practices to all practices"""
    return self.successful_practices / self.practices * 100

  def __eq__(self, other):
    return (self.name == other.name and self.id == other.id and self.active == other.active and
            self.language == other.language and self.description == other.description and
            self.synonyms == other.synonyms)

  def __str__(self):
    return f"word object {self.name} active: {self.active} language: {self.language}"
