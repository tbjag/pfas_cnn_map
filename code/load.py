import numpy as np
import argparse
import os

class ProcessData:
    def __init__(self, input_folder, interval) -> None:
        self.input_folder = input_folder
        self.interval = interval

    def load(self):
        arrays = []
        cnt = 0
        while True:
            cnt += self.interval
            filename = os.path.join(self.input_folder, f"generate_{cnt}.npy")
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    fi = np.load(f, allow_pickle=True)
                    arrays.append(fi)
            else:
                break
            
        if arrays:
            return np.concatenate(arrays)
        else:
            return None
        
        


def main():
    parser = argparse.ArgumentParser('process map data')
    parser.add_argument('-length', type=int, default=7)
    parser.add_argument('-grain', type=float, default=0.1)
    parser.add_argument('-input', type=str, default='data')
    parser.add_argument('-output', type=str, default='data/generate')
    parser.add_argument('-interval', type=int, default=100)
    parser.add_argument('-checkpoint', type=int, default=0)
    
    args = parser.parse_args()
    print(args)
    # TODO check length is odd

    # with open('data/generate_10.npy', 'rb') as f:
    #     h = np.load(f, allow_pickle=True)
    #     print(h.shape)

    x = ProcessData(args.input, args.interval)
    data = x.load()


    print(data[700])



if __name__ == '__main__':
    main()
    