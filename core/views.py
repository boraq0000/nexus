from django.contrib.auth.hashers import make_password, check_password
import json
from pathlib import Path
from datetime import datetime

from django.contrib.auth.hashers import check_password, make_password
from django.db import connection
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Users, Projects, ProjectsMember, Evaluations, Investments, InvestorRatings
from django_ratelimit.decorators import ratelimit
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.

# Serve the main HTML page.
def home_view(request):
    index_path = BASE_DIR / 'core' / 'index.html'
    return FileResponse(open(index_path, 'rb'), content_type='text/html')


# Parse JSON from the request body.
def parse_json_body(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return None


# Return users filtered by role.
def get_users_by_role(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
    role = request.GET.get('role', '').strip()
    if not role:
        return JsonResponse({'success': False, 'error': 'role query parameter is required.'}, status=400)

    role_map = {
        'student': 'Student',
        'professor': 'Professor',
        'investor': 'Investor',
    }
    
    role_normalized = role_map.get(role.lower())
    if not role_normalized:
        return JsonResponse({'success': False, 'error': 'Invalid role.'}, status=400)

    users = Users.objects.filter(role=role_normalized).values('user_id', 'name')
    return JsonResponse({'success': True, 'users': list(users)})


# Convert a project object to JSON-friendly data.
def serialize_project(project, member=None):
    data = {
        'id': project.project_id,
        'title': project.title,
        'description': project.description,
        'owner_id': project.owner.user_id if project.owner else None,
        'owner_name': project.owner.name if project.owner else None,
        'professor_id': project.professor.user_id if project.professor else None,
        'professor_name': project.professor.name if project.professor else None,
        'status': project.status,
        'approval_status': project.approval_status,
        'professor_score': float(project.professor_score) if project.professor_score is not None else None,
        'views': project.views,
        'rank_badge': project.rank_badge,
        'created_date': project.created_date.isoformat() if project.created_date else None,
    }
    if member:
        data['membership_status'] = member.status
        data['membership_role'] = member.role_in_project
    return data


# Handle new user signup requests.
@csrf_exempt
def signup_check(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    name = payload.get('name', '').strip()
    email = payload.get('email', '').strip()
    password = payload.get('password', '')
    role = payload.get('role', 'student').strip()

    if not name or not email or not password:
          return JsonResponse({'success': False, 'error': 'Name, email, and password are required.'}, status=400)

    if len(password) < 8:
        return JsonResponse({'success': False, 'error': 'Password must be at least 8 characters.'}, status=400)

    if not any(c.isdigit() for c in password):
        return JsonResponse({'success': False, 'error': 'Password must contain at least one number.'}, status=400)

    if not any(c.isupper() for c in password):
        return JsonResponse({'success': False, 'error': 'Password must contain at least one uppercase letter.'}, status=400)
      
    allowed_domains = ['gmail.com', 'yahoo.com', 'outlook.com','hotmail.com', 'alexu.edu.eg']
    email_domain = email.split('@')[-1]
    if email_domain not in allowed_domains:
        return JsonResponse({'success': False, 'error':'Please use a valid email address.'}, status=400)
    

    role_map = {
        'student': 'Student',
        'professor': 'Professor',
        'investor': 'Investor',
    }
    normalized_role = role.lower()
    if normalized_role not in role_map:
        return JsonResponse({'success': False, 'error': 'Invalid role.'}, status=400)
    role = role_map[normalized_role]

    if Users.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'Email already registered.'}, status=409)

    try:
        user = Users.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            role=role
        )
        request.session['user_id'] = user.user_id
        request.session.modified = True
        return JsonResponse({
            'success': True,
            'message': 'Account created successfully.',
            'user': {
                'id': user.user_id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
            },
        })
    except Exception:
        return JsonResponse({'success': False, 'error': 'Failed to create account.'}, status=500)


# Authenticate a user and start a session.
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@csrf_exempt
def login_check(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    email = payload.get('email', '').strip()
    password = payload.get('password', '')

    if not email or not password:
        return JsonResponse({'success': False, 'error': 'Email and password are required.'}, status=400)

    
    try:
        user = Users.objects.get(email=email)
        # التعديل الأمني: استخدام check_password للمقارنة مع القيمة المشفّرة
        if check_password(password, user.password):
            request.session['user_id'] = user.user_id # إنشاء جلسة مؤمنة
            request.session.modified = True
            return JsonResponse({'success': True, 'user': {'id': user.user_id, 'name': user.name}})
        else:
            return JsonResponse({'success': False, 'error': 'بيانات الدخول غير صحيحة'}, status=401)
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'المستخدم غير موجود'}, status=401)
    password_valid = check_password(password, user.password)
    if not password_valid:
        if user.password != password:
            return JsonResponse({'success': False, 'error': 'Invalid email or password.'}, status=401)
        user.password = make_password(password)
        user.save(update_fields=['password'])

    request.session['user_id'] = user.user_id
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'message': 'Login successful.',
        'user': {
            'id': user.user_id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
        },
    })


# Return the currently authenticated user.
def current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)

    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)

    return JsonResponse({
        'success': True,
        'user': {
            'id': user.user_id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
        },
    })


# Log out the current session.
@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

    request.session.flush()
    return JsonResponse({'success': True, 'message': 'Logged out successfully.'})


# Return the list of approved projects.
def projects_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Use GET request.'}, status=405)

    projects = Projects.objects.filter(approval_status__iexact='approved')
    data = [serialize_project(project) for project in projects]
    return JsonResponse({'success': True, 'projects': data})


# Create a new project and owner membership.
@csrf_exempt
def create_project(request):
     user_id = request.session.get('user_id')
     if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
     if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

     payload = parse_json_body(request)
     if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

     title = payload.get('title', '').strip()
     description = payload.get('description', '').strip()
     owner_id = payload.get('owner_id')
     professor_id = payload.get('professor_id')
     status = payload.get('status', 'For Investment').strip()
     rank_badge = payload.get('rank_badge', 'General').strip()

     status_map = {
        'For Investment': 'Investment',
        'For Sale': 'Sale',
        'For Display': 'Display',
        'Investment': 'Investment',
        'Sale': 'Sale',
        'Display': 'Display',
     }
     status = status_map.get(status, 'Investment')

     if not title or not description or not owner_id or not professor_id:
        return JsonResponse({'success': False, 'error': 'Title, description, owner_id and professor_id are required.'}, status=400)

     try:
        owner = Users.objects.get(user_id=owner_id)
        professor = Users.objects.get(user_id=professor_id, role__iexact='professor')
     except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Owner or professor not found.'}, status=404)

     if owner.role.lower() != 'student':
        return JsonResponse({'success': False, 'error': 'Only students can create projects.'}, status=403)

     try:
         project = Projects.objects.create(
            title=title,
            description=description,
            owner=owner,
            professor=professor,
            status=status,
            rank_badge=rank_badge,
            approval_status='Pending Approval',
            views=0,
         )

         ProjectsMember.objects.create(
            project=project,
            user=owner,
            role_in_project='owner',
            status='accepted',
         )

         return JsonResponse({'success': True, 'project': serialize_project(project)})
     except Exception as exc:
         return JsonResponse({'success': False, 'error': str(exc)}, status=500)


# Return all projects owned by or joined by a user.
def my_projects(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)

    try:
        user = Users.objects.get(user_id=user_id)
        
        owned = Projects.objects.filter(owner=user)
        member_records = ProjectsMember.objects.filter(user=user)
        member_project_ids = member_records.values_list('project_id', flat=True)
        member_projects = Projects.objects.filter(project_id__in=member_project_ids)

        projects = []
        for project in owned:
            project_data = serialize_project(project)
            project_data['membership_status'] = 'accepted'
            project_data['membership_role'] = 'owner'
            projects.append(project_data)

        for project in member_projects:
            if project.owner and project.owner.user_id == user.user_id:
                continue
            member = member_records.filter(project=project).first()
            projects.append(serialize_project(project, member))

        return JsonResponse({'success': True, 'projects': projects})

    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Database Error: {str(e)}'}, status=500)


# Apply a user to join a project.
@csrf_exempt
def apply_project(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
    inviter_id = payload.get('inviter_id')
    if not inviter_id:
        return JsonResponse({'success': False, 'error': 'inviter_id is required.'}, status=400)

    try:
        project = Projects.objects.get(project_id=project_id)
        user = Users.objects.get(user_id=user_id)
        inviter = Users.objects.get(user_id=inviter_id)
    except (Projects.DoesNotExist, Users.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Project, user, or inviter not found.'}, status=404)

    if project.owner.user_id != inviter.user_id:
        return JsonResponse({'success': False, 'error': 'Only the project owner can invite members.'}, status=403)

    if ProjectsMember.objects.filter(project=project, user=user).exists():
        return JsonResponse({'success': False, 'error': 'Already applied or member.'}, status=409)

    ProjectsMember.objects.create(
        project=project,
        user=user,
        role_in_project='member',
        status='pending',
    )

    return JsonResponse({'success': True, 'member_id': None})


# Accept or reject a pending project invitation.
@csrf_exempt
def respond_invite(request, project_id):
     user_id = request.session.get('user_id')
     if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
     if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

     payload = parse_json_body(request)
     if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

     action = payload.get('action', '').strip().lower()

     if not action or action not in {'accept', 'reject'}:
        return JsonResponse({'success': False, 'error': 'Valid action are required.'}, status=400)

     try:
        member = ProjectsMember.objects.get(project__project_id=project_id, user__user_id=user_id)
     except ProjectsMember.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invite not found.'}, status=404)

     if member.status != 'pending':
        return JsonResponse({'success': False, 'error': 'Invite already responded to.'}, status=400)

     member.status = 'accepted' if action == 'accept' else 'rejected'
     member.save(update_fields=['status'])

     return JsonResponse({'success': True, 'status': member.status})


# Return projects assigned to a professor.
def professor_projects(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)

    try:
        user = Users.objects.get(user_id=user_id, role='Professor')
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Professor not found.'}, status=404)

    projects = Projects.objects.filter(professor=user)
    return JsonResponse({'success': True, 'projects': [serialize_project(project) for project in projects]})


# Return members for a project.
def get_project_members(request, project_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
    try:
        project = Projects.objects.get(project_id=project_id)
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found.'}, status=404)
    
    members = []
    owner_already_listed = False
    for member in project.members.select_related('user').order_by('joined_date'):
        members.append({
                'user_id': member.user.user_id,
                'role_in_project': member.role_in_project,
                'status': member.status,
                'joined_date': member.joined_date.isoformat() if member.joined_date else None,
                'name': member.user.name,
                'email': member.user.email,
            })
        if project.owner and member.user.user_id == project.owner.user_id:
                owner_already_listed = True
                
                if project.owner and not owner_already_listed:
                    members.append({
            'user_id': project.owner.user_id,
            'role_in_project': 'owner',
            'status': 'accepted',  # Owner is always accepted
            'joined_date': None,
            'name': project.owner.name,
            'email': project.owner.email,
        })

    return JsonResponse({'success': True, 'members': members})


# Approve or reject a project.
@csrf_exempt
def approve_project(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    approval_status = payload.get('approval_status')
    status_map = {
        'approved': 'Approved',
        'rejected': 'Rejected',
    }

    if approval_status not in status_map:
        return JsonResponse({'success': False, 'error': 'Invalid status.'}, status=400)

    try:
        project = Projects.objects.get(project_id=project_id)
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found.'}, status=404)

    project.approval_status = status_map[approval_status]
    project.approval_date = datetime.utcnow()
    project.save()
    
    return JsonResponse({'success': True, 'project': serialize_project(project)})

# Record a professor's grade for a project.
@csrf_exempt
def grade_project(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
    try:
        current_user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)
    if current_user.role != 'Professor':
        return JsonResponse({'success': False, 'error': 'Only professors can grade projects.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    project_id = payload.get('project_id')
    student_id = payload.get('student_id')
    professor_id = payload.get('professor_id')
    score_average = payload.get('score_average')
    feedback = payload.get('feedback', '')

    if not project_id or not student_id or not professor_id or score_average is None:
        return JsonResponse({'success': False, 'error': 'project_id, student_id, professor_id, and score_average are required.'}, status=400)

    try:
        project = Projects.objects.get(project_id=project_id)
        student = Users.objects.get(user_id=student_id)
        professor = Users.objects.get(user_id=professor_id, role='Professor')
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student or professor not found.'}, status=404)
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found.'}, status=404)

    # Check if the student is a member of the project or the owner
    is_member = ProjectsMember.objects.filter(project=project, user=student, status='accepted').exists()
    is_owner = project.owner and project.owner.user_id == student.user_id
    if not (is_member or is_owner):
        return JsonResponse({'success': False, 'error': 'Student is not a member or owner of this project.'}, status=400)

    evaluation = Evaluations.objects.create(
        project=project,
        student=student,
        professor=professor,
        score_average=score_average,
        feedback=feedback,
        evaluation_date=datetime.utcnow(),
    )

    project.professor_score = score_average
    project.save()

    return JsonResponse({'success': True, 'evaluation_id': evaluation.evaluation_id})


# Return all grades for a project.
def get_project_grades(request, project_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
    try:
        project = Projects.objects.get(project_id=project_id)
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found.'}, status=404)

    grades = []
    for evaluation in Evaluations.objects.filter(project=project).select_related('student', 'professor').order_by('-evaluation_date'):
        grades.append({
            'evaluation_id': evaluation.evaluation_id,
            'student_id': evaluation.student.user_id,
            'student_name': evaluation.student.name,
            'professor_id': evaluation.professor.user_id,
            'professor_name': evaluation.professor.name,
            'score_average': float(evaluation.score_average) if evaluation.score_average is not None else None,
            'feedback': evaluation.feedback,
            'evaluation_date': evaluation.evaluation_date.isoformat() if evaluation.evaluation_date else None,
        })

    return JsonResponse({'success': True, 'grades': grades})


# Record a new investment for a project.
@csrf_exempt
def invest_project(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
    try:
        current_user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)
    if current_user.role != 'Investor':
        return JsonResponse({'success': False, 'error': 'Only investors can invest in projects.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    project_id = payload.get('project_id')
    investor_id = payload.get('investor_id')
    amount = payload.get('amount')

    if not project_id or not investor_id or amount is None:
        return JsonResponse({'success': False, 'error': 'project_id, investor_id and amount are required.'}, status=400)

    try:
        project = Projects.objects.get(project_id=project_id)
        investor = Users.objects.get(user_id=investor_id, role='Investor')
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Investor not found.'}, status=404)
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found.'}, status=404)

    if Investments.objects.filter(project=project, investor=investor).exists():
        return JsonResponse({'success': False, 'error': 'Investor already invested in this project.'}, status=409)

    investment = Investments.objects.create(
        project=project,
        investor=investor,
        amount=amount,
        status='active',
    )

    return JsonResponse({'success': True, 'investment_id': investment.investment_id})


# Save an investor rating for a project.
@csrf_exempt
def rate_project(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated.'}, status=401)
    try:
        current_user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)
    if current_user.role != 'Investor':
        return JsonResponse({'success': False, 'error': 'Only investors can rate projects.'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Use POST request.'}, status=405)

    payload = parse_json_body(request)
    if payload is None:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    project_id = payload.get('project_id')
    investor_id = payload.get('investor_id')
    rating = payload.get('rating')
    review = payload.get('review', '')

    if not project_id or not investor_id or rating is None:
        return JsonResponse({'success': False, 'error': 'project_id, investor_id and rating are required.'}, status=400)

    if int(rating) < 1 or int(rating) > 5:
        return JsonResponse({'success': False, 'error': 'Rating must be between 1 and 5.'}, status=400)

    try:
        project = Projects.objects.get(project_id=project_id)
        investor = Users.objects.get(user_id=investor_id, role='Investor')
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Investor not found.'}, status=404)
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found.'}, status=404)

    if InvestorRatings.objects.filter(project=project, investor=investor).exists():
        return JsonResponse({'success': False, 'error': 'Investor already rated this project.'}, status=409)

    rating_obj = InvestorRatings.objects.create(
        project=project,
        investor=investor,
        rating=rating,
        review=review,
    )

    return JsonResponse({'success': True, 'rating_id': rating_obj.rating_id})
