from haystack.reader.farm import FARMReader
model = 'deepset/roberta-base-squad2'
# model = 'deepset/minilm-uncased-squad2'


def read():
    reader = FARMReader(model_name_or_path=model, progress_bar=False, use_gpu=False,
                        num_processes=4)

    return reader
