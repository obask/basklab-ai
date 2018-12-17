import JaipurState


def main():
    print("commands: exit, exchange for, camels, take, sell")
    state = JaipurState.init_state()
    # state.print()
    # print("//==============================")
    # print(state.deck)
    # print("//==============================")

    while True:
        state.print()
        repl = input().split()
        cmd = repl[0]
        if cmd == "exit":
            print("EXIT")
        elif cmd == "exchange":
            middle = repl.index("for")
            print("take", repl[1:middle])
            print("give", repl[middle+1:])
        elif cmd == "take":
            index = state.market.index(repl[1])
            print("take_1_single_good", index)
            state.take_1_single_good(index)
        elif cmd == "camels":
            print("take_the_camels")
            state.take_the_camels()
        elif cmd == "sell":
            index = state.hand.index(repl[1])
            print("sell", index)
            state.sell_cards(index)
        else:
            continue
        state = state.flip_sides()


if __name__ == "__main__":
    main()
