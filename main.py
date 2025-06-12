import os, math, time
from Graph import Point
from draw_graph import main_draw

def get_data_from_file(file_name='euler.txt'):
    result = ''
    try:
        with open(os.getcwd() + "\\" + file_name) as f:
            result = f.read()
    except:
        pass
    return result


def convert_data(data):
    data_list = list(filter(lambda el: el == '0' or el == '1', list(data)))
    data_list = list(map(lambda el: bool(int(el)), list(data_list)))
    trans = []
    d_sqrt_len = int(math.sqrt(len(data_list)))
    for i in range(d_sqrt_len):
        trans.append(data_list[i*d_sqrt_len:i*d_sqrt_len + d_sqrt_len])
    data_list = trans
    points = []
    for i in range(len(data_list)):
        points.append(Point(data_list[i], str(i+1)))
    return points


def connect_points(points):
    for point in points:
        for i, connection in enumerate(point.connections):
            if connection:
                point.connections[i] = points[i]
        point.connections = list(filter(lambda a: type(a) == Point, point.connections))
    return points

def main():
    files = ['euler.txt', 'euler copy.txt']
    all_data = []
    for file in files:
        data = get_data_from_file(file)
        if data == '':
            print(f'[ERROR] DATA FILE {file} ERROR [ERROR]')
            continue
        all_data.append(connect_points(convert_data(data)))
    if len(all_data) > 0:
        main_draw(all_data)


if __name__ == '__main__':
    id = int(round(time.time(), 0))
    print(f'[INFO] MAIN WITH ID {id} --START-- [INFO]')
    main()
    print(f'[INFO] MAIN WITH ID {id} ---END--- [INFO]')