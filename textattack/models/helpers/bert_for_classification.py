import textattack.utils as utils
import torch

from textattack.tokenizers import BERTTokenizer, BERTEntailmentTokenizer
from transformers.modeling_bert import BertForSequenceClassification


class BERTForClassification:
    """ 
    BERT fine-tuned for sentiment classification. 

    Args:
        max_seq_length(:obj:`string`): Path to the pre-trained model.
        max_seq_length(:obj:`int`, optional):  Number of class labels for 
            prediction, if different than 2.
        max_seq_length(:obj:`int`, optional):  Maximum length of a sequence after tokenizing.
            Defaults to 32.
            
    """
    def __init__(self, model_path, num_labels=2, entailment=False):
        utils.download_if_needed(model_path)
        print('TextAttack BERTForClassification Loading from path', model_path)
        self.model = BertForSequenceClassification.from_pretrained(
            model_path, num_labels=num_labels)
        self.model.to(utils.get_device())
        self.model.eval()
        if entailment:
            # @TODO: Use custom tokenizer after we train our own models.
            self.tokenizer = BERTEntailmentTokenizer()
        else:
            self.tokenizer = BERTTokenizer(model_path)
    
    def __call__(self, *params):
        with torch.no_grad():
            pred = self.model(*params)[0]
        return torch.nn.functional.softmax(pred, dim=-1)
