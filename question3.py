



# Input number of students

while True:
    try:
        n = int(input('Enter number of students: '))
        if 3 <= n <= 10:
            break
        else:
            print('Number of students cannot be less than 3 or greater than 10.')
    except ValueError:
        print('Invalid! Please enter a number.')


# Input student data
for i in range(n):
    name = input(f'Student{i+1} name: ')

    while True:
        try:
            score = int(input(f'{name}s score'))
            if 0 <= score <= 100:
                break
            else:
                print('The score must be between 0 and 100.')
        except ValueError:
            print('Invalid! Please enter a number.')

        
