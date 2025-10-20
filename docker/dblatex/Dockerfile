FROM ubuntu:bionic

# Latex packages
RUN apt-get update && \	
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-german texlive-lang-english && \	
	apt-get install -y dblatex && \
	apt-get install -y  inkscape   

WORKDIR /documents

