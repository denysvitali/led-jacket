flash:
	bash -c "echo $$'\cc' > /dev/ttyUSB0"
	echo -e -n "import machine; machine.reset()\r\n" > /dev/ttyUSB0
	sleep 1
	bash -c "echo $$'\ce' > /dev/ttyUSB0"
	cat main.py > /dev/ttyUSB0
	bash -c "echo $$'\cd' > /dev/ttyUSB0"

.PHONY: flash
 