def wrapper1(func, *args):  # with star
  func(*args)


def wrapper2(func, args):  # without star
  func(*args)


def func2(x, y, z):
  print(x + y + z)


wrapper1(func2, 1, 2, 3)
wrapper2(func2, [1, 2, 3])

# def tupletest(*tuple):
#     print(*tuple)
#
#
# tupletest(1, 23)
#
#
# def dicttest(self,**dictir):
#     print(dictir)
#
#
# dictir = {
#     'key1': 'value1',
#     'key2': 'value2',
# }
# dicttest([1,2,3])
