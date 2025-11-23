import numpy as np

def create_array():
    user_input=input("\nEnter numbers separated by spaces:")
    try:
        arr=np.array([float(x) for x in user_input.split()])
        print("\nArray created:",arr)
        return arr
    except:
        print("Invalid input. Try again.")
        return create_array()


def menu():
    print("""
------------------------------
   NUMPY DATA EXPLORER
------------------------------
1. Create new array
2. Index value
3. Slice array
4. Mathematical operation (+, -, *, /)
5. Axis-wise sum / mean
6. Reshape array
7. Broadcasting example
8. Save array to file
9. Load array from file
10. Compare performance (NumPy vs Python list)
0. Exit
-----------------------------
""")

def main():
    arr=None

    while True:
        menu()
        choice=input("Enter choice: ")

        if choice=="1":
            arr=create_array()

        elif choice=="2":
            if arr is None:
                print("Create an array first!")
                continue
            idx=int(input("Enter index: "))
            print("Value at index:",arr[idx])

        elif choice=="3":
            if arr is None:
                print("Create an array first!")
                continue
            start=input("Start index: ")
            end=input("End index: ")
            print("Slice:", arr[int(start):int(end)])

        elif choice=="4":
            if arr is None:
                print("Create an array first!")
                continue
            op=input("Choose operation (+, -, *, /): ")
            val=float(input("Enter value: "))
            if op=="+":
                print(arr+val)
            elif op=="-":
                print(arr-val)
            elif op=="*":
                print(arr*val)
            elif op=="/":
                print(arr/val)

        elif choice=="5":
            if arr is None:
                print("Create an array first!")
                continue
            print("Sum:",np.sum(arr))
            print("Mean:",np.mean(arr))

        elif choice=="6":
            if arr is None:
                print("Create an array first!")
                continue
            r=int(input("Rows: "))
            c=int(input("Columns: "))
            print(arr.reshape(r,c))

        elif choice=="7":
            if arr is None:
                print("Create an array first!")
                continue
            val=float(input("Enter value to broadcast add: "))
            print("Result:",arr+val)

        elif choice=="8":
            if arr is None:
                print("Create an array first!")
                continue
            filename=input("Enter filename: ")
            np.save(filename,arr)
            print("Saved successfully!")

        elif choice=="9":
            filename=input("Enter filename to load: ")
            try:
                arr=np.load(filename+".npy")
                print("Loaded:",arr)
            except Exception as e:
                print(e)

        elif choice=="10":
            import time
            N=1000000

            py_list=list(range(N))
            np_arr=np.arange(N)

            print("\nComparing Python list vs NumPy array...")

            t1=time.time()
            py_list=[x*2 for x in py_list]
            t2=time.time()

            t3=time.time()
            np_arr=np_arr*2
            t4=time.time()

            print("Python list time:",t2-t1)
            print("NumPy array time:",t4-t3)

        elif choice=="0":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice, try again.")

main()

