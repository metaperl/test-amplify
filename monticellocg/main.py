# core

import itertools
import sys
import logging

# 3rd party

import argh
import enum


logging.basicConfig(
    format='%(lineno)s %(message)s',
    level=logging.DEBUG
)
direction = enum.Enum('up', 'down', 'sideways')

class Command:
    """
    A Command is an object consisting of a start_floor
    and a list of Transition instances
    """

    def __init__(self, start_floor, transitions):
        self.start_floor = start_floor
        self.transitions = transitions

    def __str__(self):
        # return "Command, \n\tstart_floor = {0}\n\ttransitions = {1}".format(
        #     self.start_floor, self.transitions)
        return "Command, \n\tstart_floor = {0}\n\ttransitions = {1}".format(
            self.start_floor, [ t.__str__() for t in self.transitions])

class Transition:
    """
    A transition is an object consisting of an origin floor
    and destination floor
    """

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    @property
    def direction(self):
        if self.origin > self.destination:
            return direction.down
        if self.origin < self.destination:
            return direction.up
        return direction.sideways

    def __str__(self):
        return "Transition {0} -> {1}".format(self.origin, self.destination)

class Path:
    """A Path is an object representing the list of floors to go to and the
    distance traveled."""

    def __init__(self):
        self.floors = []
        self.distance = 0

    def __str__(self):
        return "{0} ({1})".format(
            " ".join([str(f) for f in self.floors]),
            self.distance)


def parse_command_string(s):
    """
    Given a COMMAND_STRING, return a 2-tuple of START_FLOOR and
    list of ORIGINS_AND_DESTINATIONS, where ORIGINS_AND_DESTINATIONS
    is a namedtuple of origin and destination.
    """
    start_floor, origins_and_destinations = s.split(':')
    start_floor = int(start_floor)

    command = Command(start_floor, [])

    for o_d in origins_and_destinations.split(','):
        o,d = [ int(i) for i in o_d.split('-') ]
        logging.debug("{0}:{1}->{2}".format(start_floor, o,d))
        command.transitions.append(Transition(o,d))

    return command


def commands(filename):
    """
    Given a FILENAME, open the file and return each line as a command.
    """
    f = file(filename).read()

    for command_string in f.split('\n'):
        logging.debug(command_string)
        yield parse_command_string(command_string)


def process(command):
    """
    Given a COMMAND, return a Path instance calculatived naively.
    """

    p = Path()

    last_floor = command.start_floor
    p.floors.append(last_floor)
    for transition in command.transitions:
        p.distance += abs(last_floor - transition.origin)
        p.distance += abs(transition.origin - transition.destination)
        p.floors.append(transition.origin)
        p.floors.append(transition.destination)
        last_floor = transition.destination

    return p

# http://stackoverflow.com/questions/5738901/removing-elements-that-have-consecutive-dupes
def remove_consecutive_duplicates(i):
    return [x[0] for x in itertools.groupby(i)]

def get_next(i):
    try:
        return i.next()
    except StopIteration:
        return None

def merge_destination(c, n):

    if c.direction == direction.down:
        return c.destination if c.destination > n.destination else n.destination

    if c.direction == direction.up:
        return c.destination if c.destination < n.destination else n.destination

    elif origin > destination:
        return direction.down
    elif origin > destination:
        return direction.up

def sort_floors(_direction, floors):
    if _direction == direction.down:
        return sorted(floors, reverse=True)
    return sorted(floors)


def compress_transitions(command):
    """
    Given a list of TRANSITIONS, return an optimized list of TRANSITIONS.
    """

    starting_floor_transition = Transition(
        command.start_floor,
        command.transitions[0].origin)

    grouped_transitions = itertools.groupby(
        [starting_floor_transition] + command.transitions,
        lambda x: x.direction)

    logging.debug(grouped_transitions)

    master_path = Path()

    for _direction, group in grouped_transitions:
        floors = set()
        for g in group:
            floors.add(g.origin)
            floors.add(g.destination)
        master_path.floors.append(sort_floors(_direction, floors))

    master_path = remove_consecutive_duplicates(
        itertools.chain.from_iterable(master_path.floors))

    return list(master_path)



def optimal_process(command):

    path = compress_transitions(command)

    logging.debug(path)

    distance = reduce(
        lambda x, y: abs(x-y),
        path)

    return Path(path, distance)

def main(input_file='input.dat', mode='naive'):
    """
    Given an INPUT_FILE return a concordance of it's data.
    """

    for i, command in enumerate(commands(input_file)):
        logging.debug(command)

        if mode == 'naive':
            print process(command)
        else:
            print optimal_process(command)


if __name__ == '__main__':

    argh.dispatch_command(main)
