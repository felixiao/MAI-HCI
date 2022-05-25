import os
from midi2audio import FluidSynth
from pypianoroll import Multitrack
import argparse

def parse_arguments():
    """Parse and return the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_name',
                        help="File name and directory to store the midi file")
    parser.add_argument('--in_name',
                        help="Directory that contains the npz file to transform")
    args = parser.parse_args()
    return args

def npz_to_mid(in_name, out_name):
    m = Multitrack(in_name)
    m.write(out_name)

def mid_to_wav(f_path):
    base_file = os.path.splitext(f_path)[0]
    f_midi = base_file + '.mid'
    f_wav = base_file + '.wav' 
    print(base_file)
    print(f_midi)
    print(f_wav)
    fs = FluidSynth()
    fs.midi_to_audio(f_midi, f_wav)
    #FluidSynth().midi_to_audio(f_midi, f_wav)
    return f_wav

if __name__ == "__main__":
    args = parse_arguments()
    print(args)
    npz_to_mid(args.in_name, args.out_name)
