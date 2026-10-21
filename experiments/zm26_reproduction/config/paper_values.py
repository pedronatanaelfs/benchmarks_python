"""Numerical values transcribed from ZM26 Tables II and III.

Source: arXiv:2601.22497 HTML, Section V-B.
Each entry is mean (std). null means not reported.
"""

# Table II. MPMOP, D=2, Psi_NP raw product and meanIGD.
TABLE_II = {
    "MPMOP1": {
        "OptMPNDS": {"nash_score": (4.21e7, 5.94e6), "meanIGD": (1.44e0, 2.96e-1)},
        "OptAll": {"nash_score": (7.79e5, 1.37e6), "meanIGD": (9.52e-1, 2.56e-2)},
    },
    "MPMOP2": {
        "OptMPNDS": {"nash_score": (8.11e2, 2.49e1), "meanIGD": (9.36e-2, 1.72e-2)},
        "OptAll": {"nash_score": (5.26e1, 2.13e1), "meanIGD": (7.53e-2, 9.64e-3)},
    },
    "MPMOP3": {
        "OptMPNDS": {"nash_score": (6.12e5, 3.26e3), "meanIGD": (1.08e-1, 3.16e-4)},
        "OptAll": {"nash_score": (9.02e4, 2.65e4), "meanIGD": (1.15e-1, 1.85e-3)},
    },
    "MPMOP4": {
        "OptMPNDS": {"nash_score": (1.18e1, 5.58e0), "meanIGD": (6.59e-2, 2.77e-3)},
        "OptAll": {"nash_score": (1.24e1, 8.35e0), "meanIGD": (6.63e-2, 2.87e-3)},
    },
    "MPMOP5": {
        "OptMPNDS": {"nash_score": (8.86e1, 1.85e1), "meanIGD": (1.05e-1, 5.40e-3)},
        "OptAll": {"nash_score": (8.87e1, 1.38e1), "meanIGD": (1.06e-1, 5.11e-3)},
    },
    "MPMOP6": {
        "OptMPNDS": {"nash_score": (7.10e0, 2.08e0), "meanIGD": (1.30e-1, 5.97e-3)},
        "OptAll": {"nash_score": (6.32e0, 2.16e0), "meanIGD": (1.32e-1, 6.97e-3)},
    },
    "MPMOP7": {
        "OptMPNDS": {"nash_score": (2.87e12, 2.25e11), "meanIGD": (1.27e0, 4.44e-1)},
        "OptAll": {"nash_score": (1.51e9, 6.23e9), "meanIGD": (1.28e0, 2.06e-1)},
    },
    "MPMOP8": {
        "OptMPNDS": {"nash_score": (4.91e5, 6.40e3), "meanIGD": (1.97e-1, 2.74e-2)},
        "OptAll": {"nash_score": (3.68e3, 3.06e3), "meanIGD": (2.50e-1, 3.68e-2)},
    },
    "MPMOP9": {
        "OptMPNDS": {"nash_score": (4.20e13, 7.97e13), "meanIGD": (1.95e-1, 3.96e-3)},
        "OptAll": {"nash_score": (4.78e13, 8.21e13), "meanIGD": (1.95e-1, 4.22e-3)},
    },
    "MPMOP10": {
        "OptMPNDS": {"nash_score": (3.20e3, 5.91e2), "meanIGD": (1.42e-1, 8.52e-3)},
        "OptAll": {"nash_score": (3.16e3, 5.58e2), "meanIGD": (1.40e-1, 8.33e-3)},
    },
    "MPMOP11": {
        "OptMPNDS": {"nash_score": (8.10e5, 6.96e3), "meanIGD": (1.97e-1, 8.66e-3)},
        "OptAll": {"nash_score": (1.09e5, 4.90e4), "meanIGD": (2.91e-1, 2.08e-2)},
    },
}

# Table III. MPDMP, log Psi_NP (natural log, inferred; see PAPER_PARAMETER_AUDIT.md)
TABLE_III = {
    "MPDMP1": {
        "OptAll": {"log_nash": (6.6979, 0.1748), "meanIGD": (4.04e0, 2.46e0)},
        "OptMPNDS": {"log_nash": (8.6562, 0.0028), "meanIGD": (5.45e-2, 2.95e-2)},
        "OptMPNDS2": {"log_nash": (8.6556, 0.0017), "meanIGD": (4.76e-2, 2.77e-2)},
        "OptMPNDS3": {"log_nash": (8.6565, 0.0024), "meanIGD": (4.47e-2, 2.85e-2)},
    },
    "MPDMP2": {
        "OptAll": {"log_nash": (8.3224, 0.1470), "meanIGD": (3.94e0, 2.06e0)},
        "OptMPNDS": {"log_nash": (9.2360, 0.0051), "meanIGD": (6.49e-2, 3.44e-2)},
        "OptMPNDS2": {"log_nash": (9.2362, 0.0044), "meanIGD": (6.17e-2, 3.25e-2)},
        "OptMPNDS3": {"log_nash": (9.2354, 0.0037), "meanIGD": (5.77e-2, 3.57e-2)},
    },
    "MPDMP3": {
        "OptAll": {"log_nash": (4.6996, 0.1737), "meanIGD": (2.73e0, 6.63e-1)},
        "OptMPNDS": {"log_nash": (6.4921, 0.0082), "meanIGD": (2.11e-1, 4.80e-2)},
        "OptMPNDS2": {"log_nash": (6.4905, 0.0076), "meanIGD": (2.15e-1, 4.19e-2)},
        "OptMPNDS3": {"log_nash": (6.4855, 0.0087), "meanIGD": (1.13e-1, 3.53e-2)},
    },
    "MPDMP4": {
        "OptAll": {"log_nash": (9.3076, 0.1440), "meanIGD": (1.78e-2, 1.38e-2)},
        "OptMPNDS": {"log_nash": (10.1946, 0.0028), "meanIGD": (9.58e-4, 2.11e-3)},
        "OptMPNDS2": {"log_nash": (10.1949, 0.0033), "meanIGD": (1.05e-3, 1.66e-3)},
        "OptMPNDS3": {"log_nash": (10.1826, 0.0039), "meanIGD": (1.33e-2, 6.03e-3)},
    },
    "MPDMP5": {
        "OptAll": {"log_nash": (9.5794, 0.1495), "meanIGD": (6.90e0, 6.07e-1)},
        "OptMPNDS": {"log_nash": (10.4618, 0.0048), "meanIGD": (2.97e0, 9.16e-2)},
        "OptMPNDS2": {"log_nash": (10.4620, 0.0041), "meanIGD": (2.94e0, 1.23e-1)},
        "OptMPNDS3": {"log_nash": (10.4666, 0.0027), "meanIGD": (2.66e0, 9.88e-2)},
    },
    "MPDMP6": {
        "OptAll": {"log_nash": (8.9463, 0.1413), "meanIGD": (3.23e0, 7.96e-1)},
        "OptMPNDS": {"log_nash": (9.9652, 0.0013), "meanIGD": (1.32e-1, 8.91e-3)},
        "OptMPNDS2": {"log_nash": (9.9645, 0.0011), "meanIGD": (1.30e-1, 9.17e-3)},
        "OptMPNDS3": {"log_nash": (9.9630, 0.0003), "meanIGD": (8.38e-2, 1.37e-2)},
    },
    "MPDMP7": {
        "OptAll": {"log_nash": (9.5011, 0.1493), "meanIGD": (8.93e0, 1.25e0)},
        "OptMPNDS": {"log_nash": (10.5529, 0.0032), "meanIGD": (2.45e0, 1.33e-1)},
        "OptMPNDS2": {"log_nash": (10.5530, 0.0028), "meanIGD": (2.45e0, 1.31e-1)},
        "OptMPNDS3": {"log_nash": (10.5549, 0.0020), "meanIGD": (2.26e0, 1.10e-1)},
    },
    "MPDMP8": {
        "OptAll": {"log_nash": (9.7392, 0.1291), "meanIGD": (6.23e0, 8.02e-1)},
        "OptMPNDS": {"log_nash": (11.0936, 0.0043), "meanIGD": (2.46e0, 6.52e-2)},
        "OptMPNDS2": {"log_nash": (11.0935, 0.0046), "meanIGD": (2.46e0, 8.63e-2)},
        "OptMPNDS3": {"log_nash": (11.0970, 0.0026), "meanIGD": (2.25e0, 5.57e-2)},
    },
    "MPDMP9": {
        "OptAll": {"log_nash": (14.9919, 0.1150), "meanIGD": (6.71e0, 3.17e0)},
        "OptMPNDS": {"log_nash": (16.1469, 0.0010), "meanIGD": (3.10e-2, 2.25e-2)},
        "OptMPNDS2": {"log_nash": (16.1464, 0.0022), "meanIGD": (2.15e-2, 1.85e-2)},
        "OptMPNDS3": {"log_nash": (16.1363, 0.0040), "meanIGD": (2.03e-1, 8.75e-1)},
    },
    "MPDMP10": {
        "OptAll": {"log_nash": (14.3334, 0.1151), "meanIGD": (6.55e0, 3.20e0)},
        "OptMPNDS": {"log_nash": (15.4952, 0.0021), "meanIGD": (9.64e-2, 4.75e-2)},
        "OptMPNDS2": {"log_nash": (15.4957, 0.0017), "meanIGD": (8.45e-2, 4.78e-2)},
        "OptMPNDS3": {"log_nash": (15.4953, 0.0017), "meanIGD": (6.99e-2, 3.51e-2)},
    },
    "MPDMP11": {
        "OptAll": {"log_nash": (17.1521, 0.1428), "meanIGD": (1.79e0, 1.79e0)},
        "OptMPNDS": {"log_nash": (18.8487, 0.0062), "meanIGD": (1.39e0, 9.76e-2)},
        "OptMPNDS2": {"log_nash": (18.8495, 0.0053), "meanIGD": (1.38e0, 7.83e-2)},
        "OptMPNDS3": {"log_nash": (18.8566, 0.0029), "meanIGD": (1.19e0, 4.58e-2)},
    },
    "MPDMP12": {
        "OptAll": {"log_nash": (17.2519, 0.1562), "meanIGD": (1.02e1, 1.62e0)},
        "OptMPNDS": {"log_nash": (18.5885, 0.0032), "meanIGD": (2.74e0, 1.49e-1)},
        "OptMPNDS2": {"log_nash": (18.5891, 0.0032), "meanIGD": (2.78e0, 1.42e-1)},
        "OptMPNDS3": {"log_nash": (18.5889, 0.0023), "meanIGD": (2.79e0, 3.17e-1)},
    },
}

PAPER_RANKING_NOTES = {
    "Table_II_best_nash": {
        "MPMOP1": "OptMPNDS",
        "MPMOP2": "OptMPNDS",
        "MPMOP3": "OptMPNDS",
        "MPMOP4": "OptAll",
        "MPMOP5": "OptAll",
        "MPMOP6": "OptMPNDS",
        "MPMOP7": "OptMPNDS",
        "MPMOP8": "OptMPNDS",
        "MPMOP9": "OptAll",
        "MPMOP10": "OptMPNDS",
        "MPMOP11": "OptMPNDS",
    },
    "Table_II_best_meanIGD": {
        "MPMOP1": "OptAll",
        "MPMOP2": "OptAll",
        "MPMOP3": "OptMPNDS",
        "MPMOP4": "OptMPNDS",
        "MPMOP5": "OptMPNDS",
        "MPMOP6": "OptMPNDS",
        "MPMOP7": "OptMPNDS",
        "MPMOP8": "OptMPNDS",
        "MPMOP9": "tie",
        "MPMOP10": "OptAll",
        "MPMOP11": "OptMPNDS",
    },
}
