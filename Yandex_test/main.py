n, m = input().split()
n = int(n)
m = int(m)

rel_list = []
for i in range(n):
    rel_list.append([int(input()),i])

arr = []
for i in range(m):
    arr.append([])
for i in range(n):
    arr[rel_list[i][0]].append(rel_list[i])

s_otv = ''

def pick(ignor):
    global s_otv
    if arr == [[]]*m:
        return
    i = 0
    j = 0
    min = n+1

    for col_ind in range(len(arr)):
        for row_ind in range(len(arr[col_ind])):

            if(arr[col_ind][row_ind][1] < min and ignor != col_ind):

                i = col_ind
                j = row_ind

                min = arr[i][j][1]
            break

    if(min == n+1):
        return
    # print(min)
    s_otv += str(min)+' '
    del arr[i][j]

    pick(i)


pick(n+1)
print(s_otv[:-1])

