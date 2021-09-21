from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from music_site import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from musix.models import Sample, Audio
from django.core.files.uploadedfile import SimpleUploadedFile
from music_site.forms import AudioUploadForm, UserRegisterForm


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('merab', 'merab@gmail.com', 'merab')

    def test_login(self):
        self.client.login(username='merab', password='merab')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        self.client.login(username='merab', password='merab')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        self.client.login(username='merab', password='merab')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    # No login required

    def test_welcome_GET(self):
        client = Client()
        response = client.get(reverse('welcome'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_site/welcome.html')

    def test_upload_list_GET(self):
        client = Client()
        response = client.get(reverse('upload_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_site/upload_list.html')

    def test_register_GET(self):
        client = Client()
        response = client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'music_site/register.html')

    def test_register_POST(self):
        client = Client()
        user = {
            'username': 'merab10',
            'email': 'merabul@gmail.com',
            'password1': 'catdog619',
            'password2': 'catdog619'
        }
        response = client.post(reverse('register'), data=user)
        self.assertEqual(response.status_code, 302)

    def test_register_POST_fail(self):
        client = Client()
        user = {
            'username': 'merab10',
            'email': 'merabul@gmail.com',
            'password1': 'password',
            'password2': 'catdog619'
        }
        response = client.post(reverse('register'), data=user)
        self.assertEqual(response.status_code, 302)


class TestModels(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('merab', 'merab@gmail.com', 'merab')

    def test_audio_create(self):
        audio = Audio.objects.create(uploader=self.user, title='Title', genre='Genre', instrument='Guitar', key='A',
                                     mp3=SimpleUploadedFile("test.mp3", ""), sample_count=0)
        self.assertTrue(isinstance(audio, Audio))
        self.assertEqual(audio.title, 'Title')

    def test_audio_create_fail(self):
        audio = Audio.objects.create(title='Title', genre='Genre', instrument='Guitar', key='A',
                                     mp3=SimpleUploadedFile("test.mp3", ""), sample_count=0)
        self.assertTrue(isinstance(audio, Audio))
        self.assertEqual(audio.title, 'Title')

    def test_sample_create(self):
        audio1 = Audio.objects.create(uploader=self.user, title='Title1', genre='Genre', instrument='Guitar', key='A',
                                      mp3=SimpleUploadedFile("test,txt,", ""), sample_count=0)
        audio2 = Audio.objects.create(uploader=self.user, title='Title2', genre='Genre', instrument='Guitar', key='A',
                                      mp3=SimpleUploadedFile("test,txt,", ""), sample_count=0)
        sample = Sample.objects.create(main=audio1, sub=audio2)
        self.assertTrue(isinstance(sample, Sample))
        self.assertEqual(sample.main.title, 'Title1')
        self.assertEqual(sample.sub.title, 'Title2')


class TestUrls(SimpleTestCase):
    def test_url_resolved_home(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.home)

    def test_url_resolved_details(self):
        url = reverse('details', args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, views.Details)

    def test_url_resolved_add_sample(self):
        url = reverse('add_sample', args=[1, 1])  # args represent parameters
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.addSample)

    def test_url_resolved_register(self):
        url = reverse('register')
        print(resolve(url))
        self.assertEquals(resolve(url).func, views.register)

    def test_url_resolved_login(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)
