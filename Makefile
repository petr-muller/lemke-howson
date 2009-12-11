all:
	make -C	program
	make -C prototype
	make -C doc

clean:
	make -C	program  	clean
	make -C prototype	clean
	make -C doc				clean
