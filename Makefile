# Author: Hsiaoming Yang <lepture@me.com>
# Website: http://lepture.com

.PHONY: doc publish


doc:
	doki.py -t default --title=July --github=july README.md > index.html


publish:
	git push origin gh-pages
