#! /bin/bash
#
# script that scans the current directory for .md files and convertsthem using pandoc to .docx

FilesFound=$(find . -type f -name "*.md" -print)
IFSbkp="$IFS"
IFS=$'\n'
for infile in $FilesFound; do
    echo $infile
    outfile="${infile%.md}.docx"
    echo $outfile
    pandoc "$infile" --from markdown --to docx -o "$outfile"
done
