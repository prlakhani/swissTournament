#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

testTourn = addTournament()

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


# changed to account for tournaments
def testStandingsBeforeMatches(testTournament):
    deleteMatches()
    deletePlayers()
    p1 = registerPlayer("Melpomene Murray")
    p2 = registerPlayer("Randy Schwartz")
    registerPlayerInTournament(p1, testTournament)
    registerPlayerInTournament(p2, testTournament)

    standings = playerStandings(testTournament)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


# changed to account for tournaments and potential ties.
def testReportMatches(testTournament):
    deleteMatches()
    deletePlayers()
    p1 = registerPlayer("Bruno Walton")
    p2 = registerPlayer("Boots O'Neal")
    p3 = registerPlayer("Cathy Burton")
    p4 = registerPlayer("Diane Grant")
    registerPlayerInTournament(p1, testTournament)
    registerPlayerInTournament(p2, testTournament)
    registerPlayerInTournament(p3, testTournament)
    registerPlayerInTournament(p4, testTournament)

    standings = playerStandings(testTournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    # do we need to use playerStandings here, since we already have p_ ids?

    # report that id1 beat id2
    reportMatch(testTournament, id1, id1, id2)

    # report that id3 beat id4
    reportMatch(testTournament, id3, id3, id4)

    # check that standings were updated correctly
    standings = playerStandings(testTournament)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 3:
            # changed to reflect points instead of # wins.
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


# changed to account for tournaments and potential ties
def testPairings(testTournament):
    deleteMatches()
    deletePlayers()
    p1 = registerPlayer("Twilight Sparkle")
    p2 = registerPlayer("Fluttershy")
    p3 = registerPlayer("Applejack")
    p4 = registerPlayer("Pinkie Pie")
    registerPlayerInTournament(p1, testTournament)
    registerPlayerInTournament(p2, testTournament)
    registerPlayerInTournament(p3, testTournament)
    registerPlayerInTournament(p4, testTournament)
    
    standings = playerStandings(testTournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    
    # report that id1 beat id2
    reportMatch(testTournament, id1, id1, id2)

    # report that id3 beat id4
    reportMatch(testTournament, id3, id3, id4)
    
    pairings = swissPairings(testTournament)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


# New
def testDeleteTournaments(testTournament):
    deleteTournaments()
    try:
        checkTournament(testTournament)
    except AssertionError:
        print "9. Deleting all tournaments works."


# TODO: pick some additional tournament unit tests to add.
# test add tournament
# test check tournament
# test delete specific tournament


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches(testTourn)
    testReportMatches(testTourn)
    testPairings(testTourn)
    # Added tests.
    testDeleteTournaments(testTourn)
    print "Success!  All tests pass!"


