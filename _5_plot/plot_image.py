# -*- coding:utf-8 -*-
r"""
    plot the packet's payload to image

"""

import errno

from _3_pcap_parser.pcap2sessions_scapy import *


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def save_payload_to_image(payload_1d, image_width=28, output_name='demo.png'):
    if len(payload_1d) < image_width * image_width:
        print(payload_1d)
        payload_1d += b'\x00' * (image_width * image_width - len(payload_1d))
    if len(payload_1d) > image_width * image_width:
        payload_1d = payload_1d[:image_width * image_width]
    hexst = binascii.hexlify(payload_1d)
    payload_1d = numpy.array([int(hexst[i:i + 2], 16) for i in range(0, len(hexst), 2)])

    rn = len(payload_1d) // image_width
    fh = numpy.reshape(payload_1d[:rn * image_width], (-1, image_width))
    fh = numpy.uint8(fh)

    im = Image.fromarray(fh)
    im.save(output_name)

    return output_name


def getMatrixfrom_pcap(filename, width):
    with open(filename, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i + 2], 16) for i in range(0, len(hexst), 2)])
    rn = len(fh) // width
    fh = numpy.reshape(fh[:rn * width], (-1, width))
    fh = numpy.uint8(fh)
    return fh


def process_pcap(input_file='.pcap', image_width=28, output_dir='./data'):
    all_stats_dict, sess_dict = pcap2sessions_statistic_with_pcapreader_scapy_improved(input_file)
    print(f"all_stats_dict:{all_stats_dict}")
    # print(f"sess_dict:{sess_dict}")   # there will be huge information, please do print it out.

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, (k, v) in enumerate(sess_dict.items()):
        line_bytes = b''
        for pkt in v:  # pkt is IP pakcet, no ethernet header
            line_bytes += pkt.payload.payload.original
        # payload_1d = list(map(lambda x:int(x,16), line_str.split('\\x')))  # change hex to decimal
        output_name = os.path.join(output_dir, k + f'-({len(line_bytes)//image_width}x{image_width}).png')
        print(f"idx={idx}, output_name:{output_name}")
        # print(f"len(line_bytes)={len(line_bytes)}, ((height,width)={len(line_bytes)//image_width}x{image_width}), {line_bytes}")
        save_payload_to_image(line_bytes, image_width=image_width, output_name=output_name)

if __name__ == '__main__':
    input_file = '../1_pcaps_data/aim_chat_3a.pcap'
    # pcap2sessions_statistic_with_pcapreader_scapy_improved(input_file)
    process_pcap(input_file, output_dir='../data/aim_chat_3a')