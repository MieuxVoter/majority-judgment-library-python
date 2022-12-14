# Majority Judgment Library for Python

[![MIT](https://img.shields.io/github/license/MieuxVoter/majority-judgment-library-python?style=for-the-badge)](./LICENSE)
[![Join the Discord chat at https://discord.gg/rAAQG9S](https://img.shields.io/discord/705322981102190593.svg?style=for-the-badge)](https://discord.gg/rAAQG9S)
![GitHub Actions](https://img.shields.io/github/checks-status/mieuxvoter/majority-judgment-library-python/main?style=for-the-badge)

Test-driven Python library to help deliberate using [Majority Judgment](https://mieuxvoter.fr/).

The goal is to be **scalable**, **reliable**, fast and extensible.
We therefore use a _score-based algorithm_ whatsoever.


## Installation

Simply use `pip` as in:

```bash
pip install git+https://github.com/MieuxVoter/majority-judgment-library-python
```

## Example Usage

Collect the **votes** for each Candidate and provide them in the function `majority_judgment` as is:

```
>>> from majority_judgment import majority_judgment
>>> data = {
...    'Pizza': [!, 0, 3, 0, 2, 0, 3, 1, 2, 3], 
...    'Chips': [0, 1, 0, 2, 1, 2, 2, 3, 2, 3],
...    'Pasta': [0, 1, 0, 1, 2, 1, 3, 2, 3, 3],
...    'Bread': [0, 1, 2, 1, 1, 2, 1, 2, 2, 3],
... }
>>> majority_judgment(data, reverse=False)
{'Chips': 0, 'Pasta': 1, 'Pizza': 2, 'Bread': 3}

```


## License
[MIT](./LICENSE)  →  _Do whatever you want except complain._

Majority Judgment itself is part of the Commons, obviously.


## Fund us

We'd love to invest more energy in Majority Judgment development.

Please consider funding us, every bit helps : https://www.paypal.com/donate/?hosted_button_id=QD6U4D323WV4S


