#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        hvqm
# Author:      Zoinkity
#
# Created:     08/05/2015
# Copyright:   (c) Zoinkity 2015
# Licence:     <unlicenced>
#-------------------------------------------------------------------------------

class HVQM2:
    def __init__(self, header, records):
        self.records = records
        if isinstance(header[0], str):
            self.version = header[0]
        else:
            self.version = header[0].decode().strip('\x00')
        # Don't save filesize; recalc using method.
        self.horz = header[1]
        self.vert = header[2]
        self.hdiff= header[3]
        self.vdiff= header[4]
        self.enc1 = header[5]
        self.enc2 = header[6]
        self.vrec_num = header[7]
        self.framerate = header[8]
        self.vrec_max = header[9]
        self.req_packets = header[10]
        self.audio = header[11]
        self.channels = header[12]
        self.bitwidth = header[13]
        self.enc3 = header[14]
        self.arec_num = header[15]
        self.samplerate = header[16]
        self.arec_max = header[17]

    @classmethod
    def frombytes(cls, data, offset=0):
        import struct
        header = struct.unpack_from(">16s4xHH4B4L4B3L", data, offset)
        return cls(header, data[offset+60:])

    def filesize(self):
        return len(self.records) + 60

    def tobytes(self):
        return self.__bytes__()

    def __bytes__(self):
        import struct
        a = [self.version.encode(), self.filesize(), self.horz, self.vert,
             self.hdiff, self.vdiff, self.enc1, self.enc2, self.vrec_num,
             self.framerate, self.vrec_max, self.req_packets, self.audio,
             self.channels, self.bitwidth, self.enc3, self.arec_num,
             self.samplerate, self.arec_max]
        header = struct.pack(">16sLHH4B4L4B3L", *a)
        return b''.join((header, self.records))

def merge(file1, file2):
    """Returns True if fixed fields from header appear to match."""
    if file1.version != file2.version:
        print("File version mismatch.")
    elif file1.horz != file2.horz:
        print("Width mismatch.")
    elif file1.vert != file2.vert:
        print("Height mismatch.")
    elif file1.hdiff != file2.hdiff:
        print("Horizontal sampling rate mismatch.")
    elif file1.vdiff != file2.vdiff:
        print("Vertical sampling rate mismatch.")
    elif file1.enc1 != file2.enc1:
        print("Unknown encoding parameter 1 mismatch.")
    elif file1.enc2 != file2.enc2:
        print("Unknown encoding parameter 2 mismatch.")
    elif file1.framerate != file2.framerate:
        print("Frame interval mismatch.")
    elif file1.audio != file2.audio:
        print("Audio format mismatch.")
    elif file1.channels != file2.channels:
        print("Different number of audio channels.")
    elif file1.bitwidth != file2.bitwidth:
        print("Audio sample size mismatch.")
    elif file1.enc3 != file2.enc3:
        print("Unknown encoding parameter 3 mismatch.")
    elif file1.samplerate != file2.samplerate:
        print("Audio sample rate mismatch.")
    else:
        # They match enough, so merge!
        h = [file1.version, file1.horz, file1.vert, file1.hdiff, file1.vdiff, file1.enc1, file1.enc2]
        h.append(file1.vrec_num + file2.vrec_num)
        h.append(file1.framerate)
        h.append(max(file1.vrec_max, file2.vrec_max))
        h.append(max(file1.req_packets, file2.req_packets))
        h.extend([file1.audio, file1.channels, file1.bitwidth, file1.enc3])
        h.append(file1.arec_num + file2.arec_num)
        h.append(file1.samplerate)
        h.append(max(file1.arec_max, file2.arec_max))
        return HVQM2(h, b''.join((file1.records, file2.records)))
    return None

def main():
    with open(r"0.hvqm", 'rb') as f:
        file1 = HVQM2.frombytes(f.read())
    with open(r"1.hvqm", 'rb') as f:
        file2 = HVQM2.frombytes(f.read())
    result = merge(file1, file2)
    with open(r"2.hvqm", 'rb') as f:
        file2 = HVQM2.frombytes(f.read())
    result = merge(result, file2)
    with open(r"sample.hvqm", 'wb') as f:
        f.write(bytes(result))

if __name__ == '__main__':
    main()