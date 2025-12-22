# sample_code/bad_code.py
def calc(a,b):
 if a>10:
  if b>10:
   if a>b:
    return a-b
   else:
    return b-a
  else:
   if a==b:return 0
   else:return a+b
 else:
  for i in range(0,10):
   print(i)
 return None
