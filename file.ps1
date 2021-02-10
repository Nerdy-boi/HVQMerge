## this is single threaded
##Get-ChildItem | ForEach-Object {.\hvqm2enc.exe .\$_ .\$_".hvqm"}


Get-ChildItem | ForEach-Object -Parallel {.\hvqm2enc.exe $_ $_".hvqm"} -ThrottleLimit 8;

$files = (Get-ChildItem -Path .\ -recurse -filter *.hvqm | measure).Count; 

py .\stitch.py $files


