---
title: "Hybrid Edge-HPC Systems for Low-Latency Data-Driven Inference"
collection: publications
category: preprints
permalink: /publications/2026-Hybrid-Edge
date: 2026-05-19
authors: "Liubov Kurafeeva, **Ryan Hartung**, Benjamin Carter, Alan Subedi, Avhishek Biswas, Michael Fay, Shantenu Jha, Chandra Krintz, Andre Merzky, Douglas Thain, Memet Can Vuran, and Rich Wolski"
venue: "arXiv preprint, arXiv:2605.20532"
# doiurl: ''
# paperurl: ''
preprint_url: 'https://doi.org/10.48550/arXiv.2605.20532'
preprint_pdf: 'https://arxiv.org/pdf/2605.20532'
bibID: kurafeeva2026hybrid
---

## Abstract

Cyber-physical systems often need fast predictions from live sensor streams, but improving their models can depend on simulations and training jobs running on remote high-performance computing (HPC) systems. Batch scheduling and simulation costs can delay those updates, even when inference needs to continue at the edge.

This paper presents Reverse Backfill (RBF), a hybrid architecture that separates low-latency edge inference from asynchronous, simulation-driven model improvement. Lightweight surrogate models run near the sensors, while updated models are incorporated as simulation and training results become available. The architecture supports different surrogate models and coordinates resources across edge devices, private 5G, cloud, and HPC systems.

The authors evaluate RBF in a digital-agriculture deployment that combines edge sensing with computational fluid dynamics simulations to infer airflow in a large agricultural screenhouse. The evaluation examines end-to-end behavior, including simulation latency, training cost, inference throughput, and how delayed model updates affect prediction accuracy.

## Publication details

- **Authors:** {{ page.authors }}
- **Publication:** arXiv preprint, arXiv:2605.20532 (2026)
- **Subject area:** Distributed, Parallel, and Cluster Computing (cs.DC)
- **Identifier:** [arXiv:2605.20532](https://arxiv.org/abs/2605.20532)
- **PDF:** [Download the preprint](https://arxiv.org/pdf/2605.20532)

## Citation

Kurafeeva, L., Hartung, R., Carter, B., Subedi, A., Biswas, A., Fay, M., Jha, S., Krintz, C., Merzky, A., Thain, D., Vuran, M. C., & Wolski, R. (2026). *Hybrid Edge-HPC Systems for Low-Latency Data-Driven Inference*. arXiv:2605.20532.
