all: build update_cv

build:
	tectonic cv.tex
	mv cv.pdf Ryan_CV.pdf || true
	rm *.synctex.gz || true
	rm *.log || true

update_cv:
	cd .. && python3 scripts/cv_to_markdown.py