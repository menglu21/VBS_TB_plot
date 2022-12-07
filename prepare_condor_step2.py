import os,json
import sys
from os import walk

def prepare_condor():
  for root, dirs, files in os.walk(BASIC_PATH,topdown = False):
        samples=files
  return samples


BASIC_PATH="/eos/user/m/melu/VBSTop_2017/"
PWD=os.getcwd()

samplejson='samples2017.json'
samplejson=PWD+'/../crab/'+samplejson

samples_name=[]
samples_dir=[]

with open(samplejson, 'r') as fin:
  data=fin.read()
  lines=json.loads(data)
  keys=lines.keys()
  for key, value in lines.items():
    samples_dir.append(key)
    samples_name.append(value[0])

#region: onelep_b_region, onelep_nob_region, tt2L_region, dy_region
Region = sys.argv[1]
#category: one, two (one lep or two lep category)
Category = sys.argv[2]

if __name__ == "__main__":

  WORKING_DIR=Region+'_'+Category
  os.mkdir(WORKING_DIR)

  samples_counts=[]
  samples_ineos=prepare_condor()
  wrapper_dir=PWD+'/wrapper.sh'

  sample_dict={}
  for iname in range(0,len(samples_name)):
    sample_dict[samples_name[iname]]=[]

  for iname in range(0,len(samples_name)):
    for isamp in samples_ineos:
      if isamp.startswith(samples_name[iname]+'_'):sample_dict[samples_name[iname]].append(isamp)

  for iname in range(0,len(samples_name)):
    samples_counts.append(len(sample_dict[samples_name[iname]]))

  for iname in range(0,len(samples_dir)):
    print samples_dir[iname]
    print PWD
    os.mkdir(samples_dir[iname])
    os.chdir(samples_dir[iname])
    os.system(r'cp ../make_hists.py .')
    os.system(r'cp ../TB.h .')
    os.system(r'cp ../sub.jdl .')
    for i in range(0,samples_counts[iname]):
      os.mkdir(samples_dir[iname]+'_'+str(i))
      os.chdir(samples_dir[iname]+'_'+str(i))
      os.system(r'cp %s .'%(wrapper_dir))
      name_temp=BASIC_PATH+sample_dict[samples_name[iname]][i]
      name_temp=name_temp.replace("/","DUMMY")
      os.system(r'sed -i "s/dummyroot/%s/g" wrapper.sh' %(name_temp))
      os.system(r'sed -i "s/INPUT/%s/g" wrapper.sh' %(name_temp.split('DUMMY')[-1]))
      os.system(r'sed -i "s/REGION/%s/g" wrapper.sh' %(Region))
      os.system(r'sed -i "s/CATEGORY/%s/g" wrapper.sh' %(Category))
      os.system(r'sed -i "s/DUMMY/\//g" wrapper.sh')
      os.chdir(PWD+'/'+samples_dir[iname])
    os.chdir(PWD+'/'+samples_dir[iname])
    os.system(r'sed -i "s/NUMBER/%s/g" sub.jdl' %(samples_counts[iname]))
    os.system(r'sed -i "s/DUMMY/%s/g" sub.jdl' %(samples_dir[iname]))
    os.chdir(PWD)
    os.system(r'mv %s %s'%(samples_dir[iname], WORKING_DIR))

