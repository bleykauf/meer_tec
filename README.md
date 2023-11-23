# MeerTEC -- Python implemenation of the MeCom interface for Meerstetter TECs.
<!--
![Test Coverage](https://raw.githubusercontent.com/bleykauf/meer_tec/master/docs/coverage.svg)
-->
[![PyPI](https://img.shields.io/pypi/v/meer_tec?color=blue)](https://pypi.org/project/meer_tec/)
![Test Status](https://github.com/bleykauf/meer_tec/actions/workflows/test.yml/badge.svg)
![Test Coverage](./docs/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Both communication via USB and [Lantronix XPort](https://www.lantronix.com/products/xport/) are supported.

Note that not all commands of [MeCom](https://www.meerstetter.ch/customer-center/compendium/64-tec-controller-remote-control) are implemented at this time. Feel free to submit more commands via a Pull Request.

## Usage

### Connection
#### USB

```python
usb = USB("COM3")
tec = TEC(usb, 0)
```

#### XPort
Create a connection to the XPort and pass it as an argument to one of the TECs

```python
xp = XPort('192.168.1.123')
tec3 = TEC(xp, 3)
```

## Commands

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

Copyright © 2020-2023 B. Leykauf

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
