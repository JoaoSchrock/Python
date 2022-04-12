def insertion_sort(l):
    for i in range(1,len(l)):
        j=i-1
        key=l[i]
        while (l[j]>key) and (j>=0):
            l[j+1]=l[j]
            j-=1
        l[j+1]=key
    return l

assert insertion_sort([1,2,3,9,8,7])==[1,2,3,7,8,9]
