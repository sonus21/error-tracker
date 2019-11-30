from django.http import HttpResponse


def index(request):
    return HttpResponse('No Exception!')


def value_error(request):
    raise ValueError


def post_view(request):
    form = request.POST
    password = "qwerty"
    secret = "pass"
    key = "key"
    foo_secret = "THIS IS SECRET"
    test_password_test = "test_password_test"
    TestPassWordTest = "TestPassWordTest"
    TestSecret = "TESTSECRET"
    l = [1, 2, 3, 4]
    t = (1, 2, 3, 4)
    d = {'test': 100, "1": 1000}
    print(form, password, secret, key, d, foo_secret,
          TestPassWordTest, test_password_test, TestSecret, l, t, d)
    print(d['KeyError'])
    return "KeyError"
