# ESP-01

## Modes

### Normal boot mode (Boot from SPI Flash)

| GPIO0 | GPIO2 |
|:-----:|:-----:|
|   H   |   H   |

> In normal boot mode (GPIO0 high), GPIO2 is ignored.

### Flashing
| GPIO0 | GPIO2 |
|:-----:|:-----:|
|   L   |   H   |

> GPIO2 must also be either left unconnected/floating, or driven Low, in order to enter the serial bootloader.


## Output

For our project, we'll use GPIO2 (since it can be left as floating during boot).


0.48k
9.85k
4.69k
9.88k

14.86k
32.2k