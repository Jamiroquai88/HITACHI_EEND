#!/usr/bin/env python3
#
# Copyright 2019 Hitachi, Ltd. (author: Yusuke Fujita)
# Licensed under the MIT license.
#

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

import yamlargparse
from eend import system_info

parser = yamlargparse.ArgumentParser(description='decoding')
parser.add_argument('-c', '--config', help='config file path',
                    action=yamlargparse.ActionConfigFile)
parser.add_argument('data_dir',
                    help='kaldi-style data dir')
parser.add_argument('model_file',
                    help='best.nnet')
parser.add_argument('out_dir',
                    help='output directory.')
parser.add_argument('--backend', default='chainer',
                    choices=['chainer', 'pytorch'],
                    help='backend framework')
parser.add_argument('--model_type', default='LSTM', type=str)
parser.add_argument('--gpu', type=int, default=-1)
parser.add_argument('--num-speakers', type=int, default=4)
parser.add_argument('--hidden-size', default=256, type=int,
                    help='number of lstm output nodes')
parser.add_argument('--num-lstm-layers', default=1, type=int,
                    help='number of lstm layers')
parser.add_argument('--input-transform', default='',
                    choices=['', 'log', 'logmel',
                             'logmel23', 'logmel23_swn', 'logmel23_mn'],
                    help='input transform')
parser.add_argument('--embedding-size', default=256, type=int)
parser.add_argument('--embedding-layers', default=2, type=int)
parser.add_argument('--chunk-size', default=2000, type=int,
                    help='input is chunked with this size')
parser.add_argument('--context-size', default=0, type=int,
                    help='frame splicing')
parser.add_argument('--subsampling', default=1, type=int)
parser.add_argument('--sampling-rate', default=16000, type=int,
                    help='sampling rate')
parser.add_argument('--frame-size', default=1024, type=int,
                    help='frame size')
parser.add_argument('--frame-shift', default=256, type=int,
                    help='frame shift')
parser.add_argument('--transformer-encoder-n-heads', default=4, type=int)
parser.add_argument('--transformer-encoder-n-layers', default=2, type=int)
parser.add_argument('--save-attention-weight', default=0, type=int)

attractor_args = parser.add_argument_group('attractor')
attractor_args.add_argument('--use-attractor', action='store_true',
                            help='Enable encoder-decoder attractor mode')
attractor_args.add_argument('--shuffle', action='store_true',
                            help='Shuffle the order in time-axis before input to the network')
attractor_args.add_argument('--attractor-loss-ratio', default=1.0, type=float,
                            help='weighting parameter')
attractor_args.add_argument('--attractor-encoder-dropout', default=0.1, type=float)
attractor_args.add_argument('--attractor-decoder-dropout', default=0.1, type=float)
attractor_args.add_argument('--attractor-threshold', default=0.5, type=float)
args = parser.parse_args()

system_info.print_system_info()
print(args)
if args.backend == 'chainer':
    from eend.chainer_backend.infer import infer
    infer(args)
elif args.backend == 'pytorch':
    # TODO
    # from eend.pytorch_backend.infer import infer
    # infer(args)
    raise NotImplementedError()
else:
    raise ValueError()
