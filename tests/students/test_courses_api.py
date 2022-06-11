import pytest
from rest_framework.test import APIClient
from students.models import Student, Course
from model_bakery import baker
from students.filters import CourseFilter
import random

FACTORY_QUANTITY = 10

@pytest.fixture
def client():
	return APIClient()


@pytest.fixture
def student():
	return Student.objects.create(name = 'Vasya')


@pytest.fixture
def course_factory():
	def factory(*args, **kwargs):
		return baker.make(Course, *args, **kwargs)
	return factory


@pytest.fixture
def student_factory():
	def factory(*args, **kwargs):
		return baker.make(Student, *args, **kwargs)
	return factory


#
# Получение одного курса
#
@pytest.mark.django_db
def test_get_one_course(client,course_factory):
	courses = course_factory(_quantity=FACTORY_QUANTITY)
	index = random.randint(0,FACTORY_QUANTITY-1)
	course_id = courses[index].id
	response = client.get(f'/api/v1/courses/{course_id}/')
	assert response.status_code in [200,202,204]
	assert course_id == response.json()['id']


#
# Проверка получения списка курсов
#
@pytest.mark.django_db
def test_get_courses_list(client, course_factory):
	# Arrange
	courses = course_factory(_quantity=FACTORY_QUANTITY)

	# Act
	response = client.get('/api/v1/courses/')

	# Assert
	assert response.status_code == 200
	data = response.json()
	assert len(data) == len(courses)
	for i, c in enumerate(data):
		assert c['name'] == courses[i].name


#
# Проверка фильтрации списка курсов по id
#
@pytest.mark.django_db
def test_check_id_filter(client, course_factory):
	courses = course_factory(_quantity=FACTORY_QUANTITY)
	index = random.randint(0,FACTORY_QUANTITY-1)
	course_id = courses[index].id
	
	response = client.get(f'/api/v1/courses/?id={course_id}')
	assert response.status_code in [200, 201]
	data = response.json()
	assert len(data) == 1
	assert data[0]['id']== course_id


#
# Проверка фильтрации списка курсов по name
#
@pytest.mark.django_db
def test_check_name_filter(client, course_factory):
	print('Проверка фильтрации списка курсов по name')
	courses = course_factory(_quantity=FACTORY_QUANTITY)
	index = random.randint(0,FACTORY_QUANTITY-1)
	course_name = courses[index].name
	
	response = client.get(f'/api/v1/courses/?name={course_name}')
	assert response.status_code in [200, 201]
	data = response.json()
	assert len(data)  > 0
	for i in range(len(data)):
		assert data[i]['name']== course_name


#
# Тест успешного создания курса
#
@pytest.mark.django_db
def test_create_course(client,student):
	print('Тест успешного создания курса')
	count = Course.objects.count()
	response= client.post('/api/v1/courses/', data={'students' : student.id,'name':'LITERATURE'})
	assert response.status_code == 201
	assert Course.objects.count() == count + 1


#
# Тест успешного обновления курса
#
@pytest.mark.django_db
def test_update_course(client,course_factory):
	courses = course_factory(_quantity=FACTORY_QUANTITY)
	index = random.randint(0,FACTORY_QUANTITY-1)
	course_id = courses[index].id
	response= client.patch(f'/api/v1/courses/{course_id}/', data={'name':'_updated_'})
	assert response.status_code in [200,204]
	

#
# Тест успешного удаления курса
#
@pytest.mark.django_db
def test_remove_course(client,course_factory):
	courses = course_factory(_quantity=FACTORY_QUANTITY)
	index = random.randint(0,FACTORY_QUANTITY-1)
	course_id = courses[index].id 
	response= client.delete(f'/api/v1/courses/{course_id}/')
	assert response.status_code in [200,202,204]
