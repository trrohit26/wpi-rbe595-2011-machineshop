#SOURCE_LIST=$(wildcard *.tex)
#TARGET_LIST=$(patsubst %.tex,%.pdf,$(SOURCE_LIST))

.PHONY: all clean

#all: $(TARGET_LIST) 
file=guardian.pdf

all: $(file)

%.pdf: %.tex
	pdflatex $*.tex
	bibtex   $*.aux
	pdflatex $*.tex
	pdflatex $*.tex

spell: %.tex
	aspell -p ./aspell.dict -c %.tex

clean:
	- rm -vf *.aux *.log *.out *.lof *.toc *.bbl *.blg *.ent *~

remove_pdfs:
	- rm -vf $(file)

run:
	make remove_pdfs
	make 
	make 
	make clean
	- acroread $(file)
	- /usr/bin/open '$(file)'

