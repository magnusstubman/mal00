s = '1234567890fewuhfuhwoh89fu23890f8wehuy89yh238fh4'
o = []
while s:
    o.append(s[:3])
    s = s[3:]


for l in o:
  print(l)
