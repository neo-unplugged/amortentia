from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import University, Department, AcademicYear, Course, Division, Chapter, Topic, SubTopic, Element

# Create your views here.

def academic_year_list(request):
    dept = Department.objects.all()[0]
    academic_years = dept.academic_years.all()
    context = {
        "dept": dept,
        "academic_years": academic_years
    }
    return render(request, "pages/academic_year_list.html", context=context)

def course_list(request, academic_year):
    # Retrieve the AcademicYear object based on the year field
    academic_year_obj = get_object_or_404(AcademicYear, year=academic_year)
    # Get all courses related to the AcademicYear
    courses = academic_year_obj.courses.all()
    context = {
        "academic_year": academic_year_obj,
        "courses": courses
    }
    return render(request, "pages/course_list.html", context=context)


def chapter_list(request, academic_year, course_slug):
    # Get the course for the specified academic year and slug
    course = get_object_or_404(Course, slug=course_slug, academic_year__year=academic_year)
    
    # Prefetch related data for divisions, chapters, topics, and sub-topics
    divisions_and_childs = course.divisions.prefetch_related(
        'chapters__topics__sub_topics'
    )
    
    # Pass the course and related data to the context
    context = {
        "academic_year": academic_year,
        "course": course,
        "divisions_and_childs": divisions_and_childs,
    }
    
    return render(request, "pages/chapter_list.html", context)



def topic_detail(request, **kwargs):
    # Extract parameters from the URL
    academic_year = kwargs.get('academic_year', None)
    course_slug = kwargs.get('course_slug', None)
    topic_slug = kwargs.get('topic_slug', None)

    # Fetch the Topic object with related Chapter
    topic = get_object_or_404(Topic.objects.select_related('chapter'), slug=topic_slug)

    # Build breadcrumb structure as a list
    breadcrumbs = [
        {'title': 'Index', 'url': reverse('chapters', kwargs={'academic_year': academic_year, 'course_slug': course_slug})},
        {'title': topic.chapter.name, 'url': None},  # Chapter
    ]

    # Example equations to pass to the template
    equations = [
        r"E = mc^2",
        r"F = ma",
        r"a = \frac{\Delta v}{\Delta t}",
    ]

    # Prepare context
    context = {
        'chapter': topic.chapter,  # Chapter object
        'topic': topic,  # Topic object
        'breadcrumbs': breadcrumbs,  # Breadcrumb navigation
        'equations': equations,  # Equations to display
    }

    # Render the template
    return render(request, "pages/topic_detail.html", context)
