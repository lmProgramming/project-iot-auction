#!/usr/bin/env python3

'''Zadanie 5: Uruchamianie skryptów języka Python z linii komend
Wykorzystując dowolny edytor tekstu, przygotuj prosty skrypt języka Python o nazwie myscript.py podejmujący interak-
cję z użytkownikiem poprzez konsolę. Skonfiguruj pierwszą linię wskazującą interpreter python3 i nadaj plikowi atrybuty
wykonywalności. Uruchom skrypt poleceniem
./myscript.py
'''


def main():
    name = input("What is your name? ")
    print(f"Hello, {name}!")


if __name__ == "__main__":
    main()
