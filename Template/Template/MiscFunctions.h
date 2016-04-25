#ifndef MISCFUNCTIONS_H
#define MISCFUNCTIONS_H

#include <string>
#include <vector>

using std::string;
using std::vector;

void PlotEtPt(  vector< vector<string> > inFileNames, vector< vector<double> > inWeights = {}, vector<string> inTitles = {}, string outName = "" );

#endif
