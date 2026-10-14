---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

<style>
  .cv-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5em;
    margin-bottom: 1.5em;
  }

  .cv-panel[hidden] {
    display: none !important;
  }

  .cv-pdf-frame {
    display: block;
    width: 100%;
    height: 85vh;
    min-height: 600px;
    border: 1px solid rgba(128, 128, 128, 0.35);
    border-radius: 4px;
  }

  .cv-pdf-fallback {
    margin-top: 0.5em;
    font-size: 0.8em;
  }
</style>

<div class="cv-controls">
  <button type="button" class="btn btn--inverse" data-cv-target="cv-pdf"
          aria-expanded="false" aria-controls="cv-pdf">View Embedded PDF</button>
  <a class="btn btn--inverse" href="{{ base_path }}/cv/Ryan_CV.pdf"
     target="_blank" rel="noopener">Open PDF in New Tab</a>
  <button type="button" class="btn btn--inverse" data-cv-target="cv-text"
          aria-expanded="false" aria-controls="cv-text">View Text Version</button>
</div>

<div id="cv-pdf" class="cv-panel" hidden>
  <iframe class="cv-pdf-frame" title="Ryan Hartung CV (PDF)"
          data-src="{{ base_path }}/cv/Ryan_CV.pdf#view=FitH"></iframe>
  <p class="cv-pdf-fallback">
    PDF not showing up? <a href="{{ base_path }}/cv/Ryan_CV.pdf" target="_blank" rel="noopener">Open it directly</a>.
  </p>
</div>

<div id="cv-text" class="cv-panel" markdown="1" hidden>

<!-- Begin CV -->
# Ryan Hartung

<rhartung@nd.edu> · [GitHub](https://github.com/RHartung-ND) · [LinkedIn](https://www.linkedin.com/in/ryan-hartung-19a901237/) · [ORCID](https://orcid.org/0009-0001-2961-7528) · [Website](https://ryanhartung.github.io/)

## Education

### The University of Notre Dame — Notre Dame, IN

**Ph.D. in Computer Science & Engineering** — *Expected May 2029*

- Advisor: Dr. Douglas Thain

- Research Focus: Distributed Systems and High-Performance Computing

### The University of Notre Dame — Notre Dame, IN

**Master of Science in Computer Science & Engineering** — *August 2025*

### The University of Texas at Austin — Austin, TX

**Bachelor of Science in Physics (Computation Option)** — *May 2024*

- Certificate in Elements of Computing

## Publications

- **2026** — Liubov Kurafeeva, **Ryan Hartung**, Benjamin Carter, Alan Subedi, Avhishek Biswas, Michael Fay, Shantenu Jha, Chandra Krintz, Andre Merzky, Douglas Thain, Mehmet Vuran, and Rich Wolski. “Hybrid Edge-HPC Systems for Low-Latency Data-Driven Inference.” *arXiv preprint arXiv:2605.20532*. <https://arxiv.org/abs/2605.20532>

- **2025** — Liubov Kurafeeva, Alan Subedi, **Ryan Hartung**, Michael Fay, Avhishek Biswas, Shantenu Jha, Ozgur Kilic, Chandra Krintz, Andre Merzky, Douglas Thain, Mehmet Vuran, and Rich Wolski. “xGFabric: Coupling Sensor Networks and HPC Facilities with 5G Wireless Networks for Real-Time Digital Agriculture.” In *Proceedings of the SC ’25 Workshops*. ACM, 2317–2327. DOI: <https://doi.org/10.1145/3731599.3767589>

## Research Experience

### The University of Notre Dame — Notre Dame, IN

**Graduate Research Assistant** — January 2025 – Present

- Contributing to the design and implementation of [xGFabric](https://sites.google.com/view/xgfabric), an architectural framework connecting remote sensor edge networks to HPC centers via 5G.

- Developing low-latency data pipelines to facilitate real-time inference across heterogeneous edge-HPC infrastructure.

### The University of Texas at Austin — Austin, TX

**Undergraduate Research Assistant** — June 2022 – December 2023

- Engineered an open-source Python tool analyzing star-spot patterns across 6,000+ star systems with optimized array processing algorithms.

- Evaluated star-spot contrast ratios using observational data from NASA Kepler and TESS missions to establish baseline metrics for exoplanet detection.

- Integrated parallel processing and multi-core compilation to optimize data throughput and execution runtime.

- Published codebase and workflows to an open-source [GitHub repository](https://github.com/BrownDwarf/contracosta/); research funded by NASA grant.

## Work Experience

### Hargrove Engineers and Constructors — Katy, TX

**Controls & Automations Engineering Intern** — May 2024 – August 2024

- Automated the migration of 200,000+ lines of Dow MOD5 code into Honeywell Experion with no loss of functionality.

- Tracked, analyzed, and documented over 7,000 variables to design flow diagrams visualizing variable definitions.

- Developed several algorithms to expedite the migration and variable mapping processes, improving overall efficiency.

### Hargrove Engineers and Constructors — Katy, TX

**Controls & Automations Engineering Intern** — May 2023 – August 2023

- Instantiated existing library modules to complete Westlake’s PVC plant Reactor and Train configuration.

- Performed safety testing on all module and sequence configurations on simulated ABB hardware.

- Successfully configured Modbus communication between the ABB and HIMA system controllers.

- Updated structured text configuration to handle cross-controller communications.

## Talks, Panels, & Presentations

### GCASR 2026 — Evanston, IL

**Poster Presenter** — May 11, 2026

- Poster: *Hybrid Edge-HPC Systems for Low-Latency Data-Driven Inference*.

### Supercomputing ’25 — St. Louis, MO

**Presenter and Demonstrator** — November 17 – 19, 2025

- Presented xGFabric and its findings at the Department of Energy’s (DOE) booth.

- Gave a live demo to DOE staff, SC attendees, and fellow researchers, showcasing:

  - Real-time data transfer between a Raspberry Pi and a 5G sensor, with live latency and throughput metrics.

  - The full end-to-end pipeline: fetching and parsing data, launching simulations, and rending results.

### Supercomputing ’25 — St. Louis, MO

**Invited Panelist** — November 16, 2025

- Participated in an expert panel on edge-to-HPC loop architectures and the future of computing during the XLOOP Workshop \[[Recording available online](https://vimeo.com/1139653482?share=copy&fl=sv&fe=ci)\].

### HPDC 2025 — Notre Dame, IN

**Poster Presenter** — July 21, 2025

- Poster: *xGFabric: Coupling Sensor Networks and HPC Facilities with 5G Wireless Networks for Real-Time Digital Agriculture*.

## Teaching Experience

### The University of Notre Dame — Notre Dame, IN

**Graduate Teaching Assistant** — August 2024 – May 2025

- CSE 10102; Elements of Computing II (Spring 2025): 37 students; held office hours, graded, assisted with in-class coding.

- CSE 10001; Principles of Computing (Fall 2024): 35 students; proctored exams and graded.

## Technical Skills

- **Programming Languages:** Bash, C, Python, Rust, Java, JavaScript/NodeJS, SQL

- **Web Development:** CSS, Django, HTML, Jekyll, React

- **Batch Schedulers:** HTCondor, SLURM, Univa Grid Engine (UGE)

- **Tools & Platforms:** ABB, Docker, Git, Honeywell, LaTeX, Linux/UNIX, MPI, OpenFOAM, OpenMP, ParaView

## Leadership & Service

- **Order of Christian Initiation of Adults (OCIA)**, Sponsor — September 2026 – Present

- **Fischer Graduate Residence Mass**, Lector — August 2025 – May 2026

- **Society of Catholic Scientists**, Member — August 2025 – Present

- **Science Policy Initiative at Notre Dame**, Member — August 2025 – Present

- **Catholic Graduate Community**, Member — April 2025 – Present

- **Technology and Catholicism Club**, Member — February 2025 – Present

- **Notre Dame Rock Climbing Club**, Member — August 2024 – Present

- **Notre Dame Texas Club**, Member — August 2024 – Present

- **Science Olympiad**, Competitor, Mentor, President, Event Supervisor, and Lab Coordinator — August 2011 – Present
<!-- End CV -->

</div>

<script>
  (() => {
    const buttons = document.querySelectorAll("[data-cv-target]");

    const show = (targetId) => {
      buttons.forEach((button) => {
        const panel = document.getElementById(button.dataset.cvTarget);
        const isOpen = button.dataset.cvTarget === targetId;

        panel.hidden = !isOpen;
        button.setAttribute("aria-expanded", String(isOpen));
        button.classList.toggle("btn--primary", isOpen);
        button.classList.toggle("btn--inverse", !isOpen);

        /* Only load the PDF the first time it's opened */
        const frame = panel.querySelector("iframe[data-src]");
        if (isOpen && frame && !frame.getAttribute("src")) {
          frame.src = frame.dataset.src;
        }
      });
    };

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const alreadyOpen = button.getAttribute("aria-expanded") === "true";
        show(alreadyOpen ? null : button.dataset.cvTarget);
      });
    });

    /* Arriving from site search: open the text CV so matches can be highlighted */
    if (new URLSearchParams(window.location.search).has("search")) {
      show("cv-text");
    }
  })();
</script>
