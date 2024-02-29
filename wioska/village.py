class Village:
    def __init__(self, name):
        self.name = name
        self.residents = []

    def add_resident(self, person):
        self.residents.append(person)
        print(f"{person.name} has moved into {self.name}.")

    def list_residents(self):
        return [person.name for person in self.residents]

class Person:
    def __init__(self, name):
        self.name = name

    def speak(self, words):
        return f"{self.name} says: '{words}'"

# Create a village
my_village = Village("Greenwood")

# Create two people
alice = Person("Alice")
bob = Person("Bob")

# Add them to the village
my_village.add_resident(alice)
my_village.add_resident(bob)

# Test interaction
print(alice.speak("Hello, Bob!"))
