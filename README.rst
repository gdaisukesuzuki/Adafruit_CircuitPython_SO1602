What is Adafruit CircuitPython SO1602
=====================================
a Pythons library which handles SO1602 
(charactor-based OEL modulesJapan's Akizuki Electronics provides)
described like adafruit's circuitpython...


Introduction
============

    python3 setup.py build
    
    
    python3 setup.py install

Usage Example
=============

.. code-block:: python

    import time
    import board
    # import digitalio # For use with SPI
    import busio
    import adafruit_so1602

    # Create library object using our Bus I2C port
    i2c = busio.I2C(board.SCL, board.SDA)
    SO1602 = adafruit_so1602.Adafruit_SO1602_I2C(i2c)

    SO1602.writeLine(str="SO1602ナンダヨ!",line=0,align="dummy")
    SO1602.writeLine(str="ΩΩΩ<ナ、ナンダッテー!?",line=1,align="dummy")

