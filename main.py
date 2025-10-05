import math
import os
from interpreter.interpreter import InterpreterHelper
import logging
import time
import re
import shutil
import numpy as np

def process_nodes_dynamic_robot_speed(input_file_, output_file_, total_layer_):
    trans = [280.66, 570.45, -93.18]
    z_lift = 0.010
    layer_sleep_time = 1.0
    ret_extrude_ini = 0.7
    pre_extrude_ini = 0.8
    extrusion_rate = 1.00

    Feed_rate = 55
    speed_ini = 0.004
    line_number = 0
    blend_radius = 0.000
    limit_speed = 0.0125

    with open(input_file_, 'r') as infile_, open(output_file_, 'w') as outfile_:
        pre_info = None
        for line_ in infile_:
            line_number += 1
            parts = line_.split()

            if len(parts) >= 8:
                *coords, nx, ny, nz = map(float, parts[:6])
                extrude_value, extrude_ori, _, printer, layer = map(float, parts[6:])
                extrude_value = extrude_value * extrusion_rate
            else:
                continue

            printer = int(printer)

            x, y, z = (coords[0] + trans[0]) / 1000, (coords[1] + trans[1]) / 1000, (coords[2] + trans[2]) / 1000
            rx, ry, rz = convert_n_to_r(nx, ny, nz)

            if pre_info:
                distance = calculate_euclidean_distance(*pre_info[:3], x, y, z) * 1000

                if distance > 2.0 or pre_info[9] != layer:
                    speed = 0.005
                    ret_extrude = ret_extrude_ini
                    pre_extrude = pre_extrude_ini

                    outfile_.write(f'socket_send_line("G1 E{-ret_extrude:.3f} F{1.5 * Feed_rate:.3f}", "socket_01")\n')
                    outfile_.write(f'sleep(1.0)\n')
                    outfile_.write(f'movep(p[{pre_info[0]:.6f}, {pre_info[1]:.6f}, {pre_info[2] + z_lift:.6f}, {pre_info[3]:.6f}, {pre_info[4]:.6f}, {pre_info[5]:.6f}],accel_mss,{2 * speed:.5f},{blend_radius})\n')
                    outfile_.write(f'movep(p[{x:.6f}, {y:.6f}, {z + z_lift:.6f}, {rx:.6f}, {ry:.6f}, {rz:.6f}],accel_mss,{2 * speed:.5f},{blend_radius})\n')
                    if pre_info[9] != layer:
                        remaining_layers = total_layer_ - layer
                        sleep_time = layer_sleep_time
                        outfile_.write(f'sleep({sleep_time})\n')
                        print(f'remaining layers: {remaining_layers} calculate compensation {sleep_time} s...')

                    if pre_info[9] != layer and pre_info[6] != printer:
                        outfile_.write(f'sleep(205.0)\n')
                        print('Tool change 205.0 s...')

                    outfile_.write(f'movep(p[{x:.6f}, {y:.6f}, {z:.6f}, {rx:.6f}, {ry:.6f}, {rz:.6f}],accel_mss,{2 * speed:.5f},{blend_radius})\n')
                    outfile_.write(f'socket_send_line("G1 E{pre_extrude:.3f} F{1.5 * Feed_rate:.3f}", "socket_01")\n')
                    outfile_.write(f'sleep(1.0)\n')

                    print('lifting')
                else:
                    if extrude_value <= 0.01:
                        speed = 0.004
                    else:
                        speed = 0.001 * distance * (Feed_rate / 60) / extrude_value  # 单位m/s

                    if speed > limit_speed:
                        print(f'speed {speed:.4f} too fast, reduce speed to {limit_speed}.')
                        speed = limit_speed
                    outfile_.write(f'socket_send_line("G1 E{extrude_value:.3f} F{Feed_rate:.3f}", "socket_01")\n')

            else:
                speed = speed_ini

            outfile_.write(f'movep(p[{x:.6f}, {y:.6f}, {z:.6f}, {rx:.6f}, {ry:.6f}, {rz:.6f}],accel_mss,{speed:.5f},{blend_radius})\n')

            pre_info = (x, y, z, rx, ry, rz, printer, Feed_rate, extrude_value, layer, nx, ny, nz)

    print(f'{output_file_} layer: {layer} ext_ori: {extrude_ori:.3f} ext: {extrude_value:.3f} speed: {speed:.5f}')

def filter_points_in_file(file_path, threshold=0.40):
    with open(file_path, 'r') as file_:
        lines = file_.readlines()

    filtered_lines = []

    for i, line in enumerate(lines):
        values = list(map(float, line.split()))

        if 0.001 < values[6] < 0.080:
            values[6] = 0.110
            values[7] = 0.110
            print(f'line {i} too low extrusion, adjust to 0.100')

        if 0.900 < values[6] < 100.00:
            values[6] = 0.250
            values[7] = 0.250
            print(f'line {i} too high extrusion, adjust to 0.250')

        modified_line = f"{values[0]:.3f}\t{values[1]:.3f}\t{values[2]:.3f}\t{values[3]:.3f}\t{values[4]:.3f}\t{values[5]:.3f}" \
                        f"\t{values[6]:.3f}\t{values[7]:.3f}\t{values[8]:.3f}\t{int(values[9])}\t{int(values[10])}\n"

        if i == 0:
            filtered_lines.append(modified_line)
        else:
            prev_values = list(map(float, filtered_lines[-1].split()))
            x1, y1, z1 = values[:3]
            x2, y2, z2 = prev_values[:3]

            distance = calculate_euclidean_distance(x1, y1, z1, x2, y2, z2)

            if distance >= threshold:
                filtered_lines.append(modified_line)
            else:
                print(f'line {i} too close point, delete the latter')

    with open(file_path, 'w') as file_:
        file_.writelines(filtered_lines)

    with open('data/0.txt', 'w') as file_:
        file_.writelines(filtered_lines)

    print(f"Filtered data has been saved to  {file_path} and data/0.txt")

def rotate_around_z(x, y, z, nx, ny, nz, angle):
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])

    coordinates = np.array([x, y, z])
    rotated_coordinates = np.dot(rotation_matrix, coordinates)

    normal = np.array([nx, ny, nz])
    rotated_normal = np.dot(rotation_matrix, normal)

    return rotated_coordinates, rotated_normal

def rotation_process(merged_file_path_):
    with open(merged_file_path_, 'r') as file_:
        lines = file_.readlines()

    rotated_data = []
    for line in lines:
        values = list(map(float, line.split()))

        x, y, z = values[:3]
        nx, ny, nz = values[3:6]

        rotated_coordinates, rotated_normal = rotate_around_z(x, y, z, nx, ny, nz, np.pi / 6)

        new_values = (
            f"{rotated_coordinates[0]:.3f}\t{rotated_coordinates[1]:.3f}\t{rotated_coordinates[2]:.3f}\t"
            f"{rotated_normal[0]:.3f}\t{rotated_normal[1]:.3f}\t{rotated_normal[2]:.3f}\t"
            f"{values[6]:.3f}\t{values[7]:.3f}\t{values[8]:.3f}\t"
            f"{int(values[9])}\t{int(values[10])}\n"
        )
        rotated_data.append(new_values)

    with open(merged_file_path_, 'w') as file_:
        file_.writelines(rotated_data)

    with open('data/0.txt', 'w') as file_:
        file_.writelines(rotated_data)

    print(f"Rotated data saved to {merged_file_path_} and data/0.txt")

def calculate_euclidean_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

def convert_n_to_r(nx, ny, nz):
    rx = -math.degrees(math.asin(ny / math.sqrt(ny ** 2 + nz ** 2)))
    rx = rx * math.pi / 180
    ry = math.degrees(math.asin(nx / math.sqrt(nx ** 2 + ny ** 2 + nz ** 2)))
    ry = ry * math.pi / 180
    rz = 0
    rz = rz * math.pi / 180

    if abs(rx) < 1e-6:
        rx = 0.000000
    if abs(ry) < 1e-6:
        ry = 0.000000
    if abs(rz) < 1e-6:
        rz = 0.000000

    return rx, ry, rz

def process_last_line(merged_file_path_):
    with open(merged_file_path_, 'r') as file:
        lines = file.readlines()

    last_line = lines[-1].strip()
    elements = last_line.split()

    if not elements or len(elements) < 3:
        if len(lines) < 2:
            raise ValueError("no content")
        last_line = lines[-2].strip()
        elements = last_line.split()

    try:
        elements[2] = str(float(elements[2]) + 30)
    except (ValueError, IndexError):
        raise ValueError("wrong file format")

    new_line = '\t'.join(elements)
    original_line_count = len(lines)
    new_file_name = f'output/merge_lines_{original_line_count}_to_{original_line_count + 1}.txt'
    os.makedirs(os.path.dirname(new_file_name), exist_ok=True)
    with open(new_file_name, 'w') as new_file:
        new_file.write(last_line + '\n' + new_line)

    return new_file_name

def send_cmd_interpreter_mode_file(intrp, command_file):
    CLEARBUFFER_LIMIT = int(line_per_file + line_per_file * 0.4)

    f = open(command_file, "r")
    command_count = 1
    lines = f.readlines()
    for line_ in lines:
        command_id = intrp.execute_command(line_)
        if command_count % CLEARBUFFER_LIMIT == 0:
            while intrp.get_last_executed_id() != command_id:
                time.sleep(0.0001)

            intrp.clear()
        command_count += 1


def merge_layers(input_folder_, output_folder_, start_layer_, end_layer_):
    output_file_name = 'merge.txt'
    merged_file_path_ = os.path.join(output_folder_, output_file_name)
    files = [f for f in os.listdir(input_folder_) if f.endswith('.txt')]
    files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()))
    selected_files = [f for f in files if start_layer_ <= int(re.search(r'(\d+)', f).group()) <= end_layer_]

    with open(merged_file_path_, 'w') as outfile:
        for i, file_name in enumerate(selected_files):
            with open(os.path.join(input_folder_, file_name), 'r') as infile:
                for line in infile:
                    if line.strip():
                        outfile.write(line)

    for file_name in files:
        os.remove(os.path.join(input_folder_, file_name))
    shutil.copy(merged_file_path_, os.path.join('data', '0.txt'))

    return merged_file_path_

def process_output_file_name(merged_file_path_):
    base_name = os.path.basename(merged_file_path_)
    output_file_name = 'ur_' + base_name
    return os.path.join(os.path.dirname(merged_file_path_), output_file_name)


def split_file_into_chunks(file_path, lines_per_file=300):
    part_no = 1
    line_offset = 0

    while True:
        with open(file_path, 'r') as file:
            skip_lines = (part_no - 1) * lines_per_file - line_offset
            for _ in range(skip_lines):
                next(file, None)

            lines_to_read = lines_per_file + (1 if part_no > 1 else 0)
            lines = [next(file, None) for _ in range(lines_to_read)]
            lines = [line for line in lines if line is not None]

            if not lines:
                break

            base_name, ext = os.path.splitext(file_path)
            end_line_no = skip_lines + len(lines)
            chunk_file_path = f"{base_name}_lines_{skip_lines+1}_to_{end_line_no}{ext}"

            with open(chunk_file_path, 'w') as chunk_file_:
                chunk_file_.writelines(lines)

            yield chunk_file_path

            part_no += 1
            line_offset = 1

def clear_directory(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def sum_extrusion(file_path):
    total_sum = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                columns = line.split()
                if len(columns) >= 7:
                    total_sum += float(columns[6])
    except FileNotFoundError:
        print(f"File {file_path} not found.")

    print(f"The sum of the sixth column is: {total_sum}")

def send_cmd_to_robot(command_file, robot_ip):

    interpreter = InterpreterHelper(robot_ip)
    interpreter.connect()
    send_cmd_interpreter_mode_file(interpreter, command_file)


if __name__ == "__main__":
    logging.basicConfig(filename='ur5e.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    ROBOT_IP = "192.168.4.3"
    start_layer = 0
    end_layer = 100

    extend_mode = False
    final_lift = True
    rotate = False
    line_per_file = 8

    input_folder = 'data'
    output_folder = 'output'

    start_time = time.time()

    if not extend_mode:
        clear_directory(output_folder)
        merged_file_path = merge_layers(input_folder, output_folder, start_layer, end_layer)

    else:
        merged_file_path = 'output/merge.txt'

    filter_points_in_file(merged_file_path, threshold=0.40)

    if rotate:
        rotation_process(merged_file_path)

    with open(merged_file_path, 'r') as file:
        total_layer = int(file.readlines()[-1].strip().split()[-1])

    for chunk_file in split_file_into_chunks(merged_file_path, lines_per_file=line_per_file):
        chunk_output_file_path = process_output_file_name(chunk_file)
        process_nodes_dynamic_robot_speed(chunk_file, chunk_output_file_path, total_layer)
        send_cmd_to_robot(chunk_output_file_path, ROBOT_IP)

    if final_lift:
        lift_file = process_last_line(merged_file_path)
        lift_output_file_path = process_output_file_name(lift_file)
        process_nodes_dynamic_robot_speed(lift_file, lift_output_file_path, total_layer)
        send_cmd_to_robot(lift_output_file_path, ROBOT_IP)

    end_time = time.time()
    execution_time = end_time - start_time
    execution_time = execution_time / 60
    sum_extrusion('output/merge.txt')
    print(f'Finish printing the model. Time: {execution_time:.3f}')
