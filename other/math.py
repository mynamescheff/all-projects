import random
import numpy as np

#set a chance of an event happening to 26%
def chance26():
    return random.randint(1, 100) <= 26

#show the probability of an event not happening 7 times in a row
def prob7n():
    return (1 - 0.26)**7

#show the probability of an event happening at least once in 7 tries
def prob7y():
    return 1 - (1 - 0.26)**7

#create a function to print those
def print_prob():
    print("Probability of an event not happening 7 times in a row: ", prob7n())
    print("Probability of an event happening at least once in 7 tries: ", prob7y())

print_prob()

#show standard deviation for this event
def std_dev():
    return np.sqrt(7 * 0.26 * 0.74)

#create a general function with inputs of probability and number of tries based on user input
def prob_y(prob, tries):
    return 1 - (1 - prob)**tries

def prob_n(prob, tries):
    return (1 - prob)**tries

#ask user for input and convert to percentage
prob = float(input("Enter probability of an event happening: ")) / 100
tries = int(input("Enter number of tries: "))
print("Probability of an event not happening: ", prob_n(prob, tries))
print("Probability of an event happening at least once: ", prob_y(prob, tries))
