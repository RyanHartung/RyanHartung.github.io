---
layout        : project
title         : 'Combination Lock'
author_profile: true
created_on    : 2026-07-21
last_updated  : 2026-08-14
permalink     : /projects/combination-lock/
tags:
  - Rust
  - Linux
---

## About:

The goal of this project was to create a simple program that finds the nearest repeating digit for a combination lock. I created this so that it was harder for people to guess what the password used for the combination lock.

I created the naive and distance approaches. The optimal min-distance was created by Google Gemini to test how they compared.

<br>

Here is an example:

```text
Input your combination:
==> 12345

Using naive average: "33333"
Using distance average: "33333"
Using optimal min-distance: "33333"
=====================
Original | Spin | New
1        | 2    | 3
2        | 1    | 3
3        | 0    | 3
4        | -1   | 3
5        | -2   | 3
=====================
Total spins: 6
```

Sometimes it doesn't align with the optimal solution:
```text
Input your combination:
==> 56198165189

Using naive average: "55555555555"
Using distance average: "55555555555"
Using optimal min-distance: "88888888888"
=====================
Original | Spin | New
5        | 3    | 8
6        | 2    | 8
1        | -3   | 8
9        | -1   | 8
8        | 0    | 8
1        | -3   | 8
6        | 2    | 8
5        | 3    | 8
1        | -3   | 8
8        | 0    | 8
9        | -1   | 8
=====================
Total spins: 21
```

## Link:

[Here](https://github.com/RHartung-ND/combination-lock){:target="_blank"} is the link to the GitHub for it.
