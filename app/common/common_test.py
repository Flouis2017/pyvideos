
arrStr = ""
arr = [1, 2, 3]
# for id in arr:
#     arrStr += str(id) + ","
# arrStr = arrStr[:-1]
arrStr = ",".join(map(lambda v: str(v), arr))
print(arrStr)
