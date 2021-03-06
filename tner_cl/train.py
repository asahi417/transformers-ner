""" Fine-tune transformers on NER dataset """
import argparse
import logging
from tner import VALID_DATASET
from tner import TrainTransformersNER


def get_options():
    parser = argparse.ArgumentParser(description='Fine-tune transformers on NER dataset')
    parser.add_argument('-c', '--checkpoint_dir', help='checkpoint directory', default='./ckpt_0/ner_model', type=str)
    parser.add_argument('-d', '--data', help='dataset: {}'.format(VALID_DATASET), default='wnut2017', type=str)
    parser.add_argument('-t', '--transformer', help='pretrained language model', default='xlm-roberta-large', type=str)
    parser.add_argument('-b', '--batch-size', help='batch size', default=32, type=int)
    parser.add_argument("--max-grad-norm", default=1.0, type=float, help="Max gradient norm.")
    parser.add_argument('--max-seq-length', default=128, type=int,
                        help='max sequence length (use same length as used in pre-training if not provided)')
    parser.add_argument('--random-seed', help='random seed', default=1234, type=int)
    parser.add_argument('--lr', help='learning rate', default=1e-5, type=float)
    parser.add_argument('--total-step', help='total training step', default=5000, type=int)
    parser.add_argument('--warmup-step', help='warmup step (6 percent of total is recommended)', default=700, type=int)
    parser.add_argument('--weight-decay', help='weight decay', default=1e-7, type=float)
    parser.add_argument('--fp16', help='fp16', action='store_true')
    parser.add_argument('--monitor-validation', help='display validation after each epoch', action='store_true')
    parser.add_argument('--lower-case', help='lower case all the data', action='store_true')
    parser.add_argument('--debug', help='show debug log', action='store_true')
    return parser.parse_args()


def main():
    opt = get_options()
    level = logging.DEBUG if opt.debug else logging.INFO
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=level, datefmt='%Y-%m-%d %H:%M:%S')
    # train model
    trainer = TrainTransformersNER(
        checkpoint_dir=opt.checkpoint_dir,
        dataset=opt.data.split(','),
        transformers_model=opt.transformer,
        random_seed=opt.random_seed,
        lr=opt.lr,
        total_step=opt.total_step,
        warmup_step=opt.warmup_step,
        weight_decay=opt.weight_decay,
        batch_size=opt.batch_size,
        max_seq_length=opt.max_seq_length,
        fp16=opt.fp16,
        max_grad_norm=opt.max_grad_norm,
        lower_case=opt.lower_case
    )
    trainer.train(monitor_validation=opt.monitor_validation)


if __name__ == '__main__':
    main()
