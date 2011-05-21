.PHONY: tags

tags:
	etags *.py
	find python-xlib/Xlib -name "*.py" | etags -a -
