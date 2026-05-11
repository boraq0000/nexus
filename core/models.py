from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.validators import EmailValidator, MinLengthValidator, MinValueValidator

# Model storing user account details

def validate_image(file):
    try:
        Image.open(file).verify()
    except Exception:
        raise ValidationError("invalid file; must be an image only")
    

def validate_no_script(value):
    if"<script>"in value.lower():
        raise ValidationError("Javascript cod is not allowed")
    

class Users(models.Model):
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('investor', 'Investor'),
    ]
    email = models.EmailField(unique=True, max_length=255, validators=[EmailValidator()])
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    academic_year = models.IntegerField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    subscription_type = models.CharField(max_length=50, blank=True, null=True)
    linkedin_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

# Model storing project metadata.
class Projects(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Pending Approval', 'Pending Approval'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    PROJECT_STATUS_CHOICES = [
        ('Investment', 'Investment'),
        ('Sale', 'Sale'),
        ('Display', 'Display'),
        ('Draft', 'Draft'),
    ]
    
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, validators=[validate_no_script])
    image = models.ImageField(upload_to="projects/", validators=[validate_image])
    description = models.TextField(blank=True, null=True, validators=[validate_no_script])
    owner = models.ForeignKey('Users', models.DO_NOTHING, related_name='owned_projects')
    professor = models.ForeignKey('Users', models.DO_NOTHING, related_name='assigned_projects', 
                                   limit_choices_to={'role': 'professor'}, null=True)
    status = models.CharField(max_length=50, choices=PROJECT_STATUS_CHOICES, default='Investment')
    approval_status = models.CharField(max_length=50, choices=APPROVAL_STATUS_CHOICES, default='Draft')
    professor_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True, default=0)
    rank_badge = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'projects'

# Model linking users to project memberships.
class ProjectsMember(models.Model):
    MEMBER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    ROLE_IN_PROJECT_CHOICES = [
        ('owner', 'Owner'),
        ('member', 'Member'),
    ]
    
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, models.DO_NOTHING, db_column='project_id', related_name='members')
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id', related_name='project_memberships')
    role_in_project = models.CharField(max_length=100, choices=ROLE_IN_PROJECT_CHOICES, default='member')
    status = models.CharField(max_length=50, choices=MEMBER_STATUS_CHOICES, default='accepted')
    joined_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'projects_member'
        unique_together = (('project', 'user'),)
        # This table uses a composite primary key in the DB.
        # Django does not support composite primary keys natively,
        # so this model must remain unmanaged and should not be registered in admin.

# Model storing project evaluation results.
class Evaluations(models.Model):
    evaluation_id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    student = models.ForeignKey('Users', models.DO_NOTHING)
    professor = models.ForeignKey('Users', models.DO_NOTHING, related_name='evaluations_professor_set')
    score_average = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    evaluation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evaluations'

# Model storing investor contributions.
class Investments(models.Model):
    # إضافة Validator لمنع أي مبلغ أقل من 0.01
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    INVESTMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    investment_id = models.AutoField(primary_key=True)
    investor = models.ForeignKey('Users', models.DO_NOTHING, related_name='investments',
                                 limit_choices_to={'role': 'investor'})
    project = models.ForeignKey('Projects', models.DO_NOTHING, related_name='investments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=INVESTMENT_STATUS_CHOICES, default='pending')
    investment_date = models.DateTimeField(auto_now_add=True)
    roi_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'investments'
        unique_together = (('investor', 'project'),)

# Model storing investor ratings for projects.
class InvestorRatings(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    rating_id = models.AutoField(primary_key=True)
    investor = models.ForeignKey('Users', models.DO_NOTHING, related_name='ratings',
                                 limit_choices_to={'role': 'investor'})
    project = models.ForeignKey('Projects', models.DO_NOTHING, related_name='investor_ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True, null=True)
    rating_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'investor_ratings'
        unique_together = (('investor', 'project'),)