#calculate additive persistence and additive root and print them
def additive_persistence_root(number):
    #Checking for single digit and printing
    if(number>=1 and number<=9):
        print("Additive Persistence=", 0, ",Additive Root=", number)
    else:
        count = 0  # To store persistence, means how many time the below loop runs
        # This loop will stop when number reacehs to single digits
        while (number > 9):
            count += 1  # Adding 1 to count
            sum = 0

            while (number > 0):
                # Finding remainder of number

                rem = number % 10

                sum = sum + rem

                number = number // 10  # Excluding last digit


            # Reassigninig number with mulplication
            number = sum



        # Printing result
        print("Additive Persistence=", count, ",Additive Root=", sum)

# Function to calculate multiplicative persistence and multiplicative root and print them
def mulplicative_persistence_root(number):
    # Checking for single digit and printing
    if (number >= 1 and number <= 9):
        print("Multiplicative Persistence=",0,",Multiplicative Root=",number)
    else:
        count=0 #To store persistence, means how many time the below loop runs

        #This loop will stop when number reacehs to single digis
        while(number>9):
            count +=1 #Adding 1 to count
            mul=1
            while(number>0):
                #Finding remainder of number
                rem=number%10
                mul=mul*rem
                number=number//10 #Excluding last digit

            #Reassigninig number with mulplication
            number=mul

        #Printing result
        print("Multiplicative Persistence=", count, ",Multiplicative Root=", mul)


#Driver part of the program
if __name__ == '__main__':
    #Running Infinite loop until user enters negative number
    while(True):
        #Asking user for a number
        number=int(input("Enter a Integer ( Enter a negative number to quit): "))
        #checking if number is negative then breaking loop and stopping program
        if(number<0):
            print("Thanks for playing along!")
            break
        else: # if number is positive calling above functions to calculate persistence
            print("For Integer:",number )

            # Calling additive persistence function
            additive_persistence_root(number)


            #Calling mulplicative persistence function
            mulplicative_persistence_root(number)

        #Adding a new line in output
        print()