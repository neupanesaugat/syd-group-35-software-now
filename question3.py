# Function to define grade for the students

from numpy import average


def get_grade(score):
    if 85 <= score <= 100:
        return "HD"
    elif 75 <= score <= 84:
        return "D"
    elif 65 <= score <= 74:
        return "C"
    elif 50 <= score <= 64:
        return "P"
    else:
        return "F"

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
students = []
total_score = 0

for i in range(n):
    name = input(f'Student{i+1} name: ')

    while True:
        try:
            score = int(input(f"{name}'s score: "))
            if 0 <= score <= 100:
                break
            else:
                print('The score must be between 0 and 100.')
        except ValueError:
            print('Invalid! Please enter a number.')

    grade = get_grade(score)
    students.append((name, score, grade))
    total_score += score

# Calculating average score 
average_score = total_score/n

# Finding highest and lowest score
highest_score = max(students, key=lambda x: x[1])
lowest_score = min(students, key=lambda x: x[1])

# Displaying results

print("\nResults:")
for name,score,grade in students:
    print(f'{name}: {score} ({grade})')

print(f'Average score: {average_score:.2f}')
print(f'Highest: {highest_score[0]} ({highest_score[1]})')
print(f'Lowest: {lowest_score[0]} ({lowest_score[1]})')


