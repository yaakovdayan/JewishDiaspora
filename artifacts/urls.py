from django.urls import path
from . import views


app_name = 'artifacts'

urlpatterns = [
    path('users/', views.ArtifactUsersListView.as_view(), name='users'),
    path('all/', views.ArtifactFullListView.as_view(), name='all_artifacts'),
    path('<int:pk>/', views.ArtifactDetailView.as_view(), name='detail'),
    path('create/step/one/', views.ArtifactCreateStepOneView.as_view(), name='create_step_one'),
    path('create/step/two/', views.ArtifactCreateStepTwoView.as_view(), name='create_step_two'),
    path('<int:pk>/create/step/three/', views.ArtifactCreateStepThreeView.as_view(), name='create_step_three'),
    path('area/create/', views.OriginAreaCreateView.as_view(), name='origin_area_create'),
    path('area/update/<int:pk>/', views.OriginAreaUpdateView.as_view(), name='origin_area_update'),
    path('material/list/', views.ArtifactMaterialListView.as_view(), name='material_list'),
    path('material/create/', views.ArtifactMaterialCreateView.as_view(), name='material_create'),
    path('material/update/<int:pk>/', views.ArtifactMaterialUpdateView.as_view(), name='material_update'),
    path('material/delete/<int:pk>/', views.ArtifactMaterialDeleteView.as_view(), name='material_delete'),
    path('area/list/', views.OriginAreaListView.as_view(), name='origin_area_list'),
    path('new/', views.TheNewForm.as_view(), name='artifacts_donors_registration'),
    path('personal_info/', views.PersonalInformationRegistrationPage.as_view(), name='PersonalInformationRegistrationPage'),
    path('artifact_info/', views.ArtifactInformationRegistrationPage.as_view(), name='ArtifactInformationRegistrationPage'),
    path('user_artifact_info/<int:pk>/', views.UserArtifactInformationPage.as_view(), name='artifact_information'),
    path('artifact_images/', views.ArtifactsImagesRegistrationPage.as_view(), name='ArtifactsImagesRegistrationPage'),
    path('image/create/', views.ArtifactImageCreateView.as_view(), name='image_create'),
]
