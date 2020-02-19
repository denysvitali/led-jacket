flash:
	bash -c "echo $$'\cc' > /dev/ttyUSB0"
	echo -e -n "import machine; machine.reset()\r\n" > /dev/ttyUSB0
	sleep 1
	bash -c "echo $$'\ce' > /dev/ttyUSB0"
	cat main.py > /dev/ttyUSB0
	bash -c "echo $$'\cd' > /dev/ttyUSB0"

install:
	bash -c "echo $$'\cc' > /dev/ttyUSB0"
	echo -e -n "import machine; machine.reset()\r\n" > /dev/ttyUSB0
	sleep 1
	bash -c "echo $$'\ce' > /dev/ttyUSB0"
	cat install.py > /dev/ttyUSB0
	bash -c "echo $$'\cd' > /dev/ttyUSB0"

picoweb:
	ampy --port /dev/ttyUSB0 mkdir picoweb
	ampy --port /dev/ttyUSB0 put picoweb/__init__.py picoweb/__init__.py
	ampy --port /dev/ttyUSB0 put picoweb/utils.py picoweb/utils.py

.PHONY: flash picoweb