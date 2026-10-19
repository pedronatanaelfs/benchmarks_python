%% MATLAB reference evaluation for all MPMOP and MPDMP benchmarks
%
% HOW TO RUN
% 1. Open this folder in MATLAB:
%       benchmarks_python/validation/matlab
% 2. Open this file.
% 3. Click the green "Run" button (or type RUN_ME_IN_MATLAB).
%
% No arguments, path edits, random seeds, or source modifications are
% required. The runner reads the deterministic CSV inputs already generated
% in ../test_inputs and evaluates the original MATLAB source code from:
%   ../../../OptMPNDS-master
%   ../../../2026ZhaoNash-main
%
% Results are written to:
%   ./results/MPMOP1.csv ... MPMOP17.csv
%   ./results/MPDMP1.csv ... MPDMP18.csv
%   ./results/metadata/*.json
%
% Please return the complete "results" folder for Python comparison.

clearvars;
clc;

fprintf('Starting MATLAB reference evaluation...\n');
fprintf('This will evaluate 35 benchmarks on shared deterministic inputs.\n\n');

run_all_matlab_reference_tests();

fprintf('\nReference evaluation finished successfully.\n');
fprintf('Please return this folder:\n  %s\n', ...
    fullfile(fileparts(mfilename('fullpath')), 'results'));
