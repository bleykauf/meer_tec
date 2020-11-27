# MeerTEC -- Python implemenation of the MeCom interface for Meerstetter TECs.

<!---
[![PyPI](https://img.shields.io/pypi/v/meer_tec?color=blue)](https://pypi.org/project/meer_tec/)
[![Conda](https://img.shields.io/conda/v/conda-forge/meer_tec?color=blue&label=conda-forge)](https://anaconda.org/conda-forge/meer_tec)
[![Build Status](https://travis-ci.com/bleykauf/meer_tec.svg?branch=main)](https://travis-ci.com/bleykauf/meer_tec)
[![Documentation Status](https://readthedocs.org/projects/meer_tec/badge/?version=latest)](https://meer_tec.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/bleykauf/meer_tec/badge.svg?branch=main)](https://coveralls.io/github/bleykauf/meer_tec?branch=main)
-->
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Currently, only communication via ethernet is supported (tested only with [Lantronix XPort](https://www.lantronix.com/products/xport/)).
Note that only a small subset of [MeCom](https://www.meerstetter.ch/customer-center/compendium/64-tec-controller-remote-control) is implemented at this time.

## Usage

Create a connection to the XPort and pass it as an argument to one of the TECs

```python
xp = XPort('192.168.1.123')
tec3 = TEC(xp, 3)
```

The commands are implemented as properties. For example the target temperature
can be read by simply using

```python
tec3.target_temperature
23.0

tec3.target_temperature = 23.1
```



## Authors

-   Bastian Leykauf (<https://github.com/bleykauf>)

## License

MeerTEC -- Python implemenation of the MeCom interface for Meerstetter TECs.

Copyright © 2020 B. Leykauf

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
