import time
import random
import multiprocessing
from concurrent import futures


def merge(L,R,arr):
    i = j = k = 0

    # copy data into temporary array named L and R
    while i < len(L) and j < len(R):
        if L[i] < R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    
    # check if there is any element left
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1
    return arr


def mergeSort(arr):

    if len(arr) > 1:

        # finds the middle element of the array
        mid = len(arr) // 2

        # splits array elements into 2 parts (Left & Right)
        L = arr[:mid]
        #print(L)
        R = arr[mid:]
        #print(R)
        # Sort first half
        mergeSort(L)

        # Sort second half
        mergeSort(R)
        return merge(L,R,arr)

    else:
        return arr


def parallelMergeSort(arr,cpu_count=multiprocessing.cpu_count()):
# By default, unless cpu count is entered specifically, it takes the number of processors from the system.
# run until the number of processors is reduced to 1
# halve the number of processors. (2 processors go to each pool) Determines how many more times it can enter
# For example, if the number of processors is 16, it can enter 2 to 4 times, while reaching a depth of 4 units, it runs 16 processes.
# Since pool expects an iterable value, we add a separate list to the left and right lists.
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        full = [left, right]
        if cpu_count == 1:
            l = mergeSort(left)
            r = mergeSort(right)
            return merge(l,r,arr)

        else:
            result = []
            with futures.ProcessPoolExecutor(cpu_count) as p:
                cpu_count = cpu_count // 2
                if cpu_count > 0:

                    cpu_countlist = [cpu_count,cpu_count]
                    future = p.map(parallelMergeSort,full,cpu_countlist)
                    for value in future:
                        result.append(value)

            return merge(result[0],result[1],arr)


def main():
    print(time.time())
    randomList = []
    choice=-1
    

    def Menu(choice):
        
        if choice==0:
            randomList.clear()
            fileName = input("Enter file name : ")
            with open(fileName, 'r') as f:
                for line in f.readlines():
                    randomList.append(int(line))

        if choice==1:
            randomList.clear()
            size = int(input("Enter the array size : "))
            for i in range(0, size):
                n = random.randint(1, size*10)
                randomList.append(n)

            #Make copies of array for sorting

        if choice==2:
            print("Generate list (Size=%s) : " %len(randomList))
            print(randomList)

        if choice==3:
            startTime = time.time()
            print("Given array is processing in serial, please wait...", end="\n")
            sorted = mergeSort(randomList)
            endTime = time.time()
            timeTaken = endTime - startTime
            print("Array is sorted, please check your dir for output file", end="\n")
            print("Sorting done in %s seconds" % (timeTaken))
            with open('sortedList_Seq.txt', 'w') as filehandler:
                filehandler.write('\nSorting Algorithm : Sequential Merge Sort')
                filehandler.write('\nTime Taken :%s' %(timeTaken))
                for listitem in sorted:
                    filehandler.write('%s\n' % listitem)

        if choice==4:
            startTime = time.time()

            print("Given array is processing in parallel, please wait...", end="\n")
            sorted = parallelMergeSort(randomList)
            endTime = time.time()
            timeTaken = endTime - startTime
            print("Array is sorted", end="\n")
            print("Sorting done in %s seconds" % (timeTaken))
            with open('sortedList_Parl.txt', 'w') as filehandler:
                filehandler.write('\nSorting Algorithm : Parallel Merge Sort')
                filehandler.write('\nTime Taken :%s' %(timeTaken))
                for listitem in sorted:
                    filehandler.write('%s\n' % listitem)

        if choice==5:
            print("This machine have %s cores" %(multiprocessing.cpu_count()))
    
    while choice!=6:
        print("\n\nWelcome, choose a choice from the MENU below :")
        print("0 - Set external input .txt")
        print("1 - Set new array size")
        print("2 - View generated list")
        print("3 - Do serial sorting")
        print("4 - Do parallel sorting")
        print("5 - See device core information")
        print("6 - EXIT")
        choice = int(input("Your Choice : "))
        print("-----------------------------------\n")
        Menu(choice)

if __name__ == '__main__':
    main()