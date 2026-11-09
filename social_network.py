"""Model a small, undirected social network with an adjacency list."""


class Person:
    def __init__(self, name):
        self.name = name
        self.friends = []

    def add_friend(self, friend):
        if friend is not self and friend not in self.friends:
            self.friends.append(friend)


class SocialNetwork:
    def __init__(self):
        self.people = {}

    def add_person(self, name):
        if name in self.people:
            print(f"Person not added. {name} already exists!")
            return
        self.people[name] = Person(name)

    def add_friendship(self, person1_name, person2_name):
        missing = [name for name in (person1_name, person2_name)
                   if name not in self.people]
        if missing:
            print(f"Friendship not created. {', '.join(dict.fromkeys(missing))} doesn't exist!")
            return
        if person1_name == person2_name:
            print("Friendship not created. A person cannot be their own friend!")
            return
        person1 = self.people[person1_name]
        person2 = self.people[person2_name]
        person1.add_friend(person2)
        person2.add_friend(person1)

    def print_network(self):
        for person in self.people.values():
            friends = ', '.join(friend.name for friend in person.friends)
            print(f"{person.name} is friends with: {friends or '(none)'}")


def main():
    network = SocialNetwork()
    for name in ("Alex", "Jordan", "Morgan", "Taylor", "Casey", "Riley"):
        network.add_person(name)
    for first, second in (
        ("Alex", "Jordan"), ("Alex", "Morgan"), ("Jordan", "Taylor"),
        ("Morgan", "Casey"), ("Taylor", "Riley"), ("Casey", "Riley"),
        ("Morgan", "Riley"), ("Alex", "Taylor"),
    ):
        network.add_friendship(first, second)
    network.add_friendship("Jordan", "Johnny")
    original_alex = network.people["Alex"]
    network.add_person("Alex")
    assert network.people["Alex"] is original_alex
    network.add_friendship("Alex", "Jordan")
    network.add_friendship("Alex", "Alex")
    assert len(network.people) == 6
    assert sum(len(p.friends) for p in network.people.values()) == 16
    for person in network.people.values():
        assert len(person.friends) == len(set(person.friends))
        assert person not in person.friends
        for friend in person.friends:
            assert person in friend.friends
    network.print_network()


if __name__ == "__main__":
    main()

# DESIGN MEMO
# A graph is the right structure for a social network because people can have
# many connections, and those connections do not follow a single hierarchy.
# Each Person is a vertex, and each friendship is an undirected edge. Keeping
# both people in each other's friends list makes the relationship mutual.
# Cycles are allowed: Alex can know Jordan, Jordan can know Taylor, and Taylor
# can also know Alex. Disconnected people can belong to the same network.
#
# A single list could store everyone's names, but it would not directly describe
# their relationships. We would need another structure to record connections.
# A tree introduces a parent-child hierarchy and cannot naturally represent
# cycles or arbitrary friendships without breaking its defining structure.
# A graph directly represents the relationships the application needs.
#
# This implementation uses an adjacency list. The dictionary finds people by
# name in average O(1) time, while each person's list stores their neighbors.
# Adding a new person is average O(1). Checking for an existing friend scans
# the list, so adding a friendship costs O(d1 + d2), where d1 and d2 are the
# two people's numbers of friends. Preventing duplicates makes additions slower
# than simply appending, but keeps repeated requests from creating extra edges.
# Printing visits every person and every adjacency entry, taking O(V + E)
# time. Each friendship appears twice, once per endpoint. Storage is O(V + E),
# which suits a sparse network better than an O(V squared) adjacency matrix.
# Names must be unique here; a larger system should use stable user IDs.
