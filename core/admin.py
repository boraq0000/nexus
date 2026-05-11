from django.contrib import admin
from .models import Users, Projects, Evaluations, Investments, InvestorRatings

# Register the Users model in the Django admin.
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'role')
    search_fields = ('name', 'email')

# Register the Projects model in the Django admin.
@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'title', 'owner', 'professor', 'status', 'approval_status', 'professor_score')
    list_filter = ('status', 'approval_status')

# Register the Evaluations model in the Django admin.
@admin.register(Evaluations)
class EvaluationsAdmin(admin.ModelAdmin):
    list_display = ('evaluation_id', 'project', 'score_average', 'evaluation_date')

# Register the Investments model in the Django admin.
@admin.register(Investments)
class InvestmentsAdmin(admin.ModelAdmin):
    list_display = ('investment_id', 'investor', 'project', 'amount', 'status', 'investment_date')
    list_filter = ('status',)
    search_fields = ('project__title', 'investor__name')

# Register the InvestorRatings model in the Django admin.
@admin.register(InvestorRatings)
class InvestorRatingsAdmin(admin.ModelAdmin):
    list_display = ('rating_id', 'investor', 'project', 'rating', 'rating_date')
    list_filter = ('rating',)
    search_fields = ('project__title', 'investor__name')

# ProjectsMember cannot be registered in admin because the DB table has no single id PK.
# admin.site.register(ProjectsMember)
# admin.site.register(ProjectAttachments)