#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"

using namespace ROOT::VecOps;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;

float bugfix_mj1j2_nob(int n_tight_nob, int j1_isB, int j2_isB, int j3_isB, int j4_isB, float mj1j2, float mj1j3, float mj1j4, float mj2j3, float mj2j4, float mj3j4){
// current logic is fully correct but just an approximation, in order to speed up the loop
  if (n_tight_nob<2) return -99.0;
  else{
    if (j1_isB==0){
      if (j2_isB==0) return mj1j2;
      else if (j3_isB==0) return mj1j3;
      else return mj1j4;
    }
    else{
      if (j2_isB==0){
        if (j3_isB==0) return mj2j3;
        else return mj2j4;
      }
      else return mj3j4;
    }
  }
}
float bugfix_detaj1j2_nob(int n_tight_nob, int j1_isB, int j2_isB, int j3_isB, int j4_isB, float detaj1j2, float detaj1j3, float detaj1j4, float detaj2j3, float detaj2j4, float detaj3j4){
// current logic is fully correct but just an approximation, in order to speed up the loop
  if (n_tight_nob<2) return -99.0;
  else{
    if (j1_isB==0){
      if (j2_isB==0) return detaj1j2;
      else if (j3_isB==0) return detaj1j3;
      else return detaj1j4;
    }
    else{
      if (j2_isB==0){
        if (j3_isB==0) return detaj2j3;
        else return detaj2j4;
      }
      else return detaj3j4;
    }
  }
}
