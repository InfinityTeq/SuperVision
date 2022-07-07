#!/usr/bin/env python
# map buses
# created by : C0SM0

buses = open('buses.txt', 'r').readlines()
alphabet = 'abcdefghijklmnopqrstuvwxyz'
output = []

for bus, route in zip(buses[::2], buses[1::2]):
    bus = bus[1:-3].lower()
    route = route[1:-2]

    # print(bus[len(bus)-1])

    if bus[len(bus)-1] in alphabet:
        
        continue


    xml_dict = f"'bus-chicago-{bus}.xml':'http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route={bus}',"
    output.append(xml_dict)

    print(xml_dict) 