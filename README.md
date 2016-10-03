A simple parity game solver that implements [Zielonka's dynamic proramming algorithm][Z1998].

This was an exercise to evaluate [graph-tool][gt], which provides python bindings for
the graph library from [boost.org][boost] and is the only dependency to run this code.

You can execute the evaluation of a demo game with

```sh
./solve.py examples/game1.dot
```

See also the output of `./solve -h` for more formating info.

[gt]: https://graph-tool.skewed.de/
[Z1998]: http://doi.org/10.1016/S0304-3975(98)00009-7
[boost]: http://www.boost.org/
