FILES = metadata.yaml \
		paper.md

OUTPUT = build

FLAGS = --bibliography=bibliography.bib \
		--csl=bibliography.csl \
		-s \
		-f markdown \
		--pdf-engine=xelatex

FLAGS_PDF = --template=eisvogel.latex

all: pdf

pdf:
	mkdir -p $(OUTPUT)
	pandoc -o $(OUTPUT)/paper.pdf $(FLAGS) $(FLAGS_PDF) $(FILES)

clean:
	rm -f $(OUTPUT)/*
