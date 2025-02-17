#code to calculate the core rmsd of the OE Xtal docked poses, using schrodinger because mdtraj can't recognize SMILES strings :(((((

from schrodinger import structure as struct
from schrodinger.structutils import analyze
from schrodinger.structutils import rmsd
import glob

#calculating rmsd of core structures for blind docking
home = '/home/jegan/pose_analysis/'
path = '/home/jegan/bccgc4/OE_new_docking/'

xtal = struct.Structure.read(home+'5QC4_lig_maestro.pdb', index = 1)
xtal_rec = analyze.evaluate_asl(xtal, '(( backbone ) ) AND (res.num 1-216)')
print(len(xtal_rec))

with open(home+'lig_core_rmsd/OE_docking/XTAL_rmsd.csv','w') as datafile:
    datafile.write('Ligand, Receptor number, Score, RMSD of Core structure from XTAL Ligand\n')
    data = []
        
    with open(path+'XTAL_docking/Scores.csv','r') as ligands:
        
        ligands = ligands.readlines()
        for line in ligands[1:]:
            items = line.split(',')

            ligand = items[0]
            print(ligand)
            score = items[2].rstrip()
            cen_num = 0 #there's only one receptor because this is the OE xtal docking

            recep_name = glob.glob(path+'XTAL_docking/receptor_pdbs/*.pdb')
            for pdb in recep_name:
                recep = struct.Structure.read(pdb) #defining the corresponding receptor in the epv file
            rec_atoms = analyze.evaluate_asl(recep, '(( backbone ) ) AND (res.num 3-218)') #defining the backbone atoms of the corresponding receptor
            print(len(rec_atoms))
            rmsd.superimpose(recep, rec_atoms, xtal, xtal_rec, move_which = rmsd.CT) #superimposing the coxtal structure's backbone atoms on the atoms of the current receptor

            lig = struct.Structure.read(path+'XTAL_docking/ligand_poses_pdbs/'+ligand+'.pdb')
            indices = analyze.evaluate_smarts_canvas(lig, 'C1NNC(C12)CCNC2') #getting the core indices of the ligand
            for index in indices: #because the nested list gives the rmsd calculation big problems......
                lig_core = index

            xtal_lig = analyze.evaluate_asl(xtal, '(res.ptype "BC7 ")') #getting the indices of the coxtal ligand after superposition
            xtal_lig_struct = (struct._AtomCollection(xtal, xtal_lig)).extractStructure() #extracting the coxtal ligand as a separate structure
            indices_2 = analyze.evaluate_smarts_canvas(xtal_lig_struct, 'c1nnc(c12)CCNC2') #getting core indices of coxtal ligand
            for index in indices_2:
                xtal_core = index

            core_rmsd = rmsd.calculate_in_place_rmsd(xtal_lig_struct, xtal_core, lig, lig_core) #calculating rmsd of cores

            dataline = [ligand, cen_num, score, core_rmsd]
            data.append(dataline)

        data.sort(key = lambda x: x[2])
        print(data[0])
        for line in data:
            newline = line[0]+','+str(line[1])+','+str(line[2])+','+str(line[3])+'\n'
            datafile.write(newline)
                                   
    





