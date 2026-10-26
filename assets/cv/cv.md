# Ryan Hartung

U.S. Citizen · South Bend, IN · (713) 449-9492 · <rhartung@nd.edu>\
[github.com/RHartung-ND](https://github.com/RHartung-ND) · [linkedin.com/in/ryanhartung](https://www.linkedin.com/in/ryanhartung/) · [ryanhartung.github.io](https://ryanhartung.github.io/)

## Education

### The University of Notre Dame — Notre Dame, IN

**Ph.D. in Computer Science & Engineering** — Expected May 2029

- Advisor: Dr. Douglas Thain

- Research Focus: Portability, Reliability, and Scalability of Distributed and High-Performance Systems

*M.S. in Computer Science & Engineering* — *Aug 2024 – Aug 2025*

- Master’s Project: HPC integration and multi-site portability for the xGFabric framework

### The University of Texas at Austin — Austin, TX

**B.S. in Physics (Computation Option)** — Aug 2020 – May 2024

- Certificate in Elements of Computing

## Publications

- **2026** — Liubov Kurafeeva, **Ryan Hartung**, Benjamin Carter, Alan Subedi, Avhishek Biswas, Michael Fay, Shantenu Jha, Chandra Krintz, Andre Merzky, Douglas Thain, Mehmet Vuran, and Rich Wolski. “Asynchronous Scientific Workflows for Simulation-Driven Inference Across the Edge–HPC Computing Continuum.” *Future Generation Computer Systems* (Elsevier), special issue. (Under review).

- **2026** — Liubov Kurafeeva, Benjamin Carter, **Ryan Hartung**, Alan Subedi, Avhishek Biswas, Michael Fay, Shantenu Jha, Chandra Krintz, Andre Merzky, Douglas Thain, Mehmet Vuran, and Rich Wolski. “GROWFLOW: Low-latency Computational Fluid Dynamics at the Edge for Real-time Agricultural Decision Support.” In *Proceedings of IEEE Smart Connected Systems and Emerging Technologies Conference (IEEE SCSETech)*, 2026 (To appear).

- **2026** — Liubov Kurafeeva, **Ryan Hartung**, Benjamin Carter, Alan Subedi, Avhishek Biswas, Michael Fay, Shantenu Jha, Chandra Krintz, Andre Merzky, Douglas Thain, Mehmet Vuran, and Rich Wolski. “Hybrid Edge-HPC Systems for Low-Latency Data-Driven Inference.” *arXiv preprint arXiv:2605.20532*. <https://arxiv.org/abs/2605.20532>

- **2025** — Liubov Kurafeeva, Alan Subedi, **Ryan Hartung**, Michael Fay, Avhishek Biswas, Shantenu Jha, Ozgur Kilic, Chandra Krintz, Andre Merzky, Douglas Thain, Mehmet Vuran, and Rich Wolski. “xGFabric: Coupling Sensor Networks and HPC Facilities with 5G Wireless Networks for Real-Time Digital Agriculture.” In *Proceedings of the SC ’25 Workshops*. ACM, 2317–2327. DOI: <https://doi.org/10.1145/3731599.3767589>

## Research Experience

### The University of Notre Dame — Notre Dame, IN

**Graduate Research Assistant, Cooperative Computing Lab** — Jan 2025 – Present

- Engineered the HPC integration pipeline for xGFabric, enabling real-time streaming of remote 5G sensor data directly into Computational Fluid Dynamics (CFD) simulations.

- Standardized multi-site deployment across 4 supercomputing facilities (ND CRC, Purdue Anvil, TACC Stampede3, NERSC Perlmutter), resolving cross-platform incompatibilities in hardware, OSs, and batch schedulers.

- Converted sequential Bash scripts into a production-ready Makeflow/Work Queue workflow, co-scheduling 72 concurrent OpenFOAM jobs at NERSC and meeting the 2-hour turnaround deadline for surrogate ML model inference (PINN/FNO/PCR).

- Ported the workflow to HTCondor and implemented a [“wait-for-workers”](https://github.com/cooperative-computing-lab/cctools/pull/4546) feature in Work Queue and TaskVine (CCTools), bringing `salloc`-style co-scheduling to throughput computing.

- Built a proof-of-concept Random Forest model predicting queue wait times for 4–64 core jobs, trained on multi-month queue data collected across 3 HPC sites.

- Identified OpenFOAM simulation as the pipeline’s latency bottleneck; profiled scaling from 1–64 cores across 1–4 nodes and found single-node 32–64 core runs minimized turnaround, outperforming multi-node runs.

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

### Harris County — Houston, TX

**Elections Clerk** — May 2022 & Dec 2023

- Assisted with polling operations, equipment setup and takedown, and ballot transportion.

## Talks, Panels, & Presentations

### GCASR 2026 — Evanston, IL

**Poster Presenter** — May 11, 2026

- Poster: *Hybrid Edge-HPC Systems for Low-Latency Data-Driven Inference*.

### Supercomputing ’25 — St. Louis, MO

**Presenter, Demonstrator, and Panelist** — November 16 – 19, 2025

- Featured panelist for the XLOOP Workshop expert session on edge-to-HPC loop architectures and computing trends \[[Recording available online](https://vimeo.com/1139653482?share=copy&fl=sv&fe=ci)\].

- Presented xGFabric and its findings at the Department of Energy’s (DOE) booth using a live demo to an audience of DOE staff, SC attendees, and fellow researchers. The demo showcased the full end-to-end pipeline: fetching and parsing data, launching simulations, and rendering results.

### HPDC 2025 — Notre Dame, IN

**Poster Presenter** — July 21, 2025

- Poster: *xGFabric: Coupling Sensor Networks and HPC Facilities with 5G Wireless Networks for Real-Time Digital Agriculture*.

## Teaching Experience

### The University of Notre Dame — Notre Dame, IN

**Graduate Teaching Assistant** — August 2024 – May 2025

- CSE 10102; Elements of Computing II (Spring 2025): 37 students; held office hours, graded, assisted with in-class coding.

- CSE 10001; Principles of Computing (Fall 2024): 35 students; proctored exams and graded.

## Technical Skills

**Programming Languages:** Bash, C, CUDA, Java, Python, Rust, SQL

**HPC & Distributed Systems:** HTCondor, Makeflow, MPI, OpenMP, Slurm, Univa Grid Engine (UGE), Work Queue

**Technologies:** Docker, Git, Linux/UNIX, Make/CMake, OpenFOAM, ParaView, Spack, Vim

**Web Development:** CSS, HTML, JavaScript/NodeJS, Jekyll, React

**Languages:** English (native), Spanish (intermediate; stronger reading)

## Projects

**[High-Performance Distributed Systems](https://github.com/RHartung-ND/rhartung-hpds)** \| *C, CUDA, OpenMP, HTCondor* — *Aug 2026 – Present*

- Wrote CUDA and hybrid CPU+GPU versions of three benchmarks; hybrid versions ran 419× (heat) and 77× (wave) faster than serial CPU, and up to 13× faster than GPU-only.

- Characterized CPU/GPU crossover: kernel launch and transfer overhead let the CPU outperform the GPU on grids below ~128–256 elements.

- Measured compiler auto-vectorization on a 1D heat solver (`-O3` gave ~7× over unoptimized code; SIMD ISA flags had negligible effect) and OpenMP N-body scaling across sockets.

**[Bminor Compiler](https://github.com/RHartung-ND/Rust-Compiler)** \| *C, Rust, x86 Assembly* — *Oct 2025 – Present*

- Ported a multi-stage C compiler to idiomatic Rust, implementing lexing, AST parsing, static type checking, and x86-64 code generation.

- Refactored C’s legacy pointer-heavy data structures into memory-safe pattern matching and algebraic types.

**[Linux Auto-scroller](https://github.com/RHartung-ND/Auto-Scroll-Linux)** \| *Rust* — *Jun 2025 – Present*

- Engineered a low-level system utility bringing native middle-click auto-scrolling to Linux.

- Interfaced with system input APIs to calculate cursor displacement and dynamically modulate scroll speed.

## Leadership & Service

**Order of Christian Initiation of Adults (OCIA)**, Sponsor — September 2026 – Present

**CCL Web & Communications:** Writing blog posts, publishing lab announcements, and maintaining the Cooperative Computing Lab’s website. — May 2026 – Present

## Memberships, Clubs, & Interests

**Fischer Graduate Residence Mass**, Lector — August 2025 – May 2026

**Society of Catholic Scientists**, Member — August 2025 – Present

**Science Policy Initiative at Notre Dame**, Member — August 2025 – Present

**Association for Computing Machinery (ACM)**, Student Member — May 2025 – Present

**Catholic Graduate Community**, Member — April 2025 – Present

**Technology and Catholicism Club**, Member — February 2025 – Present

**Notre Dame Rock Climbing Club**, Member — August 2024 – Present

**Notre Dame Texas Club**, Member — August 2024 – Present

**Science Olympiad**, Competitor, Mentor, President, Event Supervisor, and Lab Coordinator — August 2011 – Present

**Interests:** Language learning/linguistics, volleyball, intramural soccer, road trips, anime/manga
