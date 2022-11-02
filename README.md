# Speaker-Embeddings
Implementation of [Generalized End-to-end Loss for Speaker Verification](https://arxiv.org/pdf/1710.10467.pdf) - GE2E loss, which yields speaker embeddings as results.

This is a mere small project to practice re-producing paper, if you want a repository that actually re-produce the paper, please refer to [Resemblyzer](https://github.com/resemble-ai/Resemblyzer) or the encoder module of [Voice Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning/tree/master/encoder).


### Posts of Reproducing ML papers
- https://towardsdatascience.com/converting-deep-learning-research-papers-to-code-f-f38bbd87352f
- https://medium.com/@derekchia/common-problems-when-reproducing-a-machine-learning-paper-17178515d6c6

### How the author of Resemblyzer implements GE2E loss
- [Real-time Voice Cloning thesis - Section 3.3](https://matheo.uliege.be/bitstream/2268.2/6801/5/s123578Jemine2019.pdf)

### MultiReader technique
- The authors introduced the MultiReader technique to combine different data sources, enabling to train with multiple keywords (TD-SV) and multiple languages (TI-SV and TD-SV) and helps solving the limited training data problem. 

### Dataset
- [VCTK](https://datashare.ed.ac.uk/handle/10283/3443) is a large and sufficient multi-speaker dataset
- [Mozilla Common Voice](https://commonvoice.mozilla.org/en/datasets) is a smaller multi-speaker dataset crowdsourced (Can be sufficient for prototyping)
- [VIVOS](https://paperswithcode.com/dataset/vivos) is good multi-speaker VNese voice dataset
