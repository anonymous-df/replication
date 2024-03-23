# coding=utf-8
"""PyTorch RoBERTa model for DockerFill."""

import math
from typing import List, Optional, Tuple, Union

import torch
import torch.utils.checkpoint
from torch import nn
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss

from transformers.utils import (
    add_code_sample_docstrings,
    add_start_docstrings,
    add_start_docstrings_to_model_forward,
    logging,
    replace_return_docstrings,
)

from transformers.models.roberta.modeling_roberta import (
    RobertaPreTrainedModel,
    ROBERTA_INPUTS_DOCSTRING,
    MaskedLMOutput,
    _CHECKPOINT_FOR_DOC,
    _CONFIG_FOR_DOC,
    RobertaModel,
    RobertaLMHead,
)


class RobertaForMaskedLM(RobertaPreTrainedModel):
    _tied_weights_keys = ["lm_head.decoder.weight", "lm_head.decoder.bias"]

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = {'MLM': 50000, 'TTI': 4, 'MIP': 18}
        self.roberta = RobertaModel(config, add_pooling_layer=False)
        # MLM
        self.mlm_head = RobertaLMHead(config)

        # TTI
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.tti_head = nn.Linear(config.hidden_size, 4)

        # MIP
        self.mip_head = nn.Linear(config.hidden_size, 18)

        # Initialize weights and apply final processing
        self.post_init()

    def get_output_embeddings(self):
        return self.mlm_head.decoder

    def set_output_embeddings(self, new_embeddings):
        self.mlm_head.decoder = new_embeddings

    @add_start_docstrings_to_model_forward(ROBERTA_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @add_code_sample_docstrings(
        checkpoint=_CHECKPOINT_FOR_DOC,
        output_type=MaskedLMOutput,
        config_class=_CONFIG_FOR_DOC,
        mask="<mask>",
        expected_output="' Paris'",
        expected_loss=0.1,
    )
    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        token_type_ids: Optional[torch.LongTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        encoder_hidden_states: Optional[torch.FloatTensor] = None,
        encoder_attention_mask: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        task_name = None,
    ) -> Union[Tuple[torch.Tensor], MaskedLMOutput]:
        r"""
        labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
            Labels for computing the masked language modeling loss. Indices should be in `[-100, 0, ...,
            config.vocab_size]` (see `input_ids` docstring) Tokens with indices set to `-100` are ignored (masked), the
            loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`
        kwargs (`Dict[str, any]`, optional, defaults to *{}*):
            Used to hide legacy arguments that have been deprecated.
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        outputs = self.roberta(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_attention_mask,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        #print(task_name)
        sequence_output = outputs[0]
        #print(sequence_output)
        if task_name == "MLM": # MLM
            prediction_scores = self.mlm_head(sequence_output)
        elif task_name == "TTI": # TTI
            hidden_states = self.dropout(sequence_output)
            prediction_scores = self.tti_head(hidden_states)
        elif task_name == "MIP": # MIP
            hidden_states = self.dropout(sequence_output)
            prediction_scores = self.mip_head(hidden_states)


        lm_loss = None
        if labels is not None:
            # move labels to correct device to enable model parallelism
            labels = labels.to(prediction_scores.device)
            loss_fct = CrossEntropyLoss()
            #print(len(prediction_scores[0]))
            #print(len(labels[0]))
            lm_loss = loss_fct(prediction_scores.view(-1, self.num_labels[task_name]), labels.view(-1))

        if not return_dict:
            output = (prediction_scores,) + outputs[2:]
            return ((lm_loss,) + output) if lm_loss is not None else output

        return MaskedLMOutput(
            loss=lm_loss,
            logits=prediction_scores,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )
