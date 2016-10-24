temp = "test".encode()
print(temp)


temp = "test".encode('utf-8')
print(temp)

temp2 = temp.decode('utf-8')
print(temp2)