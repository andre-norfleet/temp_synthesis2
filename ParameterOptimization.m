% usage: 
% ParameterOptimization.m "weka_file" "output_file"
%
% runs particle swarm optimization to find parameters in the cellular potts
% model that result in the best TSSL score
%
% positional arguments:
% weka_file: the name of the Weka classifier corresponding to a pattern
% output_file: the name of a file specified to store the results
%
% example:
% octave ParameterOptimization.m "BullseyeRules1.txt" "OptimizationResults.txt" 

clear
%arg_list = argv ();
%if nargin < 2
%    error('weka_file and output_file must be specified');
%elseif nargin > 2
%    error('too many positional arguments');
%end
particles = 25; % Total number of particles for PSO
%parameters = 4; % Total number of paramters that we want to synthesize
parameters = 2;
%bounds = [1e-19 1e-16;1e-19 1e-17;1e-19 1e-17;1e-9 1e-7]; % Bounds for all parameters
bounds = [1e-19 1e-16; 1e-19 1e-17]; 
maxIterations = 20; % Maximum number of PSO iterations 
weka_file = "BETSENormAutoscale3formula.txt"; % File containing Weka rules
formula = getFormulaVariance(weka_file,1024);
output_file = "OptimizationResults2.txt";  % Name for output file
tic
[ optimised_parameters ] = Particle_Swarm_Optimization_Parallel ...
    (particles, parameters, bounds, 'averageScore', 'max', 2, 2.5, 3.5, 0.4, 0.9, maxIterations,formula,output_file);
toc

