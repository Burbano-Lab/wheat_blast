# USAGE: python3 fasta2SNP_bin_matrix.py <file.fasta> > bin_matrix.txt 2> ids.txt
# STDOUT -> Matrix
# STDERR -> IDs

from sys import argv, stderr

samples = [] 
genotypes = [] 
with open(argv[1], 'r') as f: 
    for line in f: 
        if line.startswith('>'): 
            samples.append(line.strip()[1:]) 
        else: 
            if len(line.strip()) > 0: 
                genotypes.append(line.strip()) 
reference = genotypes[0]

binout = {i:'' for i in samples}
for genospersample in range(len(genotypes)): 
    binpersample = '' 
    for snp in range(len(reference)): 
        if genotypes[genospersample][snp] in ('N', '-', '?'): # Notations for missing information
            binpersample = binpersample + '9' # 9 is the default missing character for SMARTPCA
        elif genotypes[genospersample][snp] == reference[snp]: 
            binpersample = binpersample + '0' 
        else: 
            binpersample = binpersample + '1' 
    binout[samples[genospersample]] = binpersample 

for snp in range(len(genotypes[0])): 
    snpallsamples = '' 
    for sample in binout.keys(): 
        snpallsamples = snpallsamples + binout[sample][snp] 
    print(' '.join(snpallsamples)) 

print('\n'.join(binout.keys()), file = stderr)
