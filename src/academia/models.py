from django.db import models
from django.utils.text import slugify
# Create your models here.


# University model
class University(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Faculty model
class Faculty(models.Model):
    name = models.CharField(max_length=255)
    university = models.ForeignKey(University, related_name='faculties', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Department model
class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, related_name='departments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Academic Year model
class AcademicYear(models.Model):
    year = models.CharField(max_length=50)  # e.g., '1st', '2nd', '3rd', '4th', 'MS'
    department = models.ForeignKey(Department, related_name='academic_years', on_delete=models.CASCADE)

    def __str__(self):
        return self.year

# Course model
class Course(models.Model):
    name = models.CharField(max_length=255)
    academic_year = models.ForeignKey(AcademicYear, related_name='courses', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a slug if it's not already set
            self.slug = slugify(self.name)
        
    def __str__(self):
        return self.name

# Division model (optional, for subdivided courses)
class Division(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='divisions', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a slug if it's not already set
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Chapter model
class Chapter(models.Model):
    name = models.CharField(max_length=255)
    division = models.ForeignKey(Division, related_name='chapters', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a slug if it's not already set
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Topic model
class Topic(models.Model):
    name = models.CharField(max_length=255)
    chapter = models.ForeignKey(Chapter, related_name='topics', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a slug if it's not already set
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# SubTopic model
class SubTopic(models.Model):
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, related_name='sub_topics', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a slug if it's not already set
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Element model (for storing various content types)
class Element(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    EQUATION = 'equation'
    LIST = 'list'
    LINK = 'link'
    TABLE = 'table'
    GRAPH = 'graph'
    SUMMARY_BOX = 'summary_box'
    NOTE = 'note'

    ELEMENT_TYPES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (EQUATION, 'Equation'),
        (LIST, 'List'),
        (LINK, 'Link'),
        (TABLE, 'Table'),
        (GRAPH, 'Graph'),
        (SUMMARY_BOX, 'Summary Box'),
        (NOTE, 'Note'),
    ]

    type = models.CharField(max_length=50, choices=ELEMENT_TYPES)
    content = models.TextField()  # content could be text, image URL, LaTeX formula, etc.
    order = models.PositiveIntegerField()  # to keep track of the order of elements
    sub_topic = models.ForeignKey(SubTopic, related_name='elements', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.get_type_display()} - {self.id}'


## We need models for each element type
## Thank you
# The genetic text type element (i.e Plain text, Note, Summary)
# Media elements (i.e Image, Figures)
# Objects (i.e Tables, Equations, Lists)

class ContentSection(models.Model):
    title = models.CharField(max_length=255, default='content section')
    sub_topic =models.ForeignKey(SubTopic, related_name='content_section', on_delete=models.CASCADE)
    
