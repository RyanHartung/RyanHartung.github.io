# Check if running inside a Pixi environment
ifndef PIXI_PROJECT_NAME
$(error Pixi environment is not active. Run 'pixi run make' or 'pixi shell' first)
endif

all: build clear_temp_files to_markdown to_docx to_odt

build:
	tectonic cv.tex

clear_temp_files:
	rm *.synctex.gz || true
	rm *.log || true

to_markdown:
	python3 ../../scripts/tex_to_markdown.py --input cv.tex --output cv.md

to_docx:
	python3 ../../scripts/tex_to_doc.py --input cv.tex --output cv.docx

to_odt:
	python3 ../../scripts/tex_to_doc.py --input cv.tex --output cv.odt
