from django.db import models
import bcrypt

# specifying choices
POLITENESS_CHOICES = (
  ("formal", "formal"),
  ("polite", "polite"),
  ("casual", "casual")
)

# Model managers
class UserManager(models.Manager):
  def basic_validator(self, postData):
    errors={}
    if 'username' in postData:
      if len(postData['username']) < 2:
        errors['username'] = "Username must be at least 2 characters"
      if len(User.objects.filter(username=postData['username'])) > 0:
          errors['username'] = "This username is already registered"
    if 'pw' in postData:            
      if len(postData['pw']) < 8:
        errors['pw'] = "Password must be at least 8 characters"
    if 'username2' in postData:
      if len(User.objects.filter(username=postData['username2'])) < 1:
        errors['login'] = "Login failed"
      elif 'username2' in postData:
        this_user = User.objects.filter(username=postData['username2'])
        print(postData['pw2'].encode('utf-8'), this_user[0].password.encode('utf-8'))
        if not bcrypt.checkpw(postData['pw2'].encode('utf-8'), this_user[0].password.encode('utf-8')):
          errors['login'] = "Login failed"
    return(errors)


class KoreanManager(models.Manager):
  def basic_validator(self, postData):
    errors={}
    if len(postData['korean']) < 1:
      errors['korean'] = "Korean phrase must be at least 1 character"
    if len(postData['english']) < 1:
      errors['english'] = "English translation must be at least 1 character"
    return errors

# Create your models here.
class User(models.Model):
  username = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

class English(models.Model):
  english = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Korean(models.Model):
  korean = models.TextField()
  politeness_level = models.CharField(
    max_length = 10,
    choices = POLITENESS_CHOICES,
    default = "formal"
  )
  eng_translation = models.ForeignKey(English, related_name="korean", on_delete=models.CASCADE)
  notes = models.TextField()
  uploaded_by = models.ForeignKey(User, related_name="korean_phrase", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = KoreanManager()

class Category(models.Model):
  phrase_translation = models.ManyToManyField(Korean, related_name="category")
  created_at = models.DateTimeField(auto_now_add=True) 
  updated_at = models.DateTimeField(auto_now=True)
