import numpy
import matplotlib.pyplot as plt
import pandas


class Deck:
    def __init__(self, cards) -> None:
        self.Cards = cards
    
    def add(self, cards):
        self.Cards.extend(cards)
    
    def try_get_card(self):
        if len(self.Cards) > 0:
            return True, self.Cards.pop(0)
        else:
            return False, None
    

class Game:
    def __init__(self, counter_limit:int = 100, shuffle:bool = True, ) -> None:
        self.Decks = self.init_decks(shuffle)
        self.ActiveDeckIndex = 0
        self.TableCards = []
        self.StealMode = False
        self.StealModeCounter = 0
        self.Counter = 0
        self.CounterLimit = counter_limit
        self.Stop = False

        # print("Deck1: {}".format(self.Decks[0].Cards))
        # print("Deck2: {}".format(self.Decks[1].Cards))
        # print("Table cards: {}".format(self.TableCards))
    
    def init_decks(self, shuffle ):
        if shuffle:
            numpy.random.shuffle(ALL_CARDS)
        # print("shuffled deck: {}".format(ALL_CARDS))
        half_length = int(len(ALL_CARDS)/2)
        return Deck(ALL_CARDS[:half_length]), Deck(ALL_CARDS[half_length:])
    
    def switch_player(self):
        self.ActiveDeckIndex = 1 - self.ActiveDeckIndex
    
    def next(self):
        active_deck = self.Decks[self.ActiveDeckIndex]
        ok, card = active_deck.try_get_card()
        if ok: 
            self.TableCards.append(card)
            if card in [1,2,3]:
                self.StealMode = True
                self.StealModeCounter = card
                self.switch_player()
            else:
                if self.StealMode == True: 
                    self.StealModeCounter -= 1
                    if self.StealModeCounter <= 0:
                        self.switch_player()
                        active_deck = self.Decks[self.ActiveDeckIndex]
                        active_deck.add(self.TableCards)
                        self.TableCards = []
                        self.StealMode = False
                else:
                    self.switch_player()

        if any([len(deck.Cards) == 0 for deck in self.Decks]): # if a deck ran out of cards the game must stop
            self.Stop = True


    def play(self) -> int:
        self.Counter = 0
        while True and self.Counter < self.CounterLimit:
            self.next()
            # print("STEP {}: ".format(self.Counter))
            # print("Deck1: {}".format(self.Decks[0].Cards))
            # print("Deck2: {}".format(self.Decks[1].Cards))
            # print("Table cards: {}".format(self.TableCards))
            # print("StealMode: {} --> StealModeCounter: {}".format(self.StealMode, self.StealModeCounter))
            self.Counter += 1
            if self.Stop:
                break
        
        return self.Counter


def run_test(n_trials = 10, counter_limit = 100, shuffle = True):
    results = []
    for i in range(n_trials):
        game = Game(counter_limit=counter_limit, shuffle = shuffle)
        count = game.play()
        results.append(count)
    return results


def plot(data):

    x = list(range(len(data)))
    y = data

    # definitions for the axes
    left, width = 0.1, 0.6
    bottom, height = 0.1, 0.8
    spacing = 0.05

    rect_scatter = [left, bottom, width, height]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8, 8))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    ax_histy = plt.axes(rect_histy)
    ax_histy.tick_params(direction='in', labelleft=False)

    # the scatter plot:
    ax_scatter.scatter(x, y)

    # now determine nice limits by hand:
    xlim = len(x)
    ylim = numpy.max(y)
    ax_scatter.set_xlim((0, xlim))
    ax_scatter.set_ylim((0, ylim))
    ax_scatter.set_xlabel('games')
    ax_scatter.set_ylabel('steps')

    binwidth = 5
    bins = numpy.arange(0, ylim + binwidth, binwidth)
    ax_histy.hist(y, bins=bins, orientation='horizontal', density=True, edgecolor='black')
    ax_histy.set_ylim(ax_scatter.get_ylim())
    ax_histy.set_xlabel('probability')

    plt.show()

def save(data):
    df = pandas.DataFrame({"Game": range(len(data)), "Count": data})
    df.to_excel('pelagallina_results.xlsx')


if __name__ == '__main__':

    ALL_CARDS = [0]*28 + [1]*4 + [2]*4 + [3]*4

    n_trials = 10000
    counter_limit = 1000

    results = run_test(n_trials=n_trials, counter_limit=counter_limit, shuffle=True)

    min = numpy.min(results)
    max = numpy.max(results)
    mean = numpy.mean(results)
    median = numpy.median(results)

    print(min)
    print(max)
    print(mean)
    print(median)

    plot(results)
    save(results)