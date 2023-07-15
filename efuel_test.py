import dataclasses
import json
import random
from datetime import datetime

import pytest

import efuel as efuel
from entry import Entry


def test_setup(monkeypatch, capsys, version):
    assert version in ['BASIS', 'ERWEITERT', 'UNBEKANNT']


def test_attributes(monkeypatch, capsys):
    start = datetime.strptime('26.02.2023 06:00', '%d.%m.%Y %H:%M')
    end = datetime.strptime('26.02.2023 08:30', '%d.%m.%Y %H:%M')
    release = datetime.strptime('26.02.2023 09:45', '%d.%m.%Y %H:%M')
    entry = Entry(start, end, release, 75.15)
    assert dataclasses.astuple(entry) == (start, end, release, 75.15)


def test_cost1(monkeypatch, capsys):
    start = datetime.strptime('23.01.2023 12:00', '%d.%m.%Y %H:%M')
    end = datetime.strptime('23.01.2023 12:30', '%d.%m.%Y %H:%M')
    release = datetime.strptime('23.01.2023 12:40', '%d.%m.%Y %H:%M')
    entry = Entry(start, end, release, 12)
    assert entry.cost == round((12 * 0.35), 2)


def test_cost2(monkeypatch, capsys):
    start = datetime.strptime('09.01.2023 12:00', '%d.%m.%Y %H:%M')
    end = datetime.strptime('09.01.2023 12:30', '%d.%m.%Y %H:%M')
    release = datetime.strptime('09.01.2023 13:15', '%d.%m.%Y %H:%M')
    entry = Entry(start, end, release, 27)
    assert entry.cost == round((27 * 0.35 + 30 * 0.05), 2)


def test_read_entry(monkeypatch, capsys):
    inputs = iter(['06.01.2023 08:07', '06.01.2023 09:45', '06.01.2023 10:00', 57.5])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    entry = efuel.read_entry()
    entry_tuple = dataclasses.astuple(entry)
    if isinstance(entry_tuple[0], str):
        assert entry == Entry('06.01.2023 08:07', '06.01.2023 09:45', '06.01.2023 10:00', 57.5)
    else:
        assert entry == Entry(
            datetime.strptime('06.01.2023 08:07', '%d.%m.%Y %H:%M'),
            datetime.strptime('06.01.2023 09:45', '%d.%m.%Y %H:%M'),
            datetime.strptime('06.01.2023 10:00', '%d.%m.%Y %H:%M'),
            57.5
        )


def test_init_accounts1(monkeypatch, capsys, version):
    print(f'Testen der Version {version}')
    if version == 'BASIS':
        assert efuel.init_accounts() == list()
    elif version == 'ERWEITERT':
        collection = efuel.init_accounts()
        assert 'Adam' in collection
    else:
        print('Test kann erst durchgeführt werden, wenn init_accounts() korrekt läuft')
        assert False


def test_init_accounts2(monkeypatch, capsys, version):
    print(f'Testen der Version {version}')
    if version == 'ERWEITERT':
        collection = efuel.init_accounts()
        assert collection['Adam'] == []
    else:
        print('Test kann nur mit der erweiterten Version von init_accounts() ausgeführt werden')
        assert False


def test_add_entries1(monkeypatch, capsys, version):
    print(f'Testen der Version {version}')
    collection = efuel.init_accounts()
    if version == 'BASIS':
        inputs = iter(['06.01.2023 08:07', '06.01.2023 09:45', '06.01.2023 10:00', 57.5, 'y'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        efuel.add_entries(collection)
        if collection[0] is None:
            assert collection == [None, None, None, None, None]
        else:
            assert isinstance(collection[0], Entry)
    elif version == 'ERWEITERT':
        inputs = iter(['Inga', '06.01.2023 08:07', '06.01.2023 09:45', '06.01.2023 10:00', 57.5, 'y'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        efuel.add_entries(collection)
        entry = collection['Inga'][0]
        assert isinstance(entry, Entry)
    else:
        print('Test kann erst durchgeführt werden, wenn init_accounts() korrekt läuft')
        assert False


def test_add_entries2(monkeypatch, capsys, version):
    if version == 'ERWEITERT':
        inputs = iter([
            'Inga', '06.01.2023 08:07', '06.01.2023 09:45', '06.01.2023 10:00', 57.5, 'n',
            'Adam', '10.01.2023 13:15', '10.01.2023 14:20', '10.01.2023 14:21', 13, 'n',
            'Inga', '12.01.2023 08:00', '12.01.2023 09:00', '12.01.2023 10:00', 57.5, 'y'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        collection = {'Inga': list(), 'Karl': list(), 'Adam': list()}
        efuel.add_entries(collection)
        assert isinstance(collection['Inga'][1], Entry)

    else:
        print('Test kann nur mit der erweiterten Version (dict) durchgeführt werden')
        assert False


def test_show_balance1(monkeypatch, capsys, version):
    if version == 'BASIS':
        entry1 = Entry(
            '12.03.2023 15:17',
            '12.03.2023 17:43',
            '12.03.2023 17:56',
            57.5
        )
        entry2 = Entry(
            '21.03.2023 08:04',
            '21.03.2023 09:53',
            '21.03.2023 10:05',
            31.35
        )
        cost0 = round((57.5 * 0.35),2)
        cost1 = round((31.35 * 0.35),2)
        output = '  {sign} 12.03.2023 15:17  CHF {amount0:.2f}\n' \
                 '  {sign} 21.03.2023 08:04  CHF {amount1:.2f}\n' \
                 '{total}: CHF {amount2:.2f}\n' \
            .format(
            sign='-',
            total='Total',
            amount0=cost0,
            amount1=cost1,
            amount2=(cost0 + cost1)
        )
        accounting = [entry1, entry2]
        efuel.show_balance(accounting)
        captured = capsys.readouterr()
        print(f'Testen der Version {version}')
        assert captured.out == output
    elif version == 'ERWEITERT':
        entry1 = Entry(
            datetime.strptime('12.03.2023 15:17', '%d.%m.%Y %H:%M'),
            datetime.strptime('12.03.2023 17:43', '%d.%m.%Y %H:%M'),
            datetime.strptime('12.03.2023 17:56', '%d.%m.%Y %H:%M'),
            57.5
        )
        entry2 = Entry(
            datetime.strptime('21.03.2023 08:04', '%d.%m.%Y %H:%M'),
            datetime.strptime('21.03.2023 09:53', '%d.%m.%Y %H:%M'),
            datetime.strptime('21.03.2023 10:05', '%d.%m.%Y %H:%M'),
            31.35
        )
        cost0 = round((57.5 * 0.35), 2)
        cost1 = round((31.35 * 0.35), 2)
        output = 'Abrechnung für {client}\n' \
                 '  {sign} 12.03.2023 15:17: CHF {amount0:.2f}\n' \
                 '  {sign} 21.03.2023 08:04: CHF {amount1:.2f}\n' \
                 '{total}: CHF {amount2:.2f}\n' \
            .format(
            client='Karl',
            sign='-',
            total='Total',
            amount0=cost0,
            amount1=cost1,
            amount2=(cost0 + cost1)
        )
        accounting = {'Karl': [entry1, entry2]}
        efuel.show_balance(accounting)
        captured = capsys.readouterr()
        print(f'Testen der Version {version}')
        assert captured.out == output
    else:
        print('Test kann erst durchgeführt werden, wenn init_accounts() korrekt läuft')
        assert False


def test_show_balance2(monkeypatch, capsys, version):
    if version == 'ERWEITERT':
        entry1 = Entry(
            datetime.strptime('12.03.2023 15:17', '%d.%m.%Y %H:%M'),
            datetime.strptime('12.03.2023 17:43', '%d.%m.%Y %H:%M'),
            datetime.strptime('12.03.2023 22:16', '%d.%m.%Y %H:%M'),
            57.5
        )
        entry2 = Entry(
            datetime.strptime('21.03.2023 08:04', '%d.%m.%Y %H:%M'),
            datetime.strptime('21.03.2023 09:53', '%d.%m.%Y %H:%M'),
            datetime.strptime('21.03.2023 10:05', '%d.%m.%Y %H:%M'),
            31.35
        )
        entry3 = Entry(
            datetime.strptime('12.03.2023 06:02', '%d.%m.%Y %H:%M'),
            datetime.strptime('12.03.2023 07:41', '%d.%m.%Y %H:%M'),
            datetime.strptime('12.03.2023 08:37', '%d.%m.%Y %H:%M'),
            61.75
        )
        cost0 = round((57.5 * 0.35 + 258 * 0.05), 2)
        cost1 = round((31.35 * 0.35), 2)
        cost2 = cost0 + cost1
        cost3 = round((61.75 * 0.35 + 41 * 0.05), 2)
        accounting = {
            'Inga': [entry1, entry2],
            'Karl': [entry3]
        }
        output = 'Abrechnung für {client1}\n' \
                 '  {sign} 12.03.2023 15:17: CHF {amount0:.2f}\n' \
                 '  {sign} 21.03.2023 08:04: CHF {amount1:.2f}\n' \
                 'Total: CHF {amount2:.2f}\n' \
                 'Abrechnung für {client2}\n' \
                 '  {sign} 12.03.2023 06:02: CHF {amount3:.2f}\n' \
                 '{total}: CHF {amount3:.2f}\n' \
            .format(
            sign='-',
            total='Total',
            client1='Inga',
            client2='Karl',
            amount0=cost0,
            amount1=cost1,
            amount2=cost2,
            amount3=cost3
        )
        try:
            efuel.show_balance(accounting)
            captured = capsys.readouterr()
            assert captured.out == output

        except:
            assert False
    else:
        print('Test kann nur mit der erweiterten Version von init_accounts() durchgeführt werden')
        assert False


def test_read_float1(monkeypatch, capsys):
    random_number = random.randint(50, 199) / 10
    inputs = iter([random_number])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    energy = efuel.read_float('')
    assert energy == random_number


def test_read_float2(monkeypatch, capsys):
    random_number = random.randint(150, 599) / 20
    inputs = iter([-4.2, 'a7', random_number])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    energy = efuel.read_float('')
    assert energy == random_number


def test_read_float3(monkeypatch, capsys):
    random_number = random.randint(150, 599) / 25
    inputs = iter([-4.2, 'a7', random_number])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    efuel.read_float('')
    captured = capsys.readouterr()
    assert captured.out == 'Geben Sie eine positive Zahl ein\nGeben Sie eine positive Zahl ein\n'


def test_read_datetime1(monkeypatch, capsys):
    inputs = iter(['05.01.2023 13:37'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    timestamp = efuel.read_datetime('')
    if isinstance(timestamp, str):
        assert timestamp == '05.01.2023 13:37'
    else:
        assert timestamp == datetime.strptime('05.01.2023 13:37', '%d.%m.%Y %H:%M')


def test_read_datetime2(monkeypatch, capsys):
    inputs = iter(['05.01.2023 1a:05', '06.01.2023 13:10'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    timestamp = efuel.read_datetime('')
    assert timestamp == datetime.strptime('06.01.2023 13:10', '%d.%m.%Y %H:%M')


def test_read_datetime3(monkeypatch, capsys):
    inputs = iter(['05.01.2023 1a:05', '06.01.2023 13:10'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    efuel.read_datetime('')
    captured = capsys.readouterr()
    assert captured.out == 'Geben Sie ein gültiges Datum/Uhrzeit ein\n'



@pytest.fixture
def version():
    collection = efuel.init_accounts()
    if collection is None:
        return 'UNBEKANNT'
    if isinstance(collection, list):
        return 'BASIS'
    if isinstance(collection, dict):
        return 'ERWEITERT'
    return 'UNBEKANNT'