def get():
    # add realtime visualization to html

    realtime = open('templates/realtime.js', 'r').read()
    read_index = open('templates/index.html', 'r').readlines()
    map_name = ''
    with open('templates/index.html', 'w') as index:
        for line in range(len(read_index) - 1):
            if read_index[line].strip().endswith('L.map('):
                map_name = read_index[line].strip(' ').replace('\t', '').replace('var ','').replace(' = L.map(','').replace('\n','')
                print(map_name)
                print()

            index.write(read_index[line])
        index.write(realtime.replace('MAP',map_name))