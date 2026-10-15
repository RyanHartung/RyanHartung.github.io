all: build update_cv

build:
	tectonic cv.tex
	tectonic resume.tex
	mv cv.pdf Ryan_CV.pdf || true
	mv resume.pdf Ryan_Resume.pdf || true
	rm *.synctex.gz || true
	rm *.log || true

update_cv:
	cd .. && python3 scripts/cv_to_markdown.py