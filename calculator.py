"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

def home(*args):
  """ Returns a STRING with the instructions """

  return """
  This online calculator can perform several operations:<br>
  <br>
  * Addition<br>
  *  Subtractions<br>
  * Multiplication<br>
  * Division<br>
  <br>
  You can send appropriate requests with the operation and operands,<br>
  and get back proper responses. For example, if you open a browser to the wsgi<br>
  application at `http://localhost:8080/add/3/5' then the response<br>
  body in the browser should be `8`.)
  """


def add(*args):
  """ Returns a STRING with the sum of the arguments """

  # TODO: Fill sum with the correct value, based on the
  # args provided.
  return 'The answer is {}'.format(str(sum(args)))



# TODO: Add functions for handling more arithmetic operations.

def subtract(*args):
  return 'The answer is {}'.format(str(args[0] - args[1]))


def multiply(*args):
  return 'The answer is {}'.format(str(args[0] * args[1]))


def divide(*args):
  try: 
    return 'The answer is {}'.format(str(args[0] / args[1]))
  except ZeroDivisionError:
    return 'Zero Division Error: Cannot divide the number by 0.'



def home():
    body = """
    <h1>Calculator Instruction</h1>
    Perform the calculation by inserting one of the following:
    <ul>
    <li>add</li>
    <li>subtract</li>
    <li>multiply</li>
    <li>divide</li>
    </ul>
    in the address bar followed by two numbers you want to do the calculation.<br>
    <br>
    For example:<br>
    localhost:8080/add/4/5<br>
    <br>
    You will get a returned answer (9) on the page.
    """

    return body


def resolve_path(path):
  """
  Should return two values: a callable and an iterable of
  arguments.
  """

  # TODO: Provide correct values for func and args. The
  # examples provide the correct *syntax*, but you should
  # determine the actual values of func and args using the
  # path.
  # func = add
  # args = ['25', '32']

  funcs = {
    '': home,
    'add': add,
    'subtract': subtract,
    'divide': divide,
    'multiply': multiply
  }

  path = path.strip('/').split('/')

  func_name = path[0]
  # args = path[1:]
  args = [float(x) for x in path[1:]]

  try:
    func = funcs[func_name]
  except (KeyError, ValueError):
    raise NameError

  return func, args





def application(environ, start_response):
  # TODO: Your application code from the book database
  # work here as well! Remember that your application must
  # invoke start_response(status, headers) and also return
  # the body of the response in BYTE encoding.
  #
  # TODO (bonus): Add error handling for a user attempting
  # to divide by zero.

  headers = [('Content-type', 'text/html')]
  body = '<a href="/"">Calculator Instruction Page</a>'
  try:
    path = environ.get('PATH_INFO', None)
    if path is None:
      raise NameError
    func ,args = resolve_path(path)
    body += "<h1>" + func(*args) + "</h1>"
    status = "200 OK"
  except NameError:
    status = '404 Not Found'
    body += "<h1>Not Found</h1>"
  except Exception:
    status = "500 Internal Server Error"
    body += "<h1>Internal Server Error</h1>"
    print(traceback.format_exc())
  finally:
    headers.append(('Content-length', str(len(body))))
    start_response(status, headers)
    return [body.encode('utf8')]



if __name__ == '__main__':
  # TODO: Insert the same boilerplate wsgiref simple
  # server creation that you used in the book database.

  from wsgiref.simple_server import make_server
  srv = make_server('localhost', 8080, application)
  srv.serve_forever()
