import os, sys, json
from shutil import copyfile
import subprocess
from os.path import join, getsize

SingleFile_Size=400.
SingleFile_Size_data=2000.

year = sys.argv[1]

PWD=os.getcwd()
CERNBOX='/eos/user/m/melu/'

os.chdir(CERNBOX)
if year=='2017':
  samplejson='samples2017.json'
  if os.path.isdir('VBSTop_2017') is False:
      os.mkdir('VBSTop_2017')
      os.chdir('VBSTop_2017')
      os.system(r"cp %s'hadd.py' ."%(CERNBOX))
  else:
    os.chdir('VBSTop_2017')
    os.system(r"cp %s'hadd.py' ."%(CERNBOX))
    

samplejson=PWD+'/../crab/'+samplejson

samples_name=[]
samples_name2=[]
samples_dir=[]

with open(samplejson, 'r') as fin:
  data=fin.read()
  lines=json.loads(data)
  keys=lines.keys()
  for key, value in lines.items():
    samples_name.append(key)
    samples_dir.append(value[1].split('/')[1])
    samples_name2.append(value[0])

print(samples_name2)
for isample in range(0,len(samples_name)):
  for root, dirs, files in os.walk(CERNBOX+samples_dir[isample],topdown = False):
    if not '000' in root:continue
    if 'log' in root:continue
    if 'Muon' in samples_name[isample] or 'EG' in samples_name[isample]:
      continue
      if not samples_name2[isample] in root:continue
      n_files=len(files)
      size_temp=sum(getsize(join(root, name))/(1024*1024.) for name in files)
      print 'Sample size (MB) of',samples_name2[isample],':', size_temp
      print 'number of root files:',n_files
      print 'Sample size (MB) of each root file', float(size_temp/n_files)
      if size_temp<SingleFile_Size_data:
        print 'very small sample, only one merge file is needed!'
        tmp_cmd=''
        for ifile in range(0,len(files)):
          tmp_cmd=tmp_cmd+' '+root+'/'+files[ifile]
        tmp_cmd='python hadd.py '+samples_name2[isample]+'.root '+tmp_cmd
        print "command:",tmp_cmd
        os.system(tmp_cmd)
      else:
        N_file=round(size_temp/SingleFile_Size_data)
        print 'should have number of merged file:', N_file
        print 'each merged file includes root file:', int(round(n_files/N_file))
        tmp_cmd=''
        if N_file>n_files or float(size_temp/n_files)>SingleFile_Size_data:
          print "don't need to merge root file, cp them into current directory!"
          for itemp in range(0,n_files):
            tmp_cmd='eoscp %s ./%s'%(root+'/'+files[itemp], files[itemp].replace('tree',samples_name2[isample]))
            print "command:",tmp_cmd
            os.system(tmp_cmd)
        else:
          for icmd in range(0,int(N_file)-1):
            tmp_cmd=''
            for ifile in files[-int(round(n_files/N_file)):]:
              tmp_cmd=tmp_cmd+' '+root+'/'+ifile
            tmp_cmd='python hadd.py '+samples_name2[isample]+'_'+str(icmd+1)+'.root '+tmp_cmd
            print "command:",tmp_cmd
            os.system(tmp_cmd)
            files=files[:-int(round(n_files/N_file))]
          tmp_cmd=''
          for ifile in files:
            tmp_cmd=tmp_cmd+' '+root+'/'+ifile
          tmp_cmd='python hadd.py '+samples_name2[isample]+'_'+str(int(N_file))+'.root '+tmp_cmd
          print "command:",tmp_cmd
          os.system(tmp_cmd)
      print '*********'
    else:
      if not samples_name2[isample]=='tbarW':continue
      n_files=len(files)
      size_temp=sum(getsize(join(root, name))/(1024*1024.) for name in files)
      print 'Sample size (MB) of',samples_name2[isample],':', size_temp
      print 'number of root files:',n_files
      print 'Sample size (MB) of each root file:', float(size_temp/n_files)
      if size_temp<SingleFile_Size:
        print 'very small sample, only one merge file is needed!'
        tmp_cmd=''
        for ifile in range(0,len(files)):
          tmp_cmd=tmp_cmd+' '+root+'/'+files[ifile]
        tmp_cmd='python hadd.py '+samples_name2[isample]+'.root '+tmp_cmd
        print "command:",tmp_cmd
        os.system(tmp_cmd)
      else:
        tmp_cmd=''
        N_file=round(size_temp/SingleFile_Size)
        print 'should have number of merged file:', N_file
        print 'each merged file includes root file:', int(round(n_files/N_file))
        if N_file>n_files or float(size_temp/n_files)>SingleFile_Size:
          print "don't need to merge root file, cp them into current directory!"
          for itemp in range(0,n_files):
            tmp_cmd='eoscp %s ./%s'%(root+'/'+files[itemp], files[itemp].replace('tree',samples_name2[isample]))
            print "command:",tmp_cmd
            os.system(tmp_cmd)
        else:
          for icmd in range(0,int(N_file)-1):
            tmp_cmd=''
            for ifile in files[-int(round(n_files/N_file)):]:
              tmp_cmd=tmp_cmd+' '+root+'/'+ifile
            tmp_cmd='python hadd.py '+samples_name2[isample]+'_'+str(icmd+1)+'.root '+tmp_cmd
            print "command:",tmp_cmd
            os.system(tmp_cmd)
            files=files[:-int(round(n_files/N_file))]
          tmp_cmd=''
          for ifile in files:
            tmp_cmd=tmp_cmd+' '+root+'/'+ifile
          tmp_cmd='python hadd.py '+samples_name2[isample]+'_'+str(int(N_file))+'.root '+tmp_cmd
          print "command:",tmp_cmd
          os.system(tmp_cmd)

      print '*********'

os.chdir(PWD)
