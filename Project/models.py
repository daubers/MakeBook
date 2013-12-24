from django.db import models

# Create your models here.


class Project(models.Model):
    """
        This model just contains the basic information about a project
    """
    title = models.TextField(max_length=255)
    startDate = models.DateTimeField()
    category = models.TextField(max_length=255)
    complete = models.BooleanField()


class BoM(models.Model):
    """
        This model describes a bill of materials
    """
    name = models.TextField(max_length=255)
    description = models.TextField()


class Part(models.Model):
    """
        This model describes a single part
    """
    name = models.TextField(max_length=255)
    source = models.TextField()
    description = models.TextField()
    cost = models.FloatField()


class BoMToParts(models.Model):
    """
        Attaches parts to a BOM
    """
    part = models.ForeignKey(Part)
    bom = models.ForeignKey(BoM)
    quantity = models.IntegerField()
    ordered = models.BooleanField()
    order_date = models.DateTimeField()
    arrived = models.BooleanField()
    arrival_date = models.DateTimeField()


class BoMtoProject(models.Model):
    """
    Links BoMs to projects
    """
    bom = models.ForeignKey(BoM)
    project = models.ForeignKey(Project)


class BlogPost(models.Model):
    """
        describes a blog post
    """
    title = models.TextField()
    url = models.TextField()
    date_posted = models.DateTimeField()


class ProjectToBlogPost(models.Model):
    """
        Links a project to a blog post
    """
    project = models.ForeignKey(Project)
    post = models.ForeignKey(BlogPost)


class Notes(models.Model):
    """
        Describes a note
    """
    title = models.TextField()
    note = models.TextField()
    date_created = models.DateTimeField()


class NotesToProject(models.Model):
    """
        Attach a note to a project
    """
    note = models.ForeignKey(Notes)
    project = models.ForeignKey(Project)


class Task(models.Model):
    """
        Describes a task
    """
    title = models.TextField(max_length=255)
    description = models.TextField()
    date_added = models.DateTimeField()
    completed = models.BooleanField()


class TaskToProject(models.Model):
    """
        Attaches a task to a project
    """
    task = models.ForeignKey(Task)
    project = models.ForeignKey(Project)


class Image(models.Model):
    """
        Describes an image
    """
    url = models.TextField()
    title = models.TextField(max_length=255)
    description = models.TextField()
    caption = models.TextField()


class ImageToProject(models.Model):
    """
        Attaches an image to a project
    """
    project = models.ForeignKey(Project)
    image = models.ForeignKey(Image)