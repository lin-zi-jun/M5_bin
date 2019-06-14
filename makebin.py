import os

# bootloader*.bin --> BOOTLOADER
# *.partitions.bin --> PARTITIONS
# boot_*.bin --> BOOTAPP
# *.ino.bin -->  APPLICATION

OFFSET_BOOTLOADER = 0x1000
OFFSET_PARTITIONS = 0x8000
OFFSET_BOOTAPP = 0xe000
OFFSET_APPLICATION = 0x10000

name_map = [
    ('bootloader', 0, OFFSET_BOOTLOADER),
    ('partitions.bin', 1, OFFSET_PARTITIONS),
    ('boot_', 2, OFFSET_BOOTAPP),
    ('ino.bin', 3, OFFSET_APPLICATION),
]

bootloader_path = os.getcwd().replace('/', '//') + '//app0_bootloader'

create_path = ['Module', 'Unit','Advanced','M5Core','Application','M5StickC']

def get_cover_list(path):
    file_list = os.listdir(path)
    cover_list = [[None, None]] * 4
    for fin in file_list:
        for i in name_map:
            if i[0] in fin:
                cover_list[i[1]] = [path + '//' + fin, i[2]]
                break
    
    if cover_list[0] == [None, None]:
        cover_list[0] = [bootloader_path + '//bootloader_qio_80m.bin', OFFSET_BOOTLOADER]
    if cover_list[2] == [None, None]:
        cover_list[2] = [bootloader_path + '//boot_app0.bin', OFFSET_BOOTAPP]
    return cover_list

def cover2firmware(path):
    cover_list = get_cover_list(path)
    if [None, None] in cover_list:
        return False
    
    cur_offset = OFFSET_BOOTLOADER

    with open(path + '//' + 'firmware_0x1000.bin', 'wb') as fout:
        for file_in, offset in cover_list:
            assert offset >= cur_offset
            fout.write(b'\xff' * (offset - cur_offset))
            cur_offset = offset
            with open(file_in, 'rb') as fin:
                data = fin.read()
                fout.write(data)
                cur_offset += len(data)
    return True

for path_total in create_path:
    fail_path = []
    for dirpath, dirnames, filenames in os.walk(path_total):
        if filenames != []:
            if cover2firmware(dirpath):
                print('finish -- {}'.format(dirpath))
            else:
                fail_path.append(dirpath)
    print(fail_path)